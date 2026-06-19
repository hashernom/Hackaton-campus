# FiftyOne Docs Navigator — MCP Server

Local MCP server that serves FiftyOne documentation offline. Built for AI-assisted hackathons.

## Quick Start

### Windows

1. Open a terminal in this folder (`mcp-fiftyone-docs/`).
2. Run:
   ```batch
   run.bat
   ```

### Linux / macOS

1. Open a terminal in this folder.
2. Make the script executable (only once):
   ```bash
   chmod +x run.sh
   ```
3. Run:
   ```bash
   ./run.sh
   ```

### What `run.bat` / `run.sh` does

1. Creates a local Python virtual environment (`venv/`).
2. Installs dependencies from `requirements.txt`.
3. Downloads FiftyOne docs with `download_docs.py` if `index.json` is missing.
4. Starts the MCP server.

All subsequent runs are instantaneous because the venv and docs are already there.

---

## Manual Setup (if you prefer)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
python download_docs.py   # one-time
python server.py
```

---

## Connecting to OpenCode

Add this to your OpenCode config:

### Windows

Global config: `%USERPROFILE%\.config\opencode\opencode.jsonc`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "fiftyone-docs": {
      "type": "local",
      "command": ["run.bat"],
      "cwd": "C:\\Users\\santiafanador\\Desktop\\Hackaton\\mcp-fiftyone-docs",
      "enabled": true
    }
  }
}
```

### Linux / macOS

Global config: `~/.config/opencode/opencode.jsonc`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "fiftyone-docs": {
      "type": "local",
      "command": ["./run.sh"],
      "cwd": "/home/tu_usuario/ruta/a/mcp-fiftyone-docs",
      "enabled": true
    }
  }
}
```

> **Tip:** You can also place the config in `.opencode/opencode.json` inside your hackathon project folder for per-project setup.

---

## Migrating to Another PC

### Option A: Copy everything (recommended for hackathons)

1. Copy the entire `mcp-fiftyone-docs/` folder to the new PC.
2. Run `run.bat` (Windows) or `./run.sh` (Linux/macOS).
3. The script creates the venv and installs dependencies automatically. Docs are already included, so it works offline immediately.

### Option B: Copy only the scripts

1. Copy `server.py`, `download_docs.py`, `requirements.txt`, `run.bat`, `run.sh`, `README.md`.
2. Run the launcher script.
3. It will download the docs from the internet (requires connection once).

---

## Tools

Your AI agent can call:

- `list_topics()` — See all available docs.
- `get_doc(path)` — Read a full guide/tutorial.
- `search_docs(query, max_results=5)` — Full-text search.
- `get_snippet(topic, max_snippets=3)` — Get Python code examples.

### Example prompts

```
¿Cómo cargo un dataset COCO en FiftyOne? usa fiftyone-docs
```

```
Busca en fiftyone-docs cómo evaluar detecciones de objetos
```

```
Dame un snippet de código para entrenar YOLOv8 con FiftyOne usando fiftyone-docs
```

---

## Project Structure

```
mcp-fiftyone-docs/
├── server.py              # MCP server
├── download_docs.py       # One-time doc downloader
├── run.bat                # Windows launcher
├── run.sh                 # Linux/macOS launcher
├── requirements.txt       # Python dependencies
├── docs/                  # Downloaded Markdown docs (~73 files)
├── index.json             # Searchable index
├── .gitignore             # Ignores venv and cache
└── README.md              # This file
```

## Notes

- Requires **Python 3.10+** (Python 3.12 recommended).
- All docs are stored locally in `docs/`; no internet required after download.
- Responses are truncated to ~25k characters to respect context windows.
- Downloaded docs include Getting Started guides, Tutorials, Recipes, Cheat Sheets, User Guide, Brain, Dataset Zoo, Model Zoo, Integrations, and CLI reference.
