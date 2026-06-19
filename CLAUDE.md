# FiftyOneHackaton

Proyecto de hackathon centrado en **FiftyOne** (herramienta de gestión y análisis de datasets de visión por computadora).

## MCP disponible: `fiftyone-docs`

Este proyecto tiene configurado un servidor MCP local que sirve la documentación de FiftyOne **offline**. Está definido en [.mcp.json](.mcp.json) y arranca con el venv en `mcp-fiftyone-docs/venv/`.

Úsalo siempre que necesites consultar cómo hacer algo en FiftyOne en vez de improvisar desde memoria.

### Herramientas
- `list_topics()` — lista los 73 documentos disponibles (guías, tutoriales, recipes, cheat sheets).
- `get_doc(path)` — lee un documento completo, p. ej. `get_doc("user_guide/basics.md")`.
- `search_docs(query, max_results=5)` — búsqueda de texto completo en toda la documentación.
- `get_snippet(topic, max_snippets=3)` — extrae ejemplos de código Python sobre un tema.

### Notas operativas
- El servidor es stdio (Python 3.14, FastMCP). Vive en `mcp-fiftyone-docs/`, autocontenido (incluye `docs/` e `index.json`).
- `server.py` ancla sus rutas a la ubicación del archivo (`Path(__file__).parent`), así que no depende del directorio de arranque.
- Las respuestas se truncan a ~25k caracteres para respetar el contexto.
- Si el MCP no aparece, ejecuta `/mcp` para ver su estado; la primera vez Claude Code pide aprobar el servidor MCP del proyecto.

## Estructura
```
FiftyOneHackaton/
├── .mcp.json              # Config del MCP (project-scoped)
├── CLAUDE.md              # Este archivo
└── mcp-fiftyone-docs/     # Servidor MCP de documentación FiftyOne
    ├── server.py
    ├── docs/              # ~73 docs en Markdown
    ├── index.json
    └── venv/              # Entorno virtual con dependencias
```
