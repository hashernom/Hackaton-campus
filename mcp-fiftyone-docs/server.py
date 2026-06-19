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
        lines.append(f"- **{entry['title']}** (`{entry['category']}`) -> `{entry['path']}`")
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
        # 1. Fenced code blocks (```python ... ```)
        code_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
        # 2. Indented code blocks (4+ spaces, common in Jupyter-converted docs)
        indented_blocks = re.findall(r"(?:\n|\A)(?:    .*(?:\n|$))+", content)
        all_blocks = code_blocks + indented_blocks
        for block in all_blocks:
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
