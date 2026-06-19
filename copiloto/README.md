# COPILOTO — Ángel guardián para conductores que viajan solos

Asistente de seguridad vial **en tiempo real**. Vigila al conductor por webcam,
detecta **somnolencia / distracción** y, si no reacciona, **avisa a un contacto
de emergencia** por Telegram con una foto del momento.

> Reto 1 del hackathon (Transporte Inteligente y Seguridad Vial — COPILOTO).

## Arquitectura

```
webcam ──► modelo HF de somnolencia (transformers)   ─┐
       └─► MediaPipe FaceMesh (EAR + mirada)          ─┴─► escalado ──► voz + banner
                                                                   └─► Telegram (foto) al contacto
```

- **Modelo de IA (Hugging Face):** [`chbh7051/driver-drowsiness-detection`](https://huggingface.co/chbh7051/driver-drowsiness-detection) (ViT, etiquetas `drowsy` / `notdrowsy`)
- **Distracción / plan B:** MediaPipe FaceMesh (EAR = ojos cerrados, yaw = mirada fuera de la vía)
- **Voz:** `pyttsx3` (offline)
- **Notificación:** Telegram Bot API
- **Validación del modelo:** FiftyOne (`validate_fiftyone.py`)

## Instalación (Windows / PowerShell)

> **Nota Python 3.14:** `torch`, `mediapipe` y `fiftyone` pueden no tener wheels
> para 3.14 todavía. Si la instalación completa falla, usa la **capa core +
> mediapipe** y corre con `--no-model` (somnolencia por EAR, sin torch).

```powershell
python -m venv copiloto/venv
copiloto/venv/Scripts/Activate.ps1
python -m pip install --upgrade pip

# Capa core (siempre)
pip install opencv-python pillow numpy python-dotenv requests pyttsx3
# Detección facial (somnolencia EAR + distracción)
pip install mediapipe
# Modelo HF (si hay wheels para tu Python)
pip install transformers torch
# Validación
pip install fiftyone
```

## Configuración de Telegram

1. En Telegram, habla con **@BotFather** → `/newbot` → copia el **token**.
2. Escríbele un mensaje a tu nuevo bot.
3. Abre `https://api.telegram.org/bot<TOKEN>/getUpdates` y copia tu **chat_id**.
4. Copia `.env.example` a `.env` y rellena `TELEGRAM_BOT_TOKEN` y `DEFAULT_CHAT_ID`.
5. Prueba: `python copiloto/notifier.py`

## Uso

```powershell
# 1) Registrar el viaje y el contacto de emergencia
python copiloto/trip.py --driver "Juan Perez" --contact "Mama:123456789"

# 2) Arrancar el copiloto en vivo
python copiloto/live_demo.py
#    Solo MediaPipe/EAR (sin torch):
python copiloto/live_demo.py --no-model
#    Ajustes de demo (dispara más rápido):
python copiloto/live_demo.py --l1 1.0 --l2 3.0

# 3) Validar el modelo con FiftyOne (dataset por carpetas de clase)
python copiloto/validate_fiftyone.py --data ruta/al/dataset
```

Salir de la ventana en vivo: tecla **q**.

## Guion de demo (el "momento mágico")

1. Registras el viaje con el celular de un compañero como contacto.
2. Cara normal → banner **VERDE**.
3. Cierras los ojos → **ROJO** + **voz**: "Atención, mantente despierto".
4. No reaccionas → el **celular del compañero suena** con la **foto**.
   Cierre: *"cuando viajas solo, alguien se entera."*

## Niveles de escalado

| Nivel | Disparo | Acción |
|------|---------|--------|
| 0 | sin riesgo | OK (verde) |
| 1 | riesgo ≥ `LEVEL1_SECS` | voz + banner rojo |
| 2 | riesgo ≥ `LEVEL2_SECS` (no se recupera) | notificación Telegram + foto |

Umbrales y modelo se ajustan por `.env` (ver `.env.example`).
