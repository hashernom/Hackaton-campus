"""COPILOTO — bucle principal en vivo.

Orquesta: webcam -> (modelo HF de somnolencia + MediaPipe) -> escalado ->
alerta en cabina (voz/visual) -> notificación remota al contacto.

Diseñado para degradar con gracia:
  - Sin modelo HF (torch no instalado): usa EAR de MediaPipe para somnolencia.
  - Sin MediaPipe: usa solo el modelo HF.
  - Sin token de Telegram: la notificación cae a consola.

Uso:
  python copiloto/live_demo.py
  python copiloto/live_demo.py --no-model      # solo MediaPipe (EAR)
  python copiloto/live_demo.py --camera 1 --l1 1.0 --l2 3.0
Salir: tecla q
"""
import argparse
import threading
import time

import cv2

import config
import trip as trip_mod
from alerts import Escalator
import notifier


class ModelWorker:
    """Corre el modelo HF en un hilo de fondo para no bloquear el video.

    El bucle principal entrega el último cuadro con submit(); el worker
    infiere a su propio ritmo (~5 fps en CPU) y publica el resultado.
    """

    def __init__(self, model):
        self.model = model
        self._frame = None
        self._lock = threading.Lock()
        self.label, self.score, self.risk = "-", 0.0, False
        self._stop = False
        self._t = threading.Thread(target=self._run, daemon=True)
        self._t.start()

    def submit(self, frame):
        with self._lock:
            self._frame = frame

    def _run(self):
        while not self._stop:
            with self._lock:
                f = None if self._frame is None else self._frame.copy()
                self._frame = None
            if f is None:
                time.sleep(0.01)
                continue
            try:
                lbl, sc = self.model.predict(f)
                self.label, self.score, self.risk = lbl, sc, self.model.is_risk(lbl)
            except Exception as e:
                print(f"[worker] error de inferencia: {e}")

    def stop(self):
        self._stop = True

GREEN = (60, 180, 75)
ORANGE = (0, 140, 255)
RED = (40, 40, 230)
WHITE = (255, 255, 255)


def draw_overlay(frame, level, status_text, info_lines, alert_count):
    h, w = frame.shape[:2]
    color = {0: GREEN, 1: ORANGE, 2: RED}[level]
    label = {0: "OK", 1: "ALERTA: RIESGO", 2: "EMERGENCIA - CONTACTO AVISADO"}[level]

    # Banda superior
    cv2.rectangle(frame, (0, 0), (w, 60), color, -1)
    cv2.putText(frame, f"COPILOTO  |  {label}", (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, WHITE, 2)

    # Borde de riesgo
    if level >= 1:
        cv2.rectangle(frame, (0, 0), (w - 1, h - 1), color, 8)

    # Líneas de info
    y = 90
    for line in [status_text] + info_lines:
        cv2.putText(frame, line, (15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)
        cv2.putText(frame, line, (15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        y += 28

    cv2.putText(frame, f"alertas: {alert_count}", (15, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)
    return frame


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--camera", type=int, default=config.CAMERA_INDEX)
    ap.add_argument("--no-model", action="store_true", help="No cargar el modelo HF (usa EAR)")
    ap.add_argument("--no-mediapipe", action="store_true", help="No usar MediaPipe")
    ap.add_argument("--l1", type=float, default=None, help="Segundos para Nivel 1")
    ap.add_argument("--l2", type=float, default=None, help="Segundos para Nivel 2")
    args = ap.parse_args()

    trip = trip_mod.load_trip()
    contact = trip_mod.primary_contact(trip)
    print(f"[copiloto] Conductor: {trip['driver']} | Contacto: {contact['name']} ({contact['chat_id'] or 'sin chat_id'})")

    # --- Modelo HF (opcional, en hilo de fondo) ---
    worker = None
    if not args.no_model:
        try:
            from model import DrowsinessModel
            worker = ModelWorker(DrowsinessModel())
        except Exception as e:
            print(f"[copiloto] Modelo HF no disponible ({e}). Uso MediaPipe/EAR.")

    # --- MediaPipe (opcional) ---
    face = None
    if not args.no_mediapipe:
        try:
            from distraction import FaceMeshDetector
            if FaceMeshDetector.available():
                face = FaceMeshDetector()
        except Exception as e:
            print(f"[copiloto] MediaPipe no disponible ({e}).")

    if worker is None and face is None:
        print("[copiloto][FATAL] No hay ni modelo HF ni MediaPipe. Instala dependencias.")
        return

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"[copiloto][FATAL] No se pudo abrir la cámara {args.camera}.")
        return

    escalator = Escalator(l1_secs=args.l1, l2_secs=args.l2)

    prev_t = time.time()
    fps = 0.0

    print("[copiloto] En marcha. Pulsa 'q' para salir.")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("[copiloto] Fin del stream de cámara.")
            break

        # FPS
        now = time.time()
        dt = now - prev_t
        prev_t = now
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt) if fps else 1.0 / dt

        # --- Modelo HF (hilo de fondo): entrega cuadro y lee último resultado ---
        last_label, last_score, model_risk = "-", 0.0, False
        if worker is not None:
            worker.submit(frame)
            last_label, last_score, model_risk = worker.label, worker.score, worker.risk

        # --- Señales de MediaPipe ---
        ear_txt = ""
        face_risk = False
        motivo = None
        if face is not None:
            st = face.analyze(frame)
            ear_txt = f"EAR:{st['ear']}" if st["ear"] is not None else "EAR:-"
            face_risk = st["eyes_closed"] or st["looking_away"] or (not st["face_present"])
            motivo = st["motivo"]

        is_risk = bool(model_risk or face_risk)
        level = escalator.update(is_risk)

        # --- Escalado a Nivel 2: notificar al contacto ---
        if level == 2:
            cv2.imwrite(str(config.EVENT_IMAGE), frame)
            causa = motivo or (last_label if model_risk else "riesgo")
            caption = (f"⚠️ {trip['driver']} muestra signos de riesgo "
                       f"({causa}) a las {time.strftime('%H:%M:%S')}. "
                       f"Está conduciendo solo: contáctalo.")
            notifier.notify(caption, photo_path=str(config.EVENT_IMAGE),
                            chat_id=contact.get("chat_id"))

        # --- Overlay ---
        status = (f"modelo HF: {last_label} ({last_score:.2f})"
                  if worker is not None else "modelo: EAR (MediaPipe)")
        info = [
            status,
            f"{ear_txt}   riesgo:{'SI' if is_risk else 'no'}   t_riesgo:{escalator.risk_secs:.1f}s",
            f"contacto: {contact['name']}   FPS:{fps:.1f}",
        ]
        draw_overlay(frame, level, f"viaje de {trip['driver']}", info, escalator.alert_count)
        cv2.imshow("COPILOTO", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if worker is not None:
        worker.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
