## 🚀 Self-Maintenance Rule (Agent MUST follow every time)
For any new insight, debugging lesson, vibe change, architecture decision, "never do X again", important lesson, or preference that comes up in our conversation:
- Immediately append (or create if missing) a single concise bullet to the "## Evolving Insights & Lessons Learned" section at the bottom of THIS file.
- Keep each bullet short (max 1-2 sentences, actionable).
- Never repeat or rewrite old entries — only add new ones.
- End your response with "✅ AGENTS.md updated with new insight" so I know it happened.
- This rule makes every future chat (even completely fresh sessions) automatically have the latest evolved context without me repeating anything ever.

---

# AGENTS.md — Ruler Project

## Project Overview

**Ruler** is a self-hosted design platform for vibe coding with AI agents. It connects to Penpot (open-source design tool) via MCP (Model Context Protocol), enabling AI agents to read, create, and modify designs — then export them as code.

**Mission:** Build a free, unlimited, self-hosted alternative to Paper.design for AI-assisted design workflows.

**Vision:**
- Free & unlimited (no rate limits)
- Self-hosted with full control
- Open source
- AI-first (MCP-native from day 1)
- Code-native (HTML/CSS foundation)
- More powerful than Paper.design

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.13+ |
| Build | hatchling, uv |
| Server | MCP (Model Context Protocol), uvicorn |
| Database | PostgreSQL (via Penpot) |
| Container | Docker, Docker Compose |
| Key Libraries | asyncpg, httpx, pydantic, websockets |
| Linting | ruff |
| Type Checking | mypy |

## Architecture

```
ruler/
├── src/
│   ├── penpot_mcp/           # Core MCP server (68+ tools)
│   │   ├── server.py         # Entry point
│   │   ├── config.py         # Configuration
│   │   ├── tools/            # Tool implementations
│   │   │   ├── create.py     # Shape creation
│   │   │   ├── modify.py     # Shape modification
│   │   │   ├── export.py     # PNG/SVG export
│   │   │   ├── shapes.py     # Shape operations
│   │   │   ├── text.py       # Text operations
│   │   │   └── ...
│   │   ├── services/         # API, DB, changes
│   │   └── transformers/     # CSS, SVG, layout
│   │
│   └── ruler_ext/            # Ruler customizations
│       ├── jsx_exporter/     # React/Vue/Tailwind export
│       ├── versioning/       # Checkpoint system
│       ├── skills/           # Skill loader
│       └── enhanced_tools/   # Analysis tools
│
├── ruler-skills/             # Skill markdown files
├── docker-compose.*          # Docker configuration
├── Dockerfile                # MCP server image
├── pyproject.toml           # Python package config
└── setup.sh                 # Interactive setup script
```

## Key Workflows

### Design to Code
```python
# 1. Get design
get_shape_details(file_id, page_id, shape_id)

# 2. Export as code
ruler_export_react(file_id, page_id, shape_id)

# 3. Get visual reference
export_frame_png(file_id, page_id, shape_id, scale=2)
```

### Create Design with AI
```python
# 1. Load skill for guidance
ruler_load_skill("create button")

# 2. Create elements
create_frame(file_id, page_id, x=0, y=0, width=100, height=40, name="Button")
create_text(file_id, page_id, text="Click Me", ...)

# 3. Export result
export_frame_png(...)
```

### Version Control
```python
# Before making changes
ruler_auto_checkpoint(file_id, ai_prompt="Change button color")

# Make changes
set_fill(file_id, page_id, shape_id, color="#FF0000")

# If unhappy, restore
ruler_restore_checkpoint(checkpoint_id)
```

## Commands

### Development
| Command | Description |
|---------|-------------|
| `./setup.sh` | Interactive Docker setup (Penpot + MCP) |
| `./setup.sh --resume` | Resume after cloud instance wake (no prompts) |
| `python -m penpot_mcp.server` | Run MCP server locally |
| `pip install -e .` | Install package in editable mode |

### Docker
| Command | Description |
|---------|-------------|
| `docker compose -p penpot -f docker-compose.yaml up -d` | Start Penpot (preserves data) |
| `docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml up -d --build penpot-mcp` | Build & start MCP |
| `docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml restart penpot-mcp` | Restart MCP |
| `docker compose -p penpot -f docker-compose.yaml down` | Stop containers (preserves data) |
| `docker logs penpot-mcp` | View MCP logs |
| `docker logs -f penpot-mcp` | Follow MCP logs live |

### Code Quality
| Command | Description |
|---------|-------------|
| `ruff check .` | Lint code |
| `ruff check . --fix` | Fix lint issues |
| `mypy src/` | Type check |

## Important Patterns

### Penpot Quirk: Font Properties as Strings
Font properties must be **strings**, not integers:
```python
# Correct
create_text(file_id, page_id, text="Hello", font_size="16", font_weight="400")

# Wrong
create_text(file_id, page_id, text="Hello", font_size=16, font_weight=400)
```

### Default Values
- Default font family: `sourcesanspro` (not Inter)
- Font sizes should be strings: `"16"`, `"24"`, etc.

### IDs
- All IDs are UUIDs (e.g., `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`)
- Use `list_projects()` → get project UUID
- Use `list_files(project_id="<uuid>")` → get file UUID
- Use `get_file_pages(file_id="<uuid>")` → get page UUIDs

### Naming
- Use clear, descriptive names for shapes
- This helps AI understand the design

## Available Skills

| Trigger | Description |
|---------|-------------|
| "create a button" | Button component patterns |
| "create a frame" | Frame/artboard creation |
| "build a page" | Full page workflow |
| "design to code" | Export workflow |
| "naming" | Best practices |

Use: `ruler_load_skill("<task>")` to load guidance.

## MCP Configuration

### OpenCode
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ruler": {
      "type": "remote",
      "url": "http://localhost:8787/mcp",
      "enabled": true
    }
  }
}
```

### Claude Code
```json
{
  "mcpServers": {
    "ruler": {
      "type": "http",
      "url": "http://localhost:8787/mcp"
    }
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PENPOT_BASE_URL` | `http://penpot-frontend:8080` | Internal Penpot URL |
| `PENPOT_PUBLIC_URL` | `http://localhost:9001` | Public URL |
| `PENPOT_ACCESS_TOKEN` | - | API access token |
| `PENPOT_EMAIL` | - | Email for credential auth |
| `PENPOT_PASSWORD` | - | Password for credential auth |
| `PENPOT_DB_HOST` | `penpot-postgres` | PostgreSQL host |
| `MCP_PORT` | `8787` | MCP server port |
| `MCP_LOG_LEVEL` | `info` | Debug logging |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized on get-file | Set `PENPOT_BACKEND_URL=http://penpot-backend:6060` in .env |
| export_frame_png fails 400 | Check penpot-exporter container is running |
| MCP not found | Check MCP server: `docker ps | grep penpot-mcp` |
| MCP container not starting | Run build: `docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml up -d --build penpot-mcp` |
| Connection refused | Ensure port 8787 is open in firewall |
| Account data lost after rebuild | Use `docker compose down` WITHOUT `-v` flag - see below |
| Duplicate PENPOT_FLAGS in .env | Edit .env, keep only one PENPOT_FLAGS line |

## Docker Commands (Data Safety)

### Safe Commands (Preserve Data)
```bash
# Start containers
docker compose -p penpot -f docker-compose.yaml up -d

# Restart containers
docker compose -p penpot -f docker-compose.yaml restart

# Rebuild MCP only
docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml up -d --build penpot-mcp

# Stop containers (preserves volumes)
docker compose -p penpot -f docker-compose.yaml down
```

### Unsafe Commands (Delete ALL Data)
```bash
# ❌ WRONG - Deletes PostgreSQL database volume (ALL USER DATA)
docker compose -p penpot -f docker-compose.yaml down -v

# ❌ WRONG - Also deletes volumes
docker compose -p penpot -f docker-compose.yaml down --volumes
```

### Verify Volumes Exist
```bash
docker volume ls | grep penpot
# Expected: penpot_penpot_postgres_v15, penpot_penpot_assets
```

## Evolving Insights & Lessons Learned

- Never use `docker compose down -v` or `--volumes` flag - it deletes all Docker volumes including the PostgreSQL database, causing permanent data loss. Use `docker compose down` (without -v) to preserve data.
