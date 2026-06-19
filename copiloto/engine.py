"""COPILOTO — motor de detección reutilizable.

Encapsula el bucle de visión (cámara -> modelo HF + MediaPipe -> escalado ->
notificación) en una clase manejable por un servidor web o cualquier consumidor.

Publica, de forma thread-safe:
  - get_jpeg()  : el último cuadro (limpio) codificado en JPEG, para MJPEG.
  - get_state() : un dict con la forma EXACTA del contrato que espera el front.

El bucle corre en un hilo de fondo (start()), igual de robusto que live_demo:
  - Sin modelo HF: usa EAR de MediaPipe para somnolencia.
  - Sin MediaPipe: usa solo el modelo HF.
  - Sin token de Telegram: notifier cae a consola.
"""
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


# Mapa nivel -> status del contrato del front.
_STATUS = {0: "ok", 1: "warning", 2: "alert"}


class CopilotoEngine:
    """Motor de visión en hilo de fondo. Publica estado + frame para la web."""

    def __init__(self, camera=None, use_model=True, use_mediapipe=True,
                 l1=None, l2=None):
        self.camera_index = config.CAMERA_INDEX if camera is None else camera
        self.use_model = use_model
        self.use_mediapipe = use_mediapipe
        self.l1 = l1
        self.l2 = l2

        self.trip = trip_mod.load_trip()
        self.contact = trip_mod.primary_contact(self.trip)

        self._lock = threading.Lock()
        self._jpeg = None
        self._state = self._initial_state()
        self._contact_notified = False
        self._last_event = None

        self._stop = False
        self._thread = None
        self._worker = None
        self._face = None

    # --- ciclo de vida -----------------------------------------------------

    def start(self):
        """Arranca el bucle de detección en un hilo daemon."""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def stop(self):
        self._stop = True
        if self._worker is not None:
            self._worker.stop()

    def reload_trip(self):
        """Re-lee el viaje/contacto (tras registrar o finalizar desde la web)."""
        self.trip = trip_mod.load_trip()
        self.contact = trip_mod.primary_contact(self.trip)
        print(f"[engine] viaje recargado: {self.trip['driver']} -> {self.contact['name']}")

    # --- accesores thread-safe --------------------------------------------

    def get_state(self):
        with self._lock:
            return dict(self._state)

    def get_jpeg(self):
        with self._lock:
            return self._jpeg

    # --- internos ----------------------------------------------------------

    def _initial_state(self):
        l1 = config.LEVEL1_SECS if self.l1 is None else self.l1
        l2 = config.LEVEL2_SECS if self.l2 is None else self.l2
        return {
            "status": "ok",
            "level": 0,
            "driver": self.trip["driver"],
            "contact": {"name": self.contact["name"], "notified": False},
            "risk": False,
            "risk_secs": 0.0,
            "signals": {
                "model_label": "-",
                "model_score": 0.0,
                "ear": 0.0,
                "eyes_closed": False,
                "looking_away": False,
                "face_present": False,
                "reason": None,
            },
            "alert_count": 0,
            "fps": 0.0,
            "thresholds": {"level1_secs": l1, "level2_secs": l2},
            "last_event": None,
        }

    def _setup_detectors(self):
        if self.use_model:
            try:
                from model import DrowsinessModel
                self._worker = ModelWorker(DrowsinessModel())
            except Exception as e:
                print(f"[engine] Modelo HF no disponible ({e}). Uso MediaPipe/EAR.")
        if self.use_mediapipe:
            try:
                from distraction import FaceMeshDetector
                if FaceMeshDetector.available():
                    self._face = FaceMeshDetector()
            except Exception as e:
                print(f"[engine] MediaPipe no disponible ({e}).")

    def _run(self):
        self._setup_detectors()
        if self._worker is None and self._face is None:
            print("[engine][FATAL] No hay ni modelo HF ni MediaPipe.")
            return

        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print(f"[engine][FATAL] No se pudo abrir la cámara {self.camera_index}.")
            return

        escalator = Escalator(l1_secs=self.l1, l2_secs=self.l2)
        prev_t = time.time()
        fps = 0.0

        print(f"[engine] Conductor: {self.trip['driver']} | "
              f"Contacto: {self.contact['name']} "
              f"({self.contact.get('chat_id') or 'sin chat_id'})")
        print("[engine] En marcha.")

        while not self._stop:
            ok, frame = cap.read()
            if not ok:
                print("[engine] Fin del stream de cámara.")
                break

            now = time.time()
            dt = now - prev_t
            prev_t = now
            if dt > 0:
                fps = 0.9 * fps + 0.1 * (1.0 / dt) if fps else 1.0 / dt

            # --- Modelo HF (hilo de fondo) ---
            model_label, model_score, model_risk = "EAR", 0.0, False
            if self._worker is not None:
                self._worker.submit(frame)
                model_label = self._worker.label
                model_score = self._worker.score
                model_risk = self._worker.risk

            # --- MediaPipe (EAR / mirada) ---
            ear = 0.0
            eyes_closed = looking_away = False
            face_present = False
            motivo = None
            if self._face is not None:
                st = self._face.analyze(frame)
                ear = st["ear"] if st["ear"] is not None else 0.0
                eyes_closed = st["eyes_closed"]
                looking_away = st["looking_away"]
                face_present = st["face_present"]
                motivo = st["motivo"]

            is_risk = bool(model_risk or eyes_closed or looking_away or
                           (self._face is not None and not face_present))
            level = escalator.update(is_risk)

            # --- Nivel 2: notificar al contacto ---
            if level == 2:
                cv2.imwrite(str(config.EVENT_IMAGE), frame)
                causa = motivo or (model_label if model_risk else "riesgo")
                caption = (f"⚠️ {self.trip['driver']} muestra signos de riesgo "
                           f"({causa}) a las {time.strftime('%H:%M:%S')}. "
                           f"Está conduciendo solo: contáctalo.")
                sent = notifier.notify(caption, photo_path=str(config.EVENT_IMAGE),
                                       chat_id=self.contact.get("chat_id"))
                # 'notificado' = se disparó el aviso (aunque caiga a consola en fallback).
                self._contact_notified = True
                self._last_event = {
                    "time": time.strftime("%H:%M:%S"),
                    "reason": causa,
                    # cache-buster para que cada alerta muestre su propia captura
                    "image_url": f"/event.jpg?t={int(now)}",
                    "notified": True,
                }
            elif level == 0:
                # Al recuperarse, el contacto vuelve a "en espera".
                self._contact_notified = False

            # --- Publicar frame (limpio) + estado ---
            ok_jpg, buf = cv2.imencode(".jpg", frame,
                                       [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            state = {
                "status": _STATUS[level],
                "level": level,
                "driver": self.trip["driver"],
                "contact": {
                    "name": self.contact["name"],
                    "notified": self._contact_notified,
                },
                "risk": is_risk,
                "risk_secs": round(escalator.risk_secs, 1),
                "signals": {
                    "model_label": model_label,
                    "model_score": round(float(model_score), 4),
                    "ear": round(float(ear), 3),
                    "eyes_closed": bool(eyes_closed),
                    "looking_away": bool(looking_away),
                    "face_present": bool(face_present) if self._face is not None else True,
                    "reason": motivo,
                },
                "alert_count": escalator.alert_count,
                "fps": round(fps, 1),
                "thresholds": {
                    "level1_secs": escalator.l1_secs,
                    "level2_secs": escalator.l2_secs,
                },
                "last_event": self._last_event,
            }

            with self._lock:
                if ok_jpg:
                    self._jpeg = buf.tobytes()
                self._state = state

        cap.release()
        print("[engine] Detenido.")
