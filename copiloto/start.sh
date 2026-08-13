#!/usr/bin/env bash
# Arranca COPILOTO: crea el venv si falta, registra el viaje si falta,
# y levanta el servidor web.
#
# Uso:
#   ./start.sh                 -> modo normal (con cámara)
#   ./start.sh --demo          -> sin cámara, solo dashboard/incidencias (--no-engine)
#   ./start.sh --driver "Ana" --contact "Mama:123456789"   -> registra/actualiza el viaje
#   Cualquier otro flag se reenvía tal cual a server.py (--port, --host, --l1, --l2, ...)

set -euo pipefail
cd "$(dirname "$0")"

VENV_PY="venv/bin/python"

if [ ! -x "$VENV_PY" ]; then
  echo "[start] No existe el venv, creándolo..."
  python3 -m venv venv
  venv/bin/pip install --upgrade pip -q
  venv/bin/pip install -r requirements.txt
fi

if [ ! -f ".env" ]; then
  echo "[start] Copiando .env.example -> .env (rellénalo con tu token de Telegram si lo usas)"
  cp .env.example .env
fi

DRIVER=""
CONTACTS=()
SERVER_ARGS=()
DEMO=0

while [ $# -gt 0 ]; do
  case "$1" in
    --demo)
      DEMO=1
      shift
      ;;
    --driver)
      DRIVER="$2"
      shift 2
      ;;
    --contact)
      CONTACTS+=("--contact" "$2")
      shift 2
      ;;
    *)
      SERVER_ARGS+=("$1")
      shift
      ;;
  esac
done

if [ -n "$DRIVER" ]; then
  "$VENV_PY" trip.py --driver "$DRIVER" "${CONTACTS[@]}"
elif [ ! -f "trip.json" ]; then
  echo "[start] No hay viaje registrado, usando valores por defecto (config.py / .env)."
  echo "[start] Para registrar uno: ./start.sh --driver \"Tu Nombre\" --contact \"Contacto:chat_id\""
fi

if [ "$DEMO" -eq 1 ]; then
  SERVER_ARGS+=("--no-engine")
fi

echo "[start] Arrancando servidor..."
exec "$VENV_PY" server.py "${SERVER_ARGS[@]}"
