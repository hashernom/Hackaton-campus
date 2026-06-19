"""Detección por puntos faciales con MediaPipe (API Tasks: FaceLandmarker).

Proporciona dos señales sin entrenar nada:
  - Somnolencia por EAR (eye aspect ratio): ojos cerrados sostenidos.
  - Distracción: mirar a un lado (yaw de la cabeza) o sin rostro presente.

Sirve también como PLAN B robusto: si el modelo HF no se puede instalar
(p. ej. torch sin wheel para esta versión de Python), live_demo puede usar
EAR para detectar somnolencia igualmente.

Nota: la build de MediaPipe para Python 3.14 solo expone la API Tasks, por eso
usamos FaceLandmarker (no la antigua solutions.face_mesh). La topología de
landmarks es la misma (478 puntos), así que los índices de EAR no cambian.
"""
import math

import config

try:
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision
    _HAS_MP = True
except Exception:
    _HAS_MP = False

# Índices de landmarks (FaceMesh) para el EAR de cada ojo: 6 puntos por ojo.
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE = [362, 385, 387, 263, 373, 380]
NOSE_TIP = 1
LEFT_EYE_OUTER = 263
RIGHT_EYE_OUTER = 33


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _ear(pts):
    # pts en orden: [p1 esquina, p2, p3, p4 esquina, p5, p6]
    a = _dist(pts[1], pts[5])
    b = _dist(pts[2], pts[4])
    c = _dist(pts[0], pts[3])
    return (a + b) / (2.0 * c + 1e-6)


def ensure_model():
    """Descarga face_landmarker.task si no existe. Devuelve la ruta (str)."""
    path = config.FACE_LANDMARKER_PATH
    if not path.exists():
        import requests
        print("[mediapipe] descargando face_landmarker.task ...")
        r = requests.get(config.FACE_LANDMARKER_URL, timeout=60)
        r.raise_for_status()
        path.write_bytes(r.content)
        print(f"[mediapipe] modelo guardado en {path}")
    return str(path)


class FaceMeshDetector:
    """Analiza un cuadro y devuelve estado facial usando FaceLandmarker."""

    def __init__(self):
        if not _HAS_MP:
            raise RuntimeError("mediapipe (Tasks API) no está disponible")
        model_path = ensure_model()
        options = mp_vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=model_path),
            running_mode=mp_vision.RunningMode.IMAGE,
            num_faces=1,
        )
        self.landmarker = mp_vision.FaceLandmarker.create_from_options(options)

    @staticmethod
    def available():
        return _HAS_MP

    def analyze(self, frame_bgr):
        """Devuelve dict: face_present, eyes_closed, looking_away, ear, motivo."""
        import cv2
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        res = self.landmarker.detect(mp_image)

        if not res.face_landmarks:
            return {
                "face_present": False,
                "eyes_closed": False,
                "looking_away": False,
                "ear": None,
                "motivo": "sin_rostro",
            }

        lm = res.face_landmarks[0]

        def px(i):
            return (lm[i].x * w, lm[i].y * h)

        ear = (_ear([px(i) for i in RIGHT_EYE]) + _ear([px(i) for i in LEFT_EYE])) / 2.0
        eyes_closed = ear < config.EAR_THRESHOLD

        # Yaw aproximado: posición horizontal de la nariz entre los dos ojos.
        nose = px(NOSE_TIP)
        le, re = px(LEFT_EYE_OUTER), px(RIGHT_EYE_OUTER)
        eye_span = abs(le[0] - re[0]) + 1e-6
        center_x = (le[0] + re[0]) / 2.0
        yaw_ratio = (nose[0] - center_x) / eye_span
        looking_away = abs(yaw_ratio) > config.YAW_THRESHOLD

        motivo = None
        if eyes_closed:
            motivo = "ojos_cerrados"
        elif looking_away:
            motivo = "mirada_fuera_via"

        return {
            "face_present": True,
            "eyes_closed": eyes_closed,
            "looking_away": looking_away,
            "ear": round(ear, 3),
            "motivo": motivo,
        }
