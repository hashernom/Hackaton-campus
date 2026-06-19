"""Configuración central de COPILOTO.

Lee variables de entorno desde copiloto/.env (si existe) y expone constantes.
Todas las rutas se anclan a la ubicación de este archivo, así funciona
sin importar desde qué carpeta se ejecute.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    _HAS_DOTENV = True
except Exception:  # dotenv es opcional
    _HAS_DOTENV = False

BASE_DIR = Path(__file__).resolve().parent
if _HAS_DOTENV:
    load_dotenv(BASE_DIR / ".env")


def _get(name, default):
    val = os.getenv(name)
    return val if val not in (None, "") else default


# --- Telegram ---
TELEGRAM_BOT_TOKEN = _get("TELEGRAM_BOT_TOKEN", "")
DEFAULT_CHAT_ID = _get("DEFAULT_CHAT_ID", "")

# --- Modelo de somnolencia (Hugging Face) ---
# ViT fine-tuned con etiquetas {0:'notdrowsy', 1:'drowsy'}. Verificado cargable.
MODEL_NAME = _get("MODEL_NAME", "chbh7051/driver-drowsiness-detection")

# Palabras clave de "riesgo" (somnolencia) y de "ok" (negación) en la etiqueta.
# Se evalúa OK primero para no confundir 'notdrowsy' (contiene 'drowsy') con riesgo.
RISK_LABEL_KEYWORDS = ["drowsy", "sleep", "closed", "fatigue", "yawn", "tired"]
OK_LABEL_KEYWORDS = ["not", "non", "awake", "open", "alert", "natural", "no_"]


def label_is_risk(label):
    """True si la etiqueta indica riesgo (somnolencia). Maneja negaciones."""
    l = str(label).lower()
    if any(n in l for n in OK_LABEL_KEYWORDS):
        return False
    return any(k in l for k in RISK_LABEL_KEYWORDS)

# --- Umbrales de escalado (segundos) ---
LEVEL1_SECS = float(_get("LEVEL1_SECS", "1.5"))   # alerta en cabina (voz/visual)
LEVEL2_SECS = float(_get("LEVEL2_SECS", "4.0"))   # notificar a contacto remoto
VOICE_COOLDOWN = float(_get("VOICE_COOLDOWN", "5.0"))
NOTIFY_COOLDOWN = float(_get("NOTIFY_COOLDOWN", "30.0"))

# --- Visión por computadora ---
CAMERA_INDEX = int(_get("CAMERA_INDEX", "0"))
INFER_EVERY = int(_get("INFER_EVERY", "3"))       # clasificar 1 de cada N cuadros
EAR_THRESHOLD = float(_get("EAR_THRESHOLD", "0.21"))   # ojos cerrados por debajo de esto
YAW_THRESHOLD = float(_get("YAW_THRESHOLD", "0.35"))   # mirar a un lado

# --- Mensaje de voz ---
VOICE_TEXT = _get("VOICE_TEXT", "Atencion, mantente despierto")

# --- MediaPipe FaceLandmarker (Tasks API) ---
FACE_LANDMARKER_PATH = BASE_DIR / "face_landmarker.task"
FACE_LANDMARKER_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)

# --- Archivos ---
TRIP_FILE = BASE_DIR / "trip.json"
EVENT_IMAGE = BASE_DIR / "last_event.jpg"
