# FiftyOne Docs Navigator MCP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local MCP server that serves pre-downloaded FiftyOne documentation offline via 4 searchable tools.

**Architecture:** A Python FastMCP server reads from a local `docs/` directory and `index.json`. A standalone `download_docs.py` script fetches ~50 key docs pages from docs.voxel51.com, converts them to Markdown, and builds the index. The server exposes `list_topics`, `get_doc`, `search_docs`, and `get_snippet`.

**Tech Stack:** Python 3.10+, `mcp` (FastMCP), `requests`, `beautifulsoup4`, `html2text`

---

## File Structure

```
mcp-fiftyone-docs/
├── server.py              # FastMCP server (4 tools)
├── download_docs.py       # One-time crawl + index builder
├── docs/                  # Markdown documentation (created by download_docs.py)
├── index.json             # Searchable index (created by download_docs.py)
├── requirements.txt       # Python dependencies
└── README.md              # Setup & connection instructions
```

---

## Task 1: Create requirements.txt

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: Write requirements**

```text
mcp>=1.6.0
requests>=2.32.0
beautifulsoup4>=4.12.0
html2text>=2024.2.26
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All packages install without errors.

---

## Task 2: Build download_docs.py

**Files:**
- Create: `download_docs.py`

- [ ] **Step 1: Write the complete downloader script**

```python
"""download_docs.py — Download key FiftyOne docs and build a local search index."""
import json
import os
import re
import textwrap
from pathlib import Path
from urllib.parse import urljoin, urlparse

import html2text
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://docs.voxel51.com"
DOCS_DIR = Path("docs")
INDEX_FILE = Path("index.json")
CHAR_LIMIT = 25_000

# Key docs to download (extracted from the official docs sidebar)
URL_PATHS = [
    # Getting Started
    "getting_started/index.html",
    "getting_started/object_detection/index.html",
    "getting_started/object_detection/01_loading_datasets.html",
    "getting_started/object_detection/02_adding_detections.html",
    "getting_started/object_detection/03_finding_mistakes.html",
    "getting_started/object_detection/04_evaluating_detections.html",
    "getting_started/segmentation/index.html",
    "getting_started/segmentation/01_intro.html",
    "getting_started/segmentation/02_explore.html",
    "getting_started/segmentation/03_sam2.html",
    "getting_started/annotation/index.html",
    "getting_started/annotation/01_quickstart.html",
    "getting_started/annotation/04_annotation_2d.html",
    "getting_started/annotation/05_annotation_3d.html",
    "getting_started/depth_estimation/index.html",
    "getting_started/depth_estimation/01_loading_depth_data.html",
    "getting_started/depth_estimation/02_depth_estimation.html",
    "getting_started/model_evaluation/index.html",
    "getting_started/model_evaluation/01_basic_evaluation.html",
    "getting_started/model_evaluation/02_advanced_analysis.html",
    "getting_started/threed_visual_ai/index.html",
    "getting_started/threed_visual_ai/01_getting_started_3d.html",
    "getting_started/threed_visual_ai/02_loading_annotations.html",
    "getting_started/medical_imaging/index.html",
    "getting_started/medical_imaging/01_getting_started.html",
    # Tutorials
    "tutorials/index.html",
    "tutorials/evaluate_detections.html",
    "tutorials/evaluate_classifications.html",
    "tutorials/image_embeddings.html",
    "tutorials/cvat_annotation.html",
    "tutorials/labelbox_annotation.html",
    "tutorials/detectron2.html",
    "tutorials/uniqueness.html",
    "tutorials/classification_mistakes.html",
    "tutorials/detection_mistakes.html",
    "tutorials/clustering.html",
    "tutorials/anomaly_detection.html",
    "tutorials/zero_shot_classification.html",
    "tutorials/dinov3.html",
    "tutorials/yolov8.html",
    "tutorials/data_augmentation.html",
    # Recipes
    "recipes/index.html",
    "recipes/creating_views.html",
    "recipes/adding_detections.html",
    "recipes/adding_classifications.html",
    "recipes/convert_datasets.html",
    "recipes/merge_datasets.html",
    "recipes/custom_importer.html",
    "recipes/custom_exporter.html",
    "recipes/image_deduplication.html",
    "recipes/remove_duplicate_annos.html",
    # Cheat Sheets
    "cheat_sheets/index.html",
    "cheat_sheets/filtering_cheat_sheet.html",
    "cheat_sheets/views_cheat_sheet.html",
    "cheat_sheets/pandas_vs_fiftyone.html",
    # User Guide
    "user_guide/index.html",
    "user_guide/basics.html",
    "user_guide/import_datasets.html",
    "user_guide/using_datasets.html",
    "user_guide/using_views.html",
    "user_guide/evaluation.html",
    "user_guide/annotation.html",
    "user_guide/app.html",
    "user_guide/export_datasets.html",
    "user_guide/using_aggregations.html",
    # Brain / Zoo / Integrations
    "brain.html",
    "dataset_zoo/overview.html",
    "model_zoo/overview.html",
    "integrations/coco.html",
    "integrations/ultralytics.html",
    "integrations/huggingface.html",
    "integrations/cvat.html",
    "cli/index.html",
]


def fetch_page(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Remove nav / header / footer noise
    for selector in ["nav", "header", "footer", "#sidebar", ".toc"]:
        for tag in soup.select(selector):
            tag.decompose()
    # Prefer main content area
    main = soup.find("main") or soup.find("div", class_=re.compile("main|content|document")) or soup.find("body")
    if not main:
        main = soup
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    return h.handle(str(main))


def save_doc(path: str, markdown: str) -> Path:
    relative = path.replace(".html", ".md")
    out_path = DOCS_DIR / relative
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    return out_path


def build_index() -> list[dict]:
    index = []
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        rel_path = str(md_file.relative_to(DOCS_DIR)).replace("\\", "/")
        # Derive title from first H1
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else rel_path
        index.append({
            "path": rel_path,
            "title": title,
            "category": rel_path.split("/")[0],
            "content": content,
        })
    return index


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    print(f"Downloading {len(URL_PATHS)} pages from {BASE_URL} ...")
    for path in URL_PATHS:
        url = urljoin(BASE_URL, path)
        try:
            html = fetch_page(url)
            md = html_to_markdown(html)
            out = save_doc(path, md)
            print(f"  ✓ {out}")
        except Exception as exc:
            print(f"  ✗ {path}: {exc}")

    print("\nBuilding index.json ...")
    index = build_index()
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ Indexed {len(index)} documents -> {INDEX_FILE}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify syntax**

Run: `python -m py_compile download_docs.py`
Expected: No output (success).

---

## Task 3: Populate local documentation store

**Files:**
- Creates: `docs/` directory tree and `index.json`

- [ ] **Step 1: Run the downloader**

Run: `python download_docs.py`
Expected: ~50 lines of `✓` output, then `Indexed X documents -> index.json`.

- [ ] **Step 2: Verify files exist**

Run: `python -c "import json, pathlib; idx = json.loads(pathlib.Path('index.json').read_text()); print(len(idx), 'docs indexed'); assert any(i['path']=='user_guide/basics.md' for i in idx)"`
Expected: `50 docs indexed` (or similar) and no assertion error.

---

## Task 4: Implement server.py (MCP Server)

**Files:**
- Create: `server.py`

- [ ] **Step 1: Write the MCP server**

```python
"""server.py — FiftyOne Docs Navigator MCP Server (FastMCP)."""
import json
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DOCS_DIR = Path("docs")
INDEX_FILE = Path("index.json")
CHAR_LIMIT = 25_000

# Load index at startup
if not INDEX_FILE.exists():
    raise SystemExit(f"Index not found: {INDEX_FILE}. Run download_docs.py first.")

INDEX = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

server = FastMCP("fiftyone-docs-navigator")


@server.tool()
def list_topics() -> str:
    """List all available documentation topics with name, category, and path.

    Use this when you need to discover what guides, tutorials, recipes,
    or cheat sheets are available in the local FiftyOne documentation.
    """
    lines = ["# Available FiftyOne Documentation\n"]
    for entry in INDEX:
        lines.append(f"- **{entry['title']}** (`{entry['category']}`) → `{entry['path']}`")
    return "\n".join(lines)


@server.tool()
def get_doc(path: str) -> str:
    """Retrieve the full Markdown content of a specific doc by its path.

    Args:
        path: Relative path in the docs directory, e.g. 'user_guide/basics.md'
              or 'getting_started/object_detection/01_loading_datasets.md'.
    """
    file_path = DOCS_DIR / path
    if not file_path.exists():
        available = [e["path"] for e in INDEX if path in e["path"]]
        hint = f" Did you mean one of: {available[:3]}?" if available else ""
        return f"Error: Document not found at `{path}`.{hint} Use list_topics() to see available docs."

    content = file_path.read_text(encoding="utf-8")
    if len(content) > CHAR_LIMIT:
        content = content[:CHAR_LIMIT] + f"\n\n... [truncated, {len(content)} chars total]"
    return content


@server.tool()
def search_docs(query: str, max_results: int = 5) -> str:
    """Search the full documentation for a keyword or phrase.

    Args:
        query: Keyword or phrase to search for (case-insensitive).
        max_results: Maximum number of matching documents to return (default 5).
    """
    query_lower = query.lower()
    scored = []
    for entry in INDEX:
        score = 0
        if query_lower in entry["title"].lower():
            score += 10
        content_lower = entry["content"].lower()
        occurrences = content_lower.count(query_lower)
        score += occurrences
        if score > 0:
            scored.append((score, entry))

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:max_results]

    if not top:
        return f"No matches found for '{query}'. Try broadening your query or check list_topics()."

    lines = [f"# Search Results for '{query}'\n"]
    for score, entry in top:
        excerpt = _extract_excerpt(entry["content"], query)
        lines.append(f"## {entry['title']} (`{entry['path']}`) — score {score}\n")
        lines.append(excerpt + "\n")
    return "\n".join(lines)


@server.tool()
def get_snippet(topic: str, max_snippets: int = 3) -> str:
    """Extract Python code snippets related to a topic.

    Args:
        topic: Keyword describing what you need, e.g. 'load COCO dataset' or 'evaluate detections'.
        max_snippets: Maximum number of code blocks to return (default 3).
    """
    topic_lower = topic.lower()
    matches = []
    for entry in INDEX:
        content = entry["content"]
        # Find all fenced code blocks
        code_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
        for block in code_blocks:
            if topic_lower in block.lower() or topic_lower in entry["title"].lower():
                matches.append((entry["title"], entry["path"], block.strip()))

    if not matches:
        return f"No Python snippets found for '{topic}'. Try a broader term or use search_docs()."

    lines = [f"# Python Snippets for '{topic}'\n"]
    for title, path, snippet in matches[:max_snippets]:
        lines.append(f"## From: {title} (`{path}`)\n")
        lines.append(f"```python\n{snippet}\n```\n")
    return "\n".join(lines)


def _extract_excerpt(content: str, query: str, radius: int = 200) -> str:
    """Return a short excerpt around the first query occurrence."""
    idx = content.lower().find(query.lower())
    if idx == -1:
        return content[:300] + "..."
    start = max(0, idx - radius)
    end = min(len(content), idx + radius)
    excerpt = content[start:end]
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(content):
        excerpt = excerpt + "..."
    return excerpt


if __name__ == "__main__":
    server.run()
```

- [ ] **Step 2: Verify syntax**

Run: `python -m py_compile server.py`
Expected: No output (success).

- [ ] **Step 3: Verify imports load**

Run: `python -c "from server import server, list_topics, get_doc, search_docs, get_snippet; print('Imports OK')"`
Expected: `Imports OK` (server will not start because `__main__` is not executed).

---

## Task 5: Smoke-test the server via evaluation harness

**Files:**
- Test: manual / evaluation harness

- [ ] **Step 1: Quick functional test via Python import**

Run:
```python
python -c "
from server import list_topics, get_doc, search_docs, get_snippet
print(list_topics()[:300])
print('---')
print(get_doc('user_guide/basics.md')[:300])
print('---')
print(search_docs('dataset', max_results=2)[:300])
print('---')
print(get_snippet('load dataset', max_snippets=1)[:300])
"
```
Expected: Markdown output for each tool with no exceptions.

- [ ] **Step 2: (Optional) Test stdio transport startup**

Run the server in a background terminal / tmux:
`python server.py`

Then send a JSON-RPC initialize request via stdin (or use the MCP Inspector if available). The server should respond with capabilities.

---

## Task 6: Write README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README**

```markdown
# FiftyOne Docs Navigator — MCP Server

Local MCP server that serves FiftyOne documentation offline. Built for AI-assisted hackathons.

## Quick Start

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Download documentation (one-time)
   ```bash
   python download_docs.py
   ```

3. Run the MCP server
   ```bash
   python server.py
   ```

## Connecting to your AI Agent

### Cursor
Add to `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "fiftyone-docs": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-fiftyone-docs/server.py"]
    }
  }
}
```

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "fiftyone-docs": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-fiftyone-docs/server.py"]
    }
  }
}
```

### OpenCode / Other
Any MCP client using stdio transport can connect by running `python server.py`.

## Tools

- `list_topics()` — See all available docs.
- `get_doc(path)` — Read a full guide/tutorial.
- `search_docs(query, max_results=5)` — Full-text search.
- `get_snippet(topic, max_snippets=3)` — Get Python code examples.

## Notes
- All docs are stored locally in `docs/`; no internet required after download.
- Responses are truncated to ~25k characters to respect context windows.
```

---

## Spec Coverage Check

| Spec Requirement | Plan Task |
|---|---|
| Local doc store (`docs/` + `index.json`) | Task 2 (script), Task 3 (execution) |
| Tool: `list_topics` | Task 4 |
| Tool: `get_doc` | Task 4 |
| Tool: `search_docs` | Task 4 |
| Tool: `get_snippet` | Task 4 |
| Markdown responses + truncation | Task 4 (`CHAR_LIMIT`) |
| Read-only, offline, no secrets | Task 4 (local file reads only) |
| README with connection instructions | Task 6 |

## Placeholder Scan

- No TBD / TODO / "implement later" found.
- All steps include exact file paths, exact code, and exact commands.
- Types and function names are consistent across tasks.

---

*Plan ready for execution.*
