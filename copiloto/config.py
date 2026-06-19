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
# Voz neural en español para edge-tts (online). Alternativas: es-ES-AlvaroNeural,
# es-MX-JorgeNeural, es-ES-ElviraNeural.
VOICE_EDGE = _get("VOICE_EDGE", "es-MX-DaliaNeural")

# --- MediaPipe FaceLandmarker (Tasks API) ---
FACE_LANDMARKER_PATH = BASE_DIR / "face_landmarker.task"
FACE_LANDMARKER_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)

# --- Archivos ---
TRIP_FILE = BASE_DIR / "trip.json"
EVENT_IMAGE = BASE_DIR / "last_event.jpg"

# =====================================================================
# Incidencias por foto (VLM zero-shot) + estimación de demora
# =====================================================================

# Modelo zero-shot para clasificar la anomalía (CLIP trae preprocesador completo,
# así que el pipeline de transformers funciona directo).
INCIDENT_MODEL = _get("INCIDENT_MODEL", "openai/clip-vit-base-patch32")

# ¿Usar el modelo de IA para analizar la foto? Por defecto SÍ. El modelo se
# pre-carga al arrancar el servidor (warm-up) para que la primera foto no cuelgue
# la petición. El nombre que escriba el conductor puede corregir el tipo detectado.
INCIDENT_USE_MODEL = _get("INCIDENT_USE_MODEL", "true").lower() in ("1", "true", "yes")

# Taxonomía CERRADA de anomalías (clasificación fiable y evaluable).
TAXONOMY = [
    "accidente",
    "via_cerrada",
    "derrumbe",
    "ponchadura",
    "falla_mecanica",
    "reten_policial",
    "manifestacion",
    "inundacion",
    "clima_extremo",
    "sin_anomalia",
]

# Etiquetas legibles para la UI y los prompts del modelo zero-shot.
TAXONOMY_LABELS = {
    "accidente": "accidente de tránsito",
    "via_cerrada": "vía cerrada o bloqueada",
    "derrumbe": "derrumbe en la carretera",
    "ponchadura": "llanta ponchada",
    "falla_mecanica": "falla mecánica del vehículo",
    "reten_policial": "retén policial o control",
    "manifestacion": "manifestación o protesta",
    "inundacion": "inundación en la vía",
    "clima_extremo": "clima extremo (niebla, tormenta)",
    "sin_anomalia": "carretera normal sin anomalía",
}

# Estimado de demora por tipo (minutos). Configurable.
DELAY_ESTIMATES = {
    "accidente": 90,
    "via_cerrada": 120,
    "derrumbe": 180,
    "ponchadura": 40,
    "falla_mecanica": 60,
    "reten_policial": 20,
    "manifestacion": 60,
    "inundacion": 120,
    "clima_extremo": 45,
    "sin_anomalia": 0,
}

# Confianza mínima para reportar automáticamente; por debajo va a revisión humana.
INCIDENT_CONF_THRESHOLD = float(_get("INCIDENT_CONF_THRESHOLD", "0.45"))

# Carpeta donde se guardan las fotos de incidencias.
INCIDENTS_DIR = BASE_DIR / "incidents"

# --- Postgres ---
# Si no se define DATABASE_URL, db.py cae a SQLite local (copiloto/incidents.db)
# para que la demo funcione sin Docker.
DATABASE_URL = _get("DATABASE_URL", "")
SQLITE_FALLBACK = BASE_DIR / "incidents.db"

# URL pública del servidor para el QR (si se usa túnel ngrok, etc.).
# Vacío = se auto-detecta la IP LAN.
PUBLIC_URL = _get("PUBLIC_URL", "")
