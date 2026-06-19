# install.ps1 — Configura el entorno de COPILOTO en Windows
# Ejecutar desde la raiz del repo:
#   .\copiloto\install.ps1

$ErrorActionPreference = "Stop"
$python = "python"

Write-Host "`n==> Creando entorno virtual..." -ForegroundColor Cyan
& $python -m venv copiloto\venv

$pip = "copiloto\venv\Scripts\pip.exe"
$py  = "copiloto\venv\Scripts\python.exe"

Write-Host "`n==> Actualizando pip..." -ForegroundColor Cyan
& $py -m pip install --upgrade pip --quiet

Write-Host "`n==> Instalando capa core..." -ForegroundColor Cyan
& $pip install pillow numpy python-dotenv requests pyttsx3 flask qrcode edge-tts --quiet

Write-Host "`n==> Instalando almacenamiento de incidencias (Postgres / psycopg)..." -ForegroundColor Cyan
& $pip install "psycopg[binary]" --quiet

Write-Host "`n==> Instalando MediaPipe..." -ForegroundColor Cyan
& $pip install mediapipe --quiet

Write-Host "`n==> Instalando modelo HF (torch + transformers)..." -ForegroundColor Cyan
& $pip install transformers torch --quiet

Write-Host "`n==> Instalando FiftyOne (validacion)..." -ForegroundColor Cyan
& $pip install fiftyone --quiet

# fiftyone instala opencv-python-headless (sin GUI), lo reemplazamos por la version completa
Write-Host "`n==> Corrigiendo OpenCV (fiftyone instala headless, necesitamos GUI)..." -ForegroundColor Yellow
& $pip uninstall opencv-python-headless -y 2>$null
& $pip install --force-reinstall opencv-python --quiet

Write-Host "`n==> Verificando imports..." -ForegroundColor Cyan
& $py -c "import cv2, mediapipe, transformers, pyttsx3, flask; print('  cv2:', cv2.__version__); print('  Todo OK')"

Write-Host "`n[OK] Instalacion completa. Ahora puedes ejecutar:" -ForegroundColor Green
Write-Host "  copiloto\venv\Scripts\python.exe copiloto\trip.py --driver `"Tu Nombre`" --contact `"Contacto:`""
Write-Host "`n  Modo web (navegador):"
Write-Host "  copiloto\venv\Scripts\python.exe copiloto\server.py --l1 1.0 --l2 3.0"
Write-Host "  -> abre http://localhost:5000"
Write-Host "`n  Modo escritorio (ventana OpenCV):"
Write-Host "  copiloto\venv\Scripts\python.exe copiloto\live_demo.py --l1 1.0 --l2 3.0"
