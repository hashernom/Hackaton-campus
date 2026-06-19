"""COPILOTO — servidor web.

Sirve el dashboard React y expone el backend como API:
  GET  /             -> el panel (dashboard)
  GET  /report       -> página móvil de captura de anomalías (se abre vía QR)
  GET  /api/state    -> JSON del estado de cabina (polling ~300ms)
  GET  /video_feed   -> stream MJPEG de la cámara
  GET  /event.jpg    -> última captura de emergencia (fatiga)
  GET  /api/qr.png   -> QR que apunta a /report (para que el conductor lo escanee)
  POST /api/incident -> sube foto -> clasifica (VLM) -> estima demora -> guarda + Telegram
  GET  /api/incidents-> lista de incidencias almacenadas
  GET  /incidents/<f>-> imagen de una incidencia

Uso:
  python copiloto/server.py
  python copiloto/server.py --no-model --l1 1.0 --l2 3.0
  python copiloto/server.py --no-engine        # solo incidencias (no usa cámara)
  python copiloto/server.py --public-url https://xxxx.ngrok.io
Abrir el dashboard en http://localhost:5000 ; el móvil escanea el QR.
Detener: Ctrl+C
"""
import argparse
import io
import socket
import sys
import threading
import time
from pathlib import Path

from flask import (Flask, Response, jsonify, request, send_file,
                   send_from_directory, abort)

import config
import db
import incidents
import notifier
import trip as trip_mod
from engine import CopilotoEngine

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app = Flask(__name__)
engine = None        # se crea en main() (puede ser None con --no-engine)
_public_base = ""    # base URL para el QR (se fija en main())


# =====================================================================
# Dashboard de cabina (fatiga) — igual que antes
# =====================================================================

@app.route("/")
def index():
    return send_file(WEB_DIR / "index.html")


def _default_state():
    """Estado con forma completa para cuando no hay motor (--no-engine)."""
    trip = trip_mod.load_trip()
    contact = trip_mod.primary_contact(trip)
    return {
        "status": "ok", "level": 0, "driver": trip.get("driver", "Conductor"),
        "contact": {"name": contact.get("name", "Contacto"), "notified": False},
        "risk": False, "risk_secs": 0.0,
        "signals": {"model_label": "-", "model_score": 0.0, "ear": 0.0,
                    "eyes_closed": False, "looking_away": False,
                    "face_present": True, "reason": None},
        "alert_count": 0, "fps": 0.0,
        "thresholds": {"level1_secs": config.LEVEL1_SECS, "level2_secs": config.LEVEL2_SECS},
        "last_event": None, "engine": False,
    }


@app.route("/api/state")
def api_state():
    if engine is None:
        return jsonify(_default_state())
    return jsonify(engine.get_state())


@app.route("/api/trip", methods=["GET"])
def api_trip_get():
    trip = trip_mod.load_trip()
    contact = trip_mod.primary_contact(trip)
    return jsonify({
        "active": trip_mod.is_active(),
        "driver": trip.get("driver"),
        "contact": {"name": contact.get("name"), "chat_id": contact.get("chat_id")},
    })


@app.route("/api/trip", methods=["POST"])
def api_trip_set():
    data = request.get_json(silent=True) or request.form
    driver = (data.get("driver") or "").strip()
    contact_name = (data.get("contact_name") or "Contacto").strip()
    chat_id = (data.get("chat_id") or "").strip()
    if not driver:
        abort(400, "Falta el nombre del conductor.")
    trip_mod.start_trip(driver, [{"name": contact_name, "chat_id": chat_id}])
    if engine is not None:
        engine.reload_trip()
    return jsonify({"ok": True})


@app.route("/api/trip/end", methods=["POST"])
def api_trip_end():
    trip_mod.end_trip()
    if engine is not None:
        engine.reload_trip()
    return jsonify({"ok": True})


def _mjpeg_generator():
    boundary = b"--frame\r\n"
    while True:
        jpeg = engine.get_jpeg() if engine is not None else None
        if jpeg is not None:
            yield (boundary +
                   b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n")
        time.sleep(0.05)


@app.route("/video_feed")
def video_feed():
    return Response(_mjpeg_generator(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/event.jpg")
def event_image():
    if config.EVENT_IMAGE.exists():
        return send_file(config.EVENT_IMAGE, mimetype="image/jpeg")
    abort(404)


# =====================================================================
# Incidencias por foto (QR -> móvil -> VLM -> Postgres -> Telegram)
# =====================================================================

@app.route("/report")
def report_page():
    return send_file(WEB_DIR / "report.html")


@app.route("/api/qr.png")
def api_qr():
    """QR que codifica la URL de /report para que el conductor lo escanee."""
    import qrcode
    url = f"{_public_base}/report"
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(buf.getvalue(), mimetype="image/png")


@app.route("/api/report_url")
def api_report_url():
    return jsonify({"url": f"{_public_base}/report"})


@app.route("/api/incident", methods=["POST"])
def api_incident():
    """Recibe foto (+nombre opcional) -> clasifica -> estima demora -> guarda -> Telegram."""
    photo = request.files.get("photo")
    driver_input = (request.form.get("driver_input") or "").strip() or None
    lat, lng = request.form.get("lat"), request.form.get("lng")
    location = None
    try:
        if lat and lng:
            location = {"lat": float(lat), "lng": float(lng)}
    except ValueError:
        location = None

    if photo is None and not driver_input:
        abort(400, "Falta la foto o el nombre de la anomalía.")

    trip = trip_mod.load_trip()
    contact = trip_mod.primary_contact(trip)

    # Guardar la foto
    image_path = None
    if photo is not None:
        config.INCIDENTS_DIR.mkdir(exist_ok=True)
        image_path = config.INCIDENTS_DIR / f"inc_{int(time.time() * 1000)}.jpg"
        photo.save(str(image_path))

    # Clasificar + estimar demora
    result = incidents.classify_anomaly(
        str(image_path) if image_path else None, driver_input=driver_input)
    typ = result.get("type")
    conf = result.get("confidence", 0.0)
    delay = incidents.estimate_delay(driver_input or typ or "")

    # Estado: auto si confianza alta o el conductor confirmó el nombre; si no, revisión.
    if typ is None:
        status = "needs_review"
    elif conf >= config.INCIDENT_CONF_THRESHOLD or driver_input:
        status = "auto"
    else:
        status = "needs_review"

    incident_id = db.add_incident(
        trip_driver=trip.get("driver"),
        type=typ,
        description=result.get("description"),
        driver_input=driver_input,
        confidence=conf,
        justifies_delay=result.get("justifies_delay", False),
        estimated_delay_min=delay,
        status=status,
        location=location,
        image_path=str(image_path) if image_path else None,
    )

    # Reporte a Telegram al contacto del viaje (sirve a cualquier conductor).
    notified = False
    if status == "auto":
        caption = (
            f"🚧 Anomalía reportada por {trip.get('driver')}: "
            f"{result.get('description') or driver_input}"
            f" (confianza {conf * 100:.0f}%). "
            f"Demora estimada: {delay} min. "
            f"Hora: {time.strftime('%H:%M:%S')}."
        )
        notified = notifier.notify(
            caption,
            photo_path=str(image_path) if image_path else None,
            chat_id=contact.get("chat_id"),
            respect_cooldown=False,
        )

    return jsonify({
        "id": incident_id,
        "type": typ,
        "description": result.get("description"),
        "confidence": conf,
        "justifies_delay": result.get("justifies_delay", False),
        "estimated_delay_min": delay,
        "status": status,
        "notified": notified,
    })


@app.route("/api/estimate")
def api_estimate():
    """Estimado de demora a partir del nombre de la anomalía (recálculo en vivo)."""
    name = request.args.get("name", "")
    return jsonify({
        "type": incidents.normalize_to_type(name),
        "estimated_delay_min": incidents.estimate_delay(name),
    })


@app.route("/api/incidents")
def api_incidents():
    items = db.list_incidents(limit=50)
    for it in items:
        path = it.get("image_path")
        it["image_url"] = ("/incidents/" + Path(path).name) if path else None
    return jsonify(items)


@app.route("/incidents/<path:filename>")
def incident_image(filename):
    return send_from_directory(config.INCIDENTS_DIR, filename)


# =====================================================================

def _lan_ip():
    """IP de la laptop en la red local (para que el móvil llegue por el QR)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def main():
    global engine, _public_base
    # Consola de Windows (cp1252) revienta con emoji; forzamos UTF-8 tolerante.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    ap = argparse.ArgumentParser(description="Servidor web de COPILOTO")
    ap.add_argument("--camera", type=int, default=config.CAMERA_INDEX)
    ap.add_argument("--no-model", action="store_true", help="No cargar el modelo HF (usa EAR)")
    ap.add_argument("--no-mediapipe", action="store_true", help="No usar MediaPipe")
    ap.add_argument("--no-engine", action="store_true", help="No usar cámara (solo incidencias)")
    ap.add_argument("--l1", type=float, default=None, help="Segundos para Nivel 1")
    ap.add_argument("--l2", type=float, default=None, help="Segundos para Nivel 2")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--host", default="0.0.0.0", help="0.0.0.0 para que el móvil llegue")
    ap.add_argument("--public-url", default=None, help="URL pública para el QR (ngrok, etc.)")
    args = ap.parse_args()

    # Base de datos de incidencias
    db.init_db()

    # URL para el QR
    if args.public_url:
        _public_base = args.public_url.rstrip("/")
    elif config.PUBLIC_URL:
        _public_base = config.PUBLIC_URL.rstrip("/")
    else:
        _public_base = f"http://{_lan_ip()}:{args.port}"

    # Pre-cargar el modelo de imagen en un hilo para que la 1ª foto no cuelgue.
    if config.INCIDENT_USE_MODEL:
        threading.Thread(target=incidents.warmup, daemon=True).start()

    # Motor de cabina (opcional)
    if not args.no_engine:
        engine = CopilotoEngine(
            camera=args.camera,
            use_model=not args.no_model,
            use_mediapipe=not args.no_mediapipe,
            l1=args.l1,
            l2=args.l2,
        ).start()

    print(f"[server] Dashboard:  http://localhost:{args.port}")
    print(f"[server] Reporte QR: {_public_base}/report")
    # threaded=True: el stream MJPEG no debe bloquear el polling de /api/state.
    # use_reloader=False: evita arrancar el motor (y la cámara) dos veces.
    app.run(host=args.host, port=args.port, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
