# FiftyOne Docs Navigator — MCP Server Design Spec

**Date:** 2026-06-17  
**Status:** Approved by user  
**Goal:** Enable AI-assisted rapid querying of FiftyOne documentation during a hackathon via an MCP server.

---

## 1. Context & Problem

The user is competing in a hackathon on Friday where all work will be AI-assisted. The FiftyOne documentation at `docs.voxel51.com` is large, extensive, and critical for building computer-vision projects. The user needs:
- Fast, offline access to docs (no reliance on spotty event Wi-Fi).
- Direct integration with their AI agent (Cursor, Claude Desktop, OpenCode, etc.).
- Ability to retrieve code snippets, guides, and API reference quickly.

## 2. Solution Overview

A local **MCP (Model Context Protocol) server** written in Python that serves pre-downloaded FiftyOne documentation as searchable tools. The AI agent connects to this server and queries it naturally (e.g., *"How do I evaluate object detections in FiftyOne?"*).

## 3. Architecture

```
┌─────────────────┐      stdio      ┌──────────────────────┐
│   AI Agent      │ ◄──────────────► │  MCP Server (Python) │
│  (Cursor/etc)   │                  │  FastMCP             │
└─────────────────┘                  └──────────────────────┘
                                              │
                                              ▼
                                     ┌──────────────────────┐
                                     │  Local doc store     │
                                     │  - docs/ (Markdown)  │
                                     │  - index.json        │
                                     └──────────────────────┘
```

### 3.1 Tech Stack
- **Language:** Python 3.10+
- **MCP Framework:** `mcp` (FastMCP) via stdio transport
- **Data Format:** Markdown files + JSON index
- **Offline:** All docs downloaded locally before hackathon

## 4. Tools (API Surface)

### 4.1 `list_topics`
**Purpose:** Let the agent discover what documentation is available.  
**Input:** None  
**Output:** JSON array of topics with `name`, `category`, `path`, `description`.  
**Annotations:** `readOnlyHint: true`

### 4.2 `get_doc`
**Purpose:** Retrieve the full content of a specific guide/tutorial.  
**Input:** `path` (string) — relative path from the docs root (e.g., `getting_started/object_detection/01_loading_datasets`).  
**Output:** Full Markdown content (truncated to ~25k chars if needed).  
**Annotations:** `readOnlyHint: true`

### 4.3 `search_docs`
**Purpose:** Full-text keyword search across all downloaded docs.  
**Input:** `query` (string), `max_results` (int, default 5).  
**Output:** List of matching excerpts with `path`, `title`, `excerpt`, `score`.  
**Annotations:** `readOnlyHint: true`

### 4.4 `get_snippet`
**Purpose:** Extract Python code examples related to a topic.  
**Input:** `topic` (string, e.g., "load COCO dataset"), `max_snippets` (int, default 3).  
**Output:** List of code blocks with context.  
**Annotations:** `readOnlyHint: true`

## 5. Data Pipeline

### 5.1 Pre-hackathon (now)
1. **Crawl & download:** Fetch all key docs pages from `docs.voxel51.com` using `webfetch`.
2. **Convert to Markdown:** Store clean Markdown under `docs/<category>/<page>.md`.
3. **Build `index.json`:** Flat index with metadata + searchable text per page.

### 5.2 During hackathon
- Server reads from local `docs/` and `index.json`.
- No network calls required.

## 6. File Structure

```
mcp-fiftyone-docs/
├── server.py              # FastMCP server implementation
├── download_docs.py       # One-time script to fetch and index docs
├── docs/                  # Downloaded documentation (Markdown)
│   ├── getting_started/
│   ├── tutorials/
│   ├── user_guide/
│   ├── recipes/
│   ├── cheat_sheets/
│   └── api/
├── index.json             # Searchable index
├── requirements.txt       # Python dependencies
└── README.md              # How to run the server & connect to agents
```

## 7. Response Formats

- **Default:** Markdown (human-readable, AI-friendly).
- **Truncation:** Hard cap at 25,000 characters per response to respect context windows.
- **Concise mode:** Optional parameter on `search_docs` to return only titles + 2-line excerpts.

## 8. Error Handling

- **Doc not found:** `"No documentation found for path 'X'. Try list_topics() to see available docs."`
- **No search results:** `"No matches found for 'X'. Try broadening your query or check list_topics()."`
- **Index missing:** `"Documentation index not found. Run download_docs.py first."`

## 9. Security & Scope

- **Read-only:** All tools are non-destructive.
- **Local-only:** No external network calls during hackathon.
- **No secrets:** No API keys or authentication needed.

## 10. Success Criteria

- [ ] Agent can list all topics in < 1s.
- [ ] Agent can retrieve any guide by name in < 1s.
- [ ] Agent can search full docs and get relevant results in < 2s.
- [ ] Agent can extract Python code snippets for any common task.
- [ ] Works completely offline after initial download.

## 11. Future Enhancements (Post-hackathon)

- Add `ask_question` tool using RAG + local embeddings (e.g., via sentence-transformers).
- Sync docs on-demand when online.
- Add FiftyOne Brain / Plugins / Enterprise docs.

---

*Approved by user on 2026-06-17. Ready for implementation planning.*
