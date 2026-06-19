#!/usr/bin/env bash
set -e

# FiftyOne Docs Navigator — Linux/macOS launcher
# Creates venv, installs deps, downloads docs if needed, then runs the MCP server.

PYTHON=${PYTHON:-python3}

if [ ! -d "venv" ]; then
    echo "[setup] Creating virtual environment..."
    "$PYTHON" -m venv venv
fi

echo "[setup] Activating virtual environment..."
source venv/bin/activate

echo "[setup] Installing dependencies..."
pip install -q -r requirements.txt

if [ ! -f "index.json" ]; then
    echo "[setup] Downloading FiftyOne documentation..."
    python download_docs.py
fi

echo "[run] Starting FiftyOne Docs Navigator MCP server..."
python server.py
