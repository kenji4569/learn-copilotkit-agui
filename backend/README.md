# Backend with AG-UI

FastAPI backend using AG-UI without an LLM adapter, directly utilizing AG-UI features.

## Getting Started

```bash
uv sync
uv run uvicorn main:app --reload
```

The server will start at http://localhost:8000

### Quality Checks

```bash
uv run ruff check
uv run pyright
uv run pytest -v
```

## Directory Structure

```
backend/
├── src/
│   └── features/
│       └── agent/           # Agent-related features
│           ├── router.py    # **FastAPI router; returns simple responses based on AG-UI**
│           └── utils/
│               └── sse.py   # Server-Sent Events utilities
├── main.py                  # Application entry point
...
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **AG-UI** - Agent interface framework (no LLM adapter)

### Development Tools
- **ruff** - Linter/Formatter
- **pyright** - Type checker
- **pytest** - Testing framework
