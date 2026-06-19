@echo off
setlocal enabledelayedexpansion

REM FiftyOne Docs Navigator — Windows launcher
REM Creates venv, installs deps, downloads docs if needed, then runs the MCP server.

if not exist "venv\Scripts\python.exe" (
    echo [setup] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [error] Failed to create virtual environment. Make sure Python 3.12+ is installed and in PATH.
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo [setup] Installing dependencies...
venv\Scripts\python.exe -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [error] Failed to install dependencies.
    exit /b 1
)

if not exist "index.json" (
    echo [setup] Downloading FiftyOne documentation...
    venv\Scripts\python.exe download_docs.py
    if errorlevel 1 (
        echo [error] Failed to download documentation.
        exit /b 1
    )
)

echo [run] Starting FiftyOne Docs Navigator MCP server...
venv\Scripts\python.exe server.py
