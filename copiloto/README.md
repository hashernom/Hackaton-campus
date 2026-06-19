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

**Opción A — script automático (recomendado):**
```powershell
# Desde la raíz del repo:
.\copiloto\install.ps1
```
El script crea el venv, instala todo y corrige automáticamente el conflicto de OpenCV.

**Opción B — manual paso a paso:**
```powershell
python -m venv copiloto\venv
copiloto\venv\Scripts\python.exe -m pip install --upgrade pip
copiloto\venv\Scripts\pip.exe install pillow numpy python-dotenv requests pyttsx3
copiloto\venv\Scripts\pip.exe install mediapipe
copiloto\venv\Scripts\pip.exe install transformers torch
copiloto\venv\Scripts\pip.exe install fiftyone

# IMPORTANTE: fiftyone instala opencv-headless (sin ventana), esto lo corrige:
copiloto\venv\Scripts\pip.exe uninstall opencv-python-headless -y
copiloto\venv\Scripts\pip.exe install --force-reinstall opencv-python
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

# 2a) MODO WEB (navegador) — recomendado para la demo
python copiloto/server.py
#     -> abre http://localhost:5000
#     Solo MediaPipe/EAR (sin torch) y umbrales rápidos:
python copiloto/server.py --no-model --l1 1.0 --l2 3.0

# 2b) MODO ESCRITORIO (ventana OpenCV) — alternativa offline
python copiloto/live_demo.py --l1 1.0 --l2 3.0

# 3) Validar el modelo con FiftyOne (dataset por carpetas de clase)
python copiloto/validate_fiftyone.py --data ruta/al/dataset
```

Salir: **Ctrl+C** (modo web) o tecla **q** (ventana de escritorio).

> ⚠️ El backend toma la cámara: **no** corras `server.py` y `live_demo.py` a la vez.

### Arquitectura del modo web

```
navegador (copiloto/web/index.html, React)
   │  GET /            -> dashboard
   │  GET /api/state   -> estado JSON (polling 300ms)
   │  GET /video_feed  -> stream MJPEG de la cámara
   │  GET /event.jpg   -> captura de la última emergencia
   ▼
Flask (server.py) ──► CopilotoEngine (engine.py, hilo de fondo)
                         cámara → modelo HF + MediaPipe → escalado → notificación
```

El front es el mismo diseño hecho con Claude Design; `getState()` lee del backend.
Para verlo con datos simulados (sin backend), abre `copiloto-dashboard-2.html`
directamente, o pon `DEMO_MODE = true` en `copiloto/web/index.html`.

## Incidencias por foto (QR + VLM + Postgres)

Reporte de anomalías en carretera: el conductor escanea un **QR**, toma una **foto**
desde el móvil, un **modelo VLM zero-shot** reconoce qué pasó y da un **estimado de
demora**, se **guarda** (Postgres o SQLite) y se **avisa al contacto por Telegram**.

```powershell
# (Opcional) levantar Postgres; si no, se usa SQLite automáticamente
docker compose -f copiloto/docker-compose.yml up -d
#  y en .env:  DATABASE_URL=postgresql://copiloto:copiloto@localhost:5432/copiloto

# Arrancar el servidor (escucha en 0.0.0.0 para que el móvil llegue)
python copiloto/server.py
#  Solo incidencias, sin usar la cámara:
python copiloto/server.py --no-engine
```

1. En el dashboard, clic en **“Reportar anomalía (QR)”** → aparece el QR.
2. El conductor lo **escanea** (móvil en la **misma WiFi**) → abre `/report`.
3. Toma la foto + (opcional) escribe el nombre → ve el **tipo** y la **demora estimada**.
4. La incidencia aparece en el **feed del dashboard** y llega el **reporte a Telegram**.

> El móvil y la laptop deben estar en la misma red. Si la red del lugar aísla clientes,
> usa un túnel y pásalo con `--public-url https://xxxx.ngrok.io`.

```
móvil ──QR──► /report ──foto──► POST /api/incident
                                   │  incidents.classify_anomaly (CLIP zero-shot)
                                   │  incidents.estimate_delay   (tipo→minutos)
                                   ├─► db (Postgres/SQLite)
                                   ├─► notifier (Telegram + foto)
                                   └─► feed del dashboard (GET /api/incidents)
```

**Validación + cola de revisión humana (FiftyOne):**
```powershell
# Evaluar el clasificador sobre fotos etiquetadas por carpeta de clase
python copiloto/validate_incidents_fiftyone.py --data ruta/al/dataset
# Revisar las incidencias dudosas (status needs_review) en la App
python copiloto/validate_incidents_fiftyone.py --review
# Confirmar/corregir una incidencia tras revisarla
python copiloto/validate_incidents_fiftyone.py --confirm 12 --as via_cerrada --by despacho
```

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
