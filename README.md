# Ruler

**Open-source Paper.design alternative for vibe coding with AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-yellow.svg)](https://python.org)
[![MCP Protocol](https://img.shields.io/badge/MCP-2025--03--26-green.svg)](https://modelcontextprotocol.io)

---

## What is Ruler?

Ruler is a self-hosted design platform built specifically for **vibe coding workflows**. It combines Penpot's powerful open-source design capabilities with custom enhancements tailored for AI-assisted development.

Think of it as: **Paper.design but open-source, self-hosted, and unlimited.**

### Why Ruler?

| Feature | Paper.design | Ruler |
|---------|--------------|-------|
| Rate Limits | 100/week (free) | **Unlimited** |
| Self-Hosted | No | **Yes** |
| Open Source | No | **Yes** |
| MCP Tools | ~20 | **68+** |
| JSX Export | Native | **Custom** |
| Versioning | Basic | **Enhanced** |

---

## Features

### Core (from Penpot MCP)
- **68 MCP Tools** - Full Penpot integration
- **Project Management** - Create, list, search files
- **Shape Operations** - Create, modify, delete shapes
- **Design Tokens** - Extract colors, typography
- **Export** - PNG, SVG export
- **Comments** - Read/write comments

### Ruler Extensions

#### 🎯 Skill System
Pre-built prompts that teach AI agents how to work with Penpot:
- Design basics (frames, shapes, text)
- Component patterns (buttons, inputs, cards)
- Full page workflows
- Best practices

#### 📸 JSX Export
Convert Penpot designs to code:
- React (inline styles)
- React + Tailwind CSS
- Vue
- Svelte
- Plain HTML

#### 🔄 Versioning
AI-friendly version control:
- Named checkpoints
- Auto-snapshot before changes
- Easy rollback
- Version comparison

#### 🧠 Enhanced Tools
Additional AI-powered tools:
- Full design context extraction
- Design token extraction
- Design analysis

### Latest Updates (v0.2.0)

New features added for efficient AI workflows:

- **Batch Creation** - `create_shapes_batch()` creates multiple shapes in 1 API call instead of 50+ individual calls
- **Gradient Support** - Add `gradient_type`, `gradient_stops`, `gradient_angle` to `create_rectangle`, `create_frame`, `create_ellipse`
- **Smart References** - Use shape names instead of UUIDs with `shape_name` param on `move_shape`
- **Component Instances** - `create_component_instance()` places existing components on canvas - perfect for grids
- **SVG Import** - `import_svg()` parses SVG strings into Penpot shapes
- **Auto-Context** - `ruler_set_context()` tracks file_id/page_id across calls to reduce repetition
- **Better Error Messages** - Detailed API errors for easier debugging

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAIN PC (Host)                              │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                     Ruler System                                │ │
│  │                                                                  │ │
│  │  ┌─────────────┐    ┌─────────────────────┐                   │ │
│  │  │   Penpot    │    │    Ruler MCP        │                   │ │
│  │  │  (Docker)   │◄──►│    Server          │                   │ │
│  │  │  :9001      │    │  :8787             │                   │ │
│  │  └─────────────┘    └──────────┬──────────┘                   │ │
│  │                               │                                 │ │
│ ───────────┴───────────┐                     │ │
│  │                    ┌ │                    │   PostgreSQL DB       │                     │ │
│  │                    └───────────────────────┘                     │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                │
                    Network (HTTP/WebSocket)
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                      LAPTOP (Client)                                 │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    AI Agent (Claude Code)                        │ │
│  │                                                                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐   │ │
│  │  │              Ruler Skills                                │   │ │
│  │  │  • "Create a button" → skill loaded                    │   │ │
│  │  │  • "Build a page" → skill loaded                        │   │ │
│  │  └─────────────────────────────────────────────────────────┘   │ │
│  │                              │                                  │ │
│  │                              ▼                                  │ │
│  │  ┌─────────────────────────────────────────────────────────┐   │ │
│  │  │              MCP Client                                 │   │ │
│  │  │  http://<main-pc-ip>:8787/mcp                         │   │ │
│  │  └─────────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.13+ (for local development)
- A Penpot instance (self-hosted or cloud)

### Installation

```bash
# Clone the repository
git clone https://github.com/olakawala/ruler.git
cd ruler

# Install dependencies (for local development)
pip install -e .

# Configure environment
cp .env_example .env
# Edit .env with your Penpot credentials

# Run the MCP server locally (optional - can also use Docker)
python -m penpot_mcp.server
```

### With Docker

```bash
# Use the provided setup script
./setup.sh
```

### With Docker

```bash
# Add to your Penpot docker-compose.yml
# See docker-compose.penpot.yml for reference

# Or use the provided setup
./setup.sh
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PENPOT_BASE_URL` | `http://penpot-frontend:8080` | Internal Penpot URL |
| `PENPOT_BACKEND_URL` | - | Direct backend URL (fixes 401 errors) |
| `PENPOT_PUBLIC_URL` | `http://localhost:9001` | Public URL |
| `PENPOT_ACCESS_TOKEN` | - | API access token |
| `PENPOT_EMAIL` | - | Email for credential auth |
| `PENPOT_PASSWORD` | - | Password for credential auth |
| `PENPOT_DB_HOST` | `penpot-postgres` | PostgreSQL host |
| `MCP_PORT` | `8787` | MCP server port |
| `MCP_LOG_LEVEL` | `info` | Debug logging (debug, info, warning, error) |
| `RULER_SKILLS_PATH` | `./ruler-skills` | Skills directory |

### Penpot Setup

1. Enable access tokens in Penpot:
   ```
   PENPOT_FLAGS=enable-login-with-password enable-registration enable-access-tokens enable-plugins-runtime
   ```
2. Create an access token in Penpot profile settings
3. Add token to your `.env` file

### Managing Ruler MCP

These commands assume your setup uses both `docker-compose.yaml` (Penpot) and `docker-compose.override.yaml` (Ruler MCP).

#### Quick Commands

| Action | Command |
|--------|---------|
| **Rebuild & start** | `docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml up -d --build penpot-mcp` |
| **Restart (no rebuild)** | `docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml restart penpot-mcp` |
| **View logs** | `docker logs penpot-mcp` |
| **Follow logs (live)** | `docker logs -f penpot-mcp` |
| **Check status** | `docker ps \| grep penpot-mcp` |
| **Stop completely** | `docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml stop penpot-mcp` |

#### After Pulling Code Updates

```bash
git pull
docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml up -d --build penpot-mcp
```

**Important**: Always use `--build` after pulling code changes. The Python code is baked into the Docker image, so `restart` alone will NOT pick up new changes.

#### Troubleshooting Commands

```bash
# Check if container is running
docker ps | grep penpot-mcp

# View recent logs
docker logs --tail=50 penpot-mcp

# View live logs while reproducing issue
docker logs -f penpot-mcp

# Restart with fresh logs
docker restart penpot-mcp && docker logs -f penpot-mcp
```

### OpenCode Config Location

OpenCode looks for `opencode.json` in these locations (in order of precedence):

1. **Current directory** (project root) - `./opencode.json`
2. **Parent directories** (up to root) - `../opencode.json`
3. **Global config** - `~/.config/opencode/opencode.json`

For this project, copy `opencode.example.json` to `opencode.json` in the project root:

```bash
cp opencode.example.json opencode.json
```

Then edit the URL to match your setup (localhost or cloud IP).

---

### OpenCode Integration

Once Ruler MCP is running, connect it to OpenCode.

#### 1. Create OpenCode Config

OpenCode uses `opencode.json` for configuration. Create or edit this file:

**Option A: Project-level (recommended for this project)**
```bash
# In the ruler project directory
touch opencode.json
```

**Option B: Global (for all projects)**
```bash
mkdir -p ~/.config/opencode
touch ~/.config/opencode/opencode.json
```

#### 2. Add MCP Server Configuration

Add the following to your `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ruler": {
      "type": "remote",
      "url": "http://<your-ip>:8787/mcp",
      "enabled": true,
      "timeout": 30000
    }
  }
}
```

- **Local:** `http://localhost:8787/mcp`
- **Cloud instance:** `http://<your-cloud-ip>:8787/mcp`
- **timeout:** Increase to 30000ms (30s) for slower connections

#### 3. Restart OpenCode

```bash
# Restart OpenCode to load the MCP server
opencode
```

#### 4. Verify Connection

```bash
# List MCP servers
opencode mcp list

# Check available tools - you should see 68+ Penpot tools!
/mcp
```

#### Using with Environment Variables

If you want to pass credentials through OpenCode config:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ruler": {
      "type": "remote",
      "url": "http://localhost:8787/mcp",
      "enabled": true,
      "headers": {
        "X-Penpot-Token": "{env:PENPOT_ACCESS_TOKEN}"
      }
    }
  }
}
```

Then set the environment variable:
```bash
export PENPOT_ACCESS_TOKEN=your-token-here
opencode
```

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP not found | Check MCP server is running: `docker ps \| grep penpot-mcp` |
| Connection refused | Ensure port 8787 is open in firewall |
| Tools not loading | Check logs: `docker logs penpot-mcp` |
| Timeout errors | Increase `timeout` in opencode.json (e.g., 60000) |
| 401 Unauthorized on get-file | Set `PENPOT_BACKEND_URL=http://penpot-backend:6060` in .env |
| get_share_links SQL error | Update to latest version - SQL fix included |
| export_frame_png fails 400 | Check penpot-exporter container is running: `docker ps \| grep exporter` |
| No authentication configured | Set PENPOT_ACCESS_TOKEN in .env or use PENPOT_EMAIL/PASSWORD |

---

## MCP Tools

### Base Tools (68 tools from Penpot MCP)

See [TOOLS.md](TOOLS.md) for the complete list.

### Ruler-Specific Tools

#### JSX Export

| Tool | Description |
|------|-------------|
| `ruler_export_jsx` | Export as generic JSX |
| `ruler_export_react` | Export as React component |
| `ruler_export_tailwind` | Export with Tailwind classes |
| `ruler_export_vue` | Export as Vue component |
| `ruler_export_svelte` | Export as Svelte component |
| `ruler_export_html` | Export as plain HTML |

#### Versioning

| Tool | Description |
|------|-------------|
| `ruler_create_checkpoint` | Create named checkpoint |
| `ruler_list_checkpoints` | List all checkpoints |
| `ruler_restore_checkpoint` | Restore to checkpoint |
| `ruler_compare_checkpoints` | Compare checkpoints |
| `ruler_auto_checkpoint` | Auto-snapshot before changes |

#### Skills

| Tool | Description |
|------|-------------|
| `ruler_load_skill` | Load relevant skill |
| `ruler_list_skills` | List available skills |

#### Enhanced

| Tool | Description |
|------|-------------|
| `ruler_get_full_context` | Get complete file state |
| `ruler_extract_tokens` | Extract design tokens |
| `ruler_analyze_design` | AI design analysis |

---

## Skills

Ruler includes a skill system that teaches AI agents how to work with Penpot.

### Available Skills

| Category | Skills |
|----------|--------|
| Design Basics | Create Frame, Add Rectangle, Add Text, Styling |
| Components | Button Patterns, Input Fields, Cards, Navigation |
| Pages | Landing Page, Dashboard, Login Page |
| Workflow | Full Page Build, Iterate with AI, Design to Code |
| Best Practices | Naming Conventions, Color Tokens |

### Using Skills

```
User: "Create a button component"
Agent: calls ruler_load_skill("create button")
→ Returns: Button creation guide with steps and examples
```

---

## AI Agent Integration

### Claude Code (Cline)

Claude Code uses a different MCP configuration format (`.mcp.json`):

**File:** `~/.claude.json` or `.mcp.json` in project root

```json
{
  "mcpServers": {
    "ruler": {
      "type": "http",
      "url": "http://<your-host-pc-ip>:8787/mcp"
    }
  }
}
```

**Note:** This format is for Claude Code / Cline. For OpenCode, use `opencode.json` as shown above.

### Gemini CLI

**File:** `~/.gemini/settings.json`

```json
{
  "mcpServers": {
    "ruler": {
      "httpUrl": "http://<your-host-pc-ip>:8787/mcp"
    }
  }
}
```

### Example Workflow

```
1. Connect AI agent to Ruler MCP
2. Load skill: ruler_load_skill("create button")
3. Create design: create_frame(), create_text()
4. Export code: ruler_export_react()
5. Create checkpoint: ruler_create_checkpoint()
6. Iterate: Make changes, export, repeat
7. Restore if needed: ruler_restore_checkpoint()
```

---

## Development

### Project Structure

```
ruler/
├── src/
│   └── penpot_mcp/             # MCP server implementation
│       ├── __init__.py
│       ├── server.py           # MCP server entry point
│       ├── config.py           # Configuration
│       ├── services/           # API clients
│       ├── tools/              # Tool implementations
│       └── transformers/       # Data transformers
│
├── ruler-skills/               # Skill library for AI agents
│   ├── design-basics/
│   ├── components/
│   ├── pages/
│   ├── workflow/
│   └── best-practices/
│
├── docker-compose.override.yaml # MCP service override
├── Dockerfile                   # MCP server Docker image
├── setup.sh                     # Setup script
├── .env_example                 # Environment template
├── opencode.json                # OpenCode config (create from template)
└── pyproject.toml              # Python package config
```
ruler-mcp/
├── src/
│   ├── penpot_mcp/           # Original ancrz code (upstream)
│   │   ├── server.py         # 68 base tools
│   │   ├── services/         # DB, API clients
│   │   └── tools/            # Tool implementations
│   │
│   └── ruler_ext/            # Ruler customizations
│       ├── jsx_exporter/     # JSX generation
│       ├── versioning/       # Checkpoint system
│       ├── skills/           # Skill integration
│       └── enhanced_tools/    # Analysis tools
│
├── ruler-skills/             # Skill library
│   ├── design-basics/
│   ├── components/
│   ├── pages/
│   ├── workflow/
│   └── best-practices/
│
├── docker/                   # Docker configs
├── tests/
└── pyproject.toml
```

### Adding New Tools

1. Add tool logic in `src/ruler_ext/`
2. Register in `src/server.py` using `@mcp.tool()` decorator
3. Document in this README

### Staying Updateable

This project is a fork of [ancrz/penpot-mcp-server](https://github.com/ancrz/penpot-mcp-server). To stay updated:

```bash
git remote add upstream https://github.com/ancrz/penpot-mcp-server.git
git fetch upstream
git merge upstream/main
```

**Important:** Keep custom code in `src/ruler_ext/` - only merge from upstream's `src/penpot_mcp/`.

---

## FAQ

### Managing Ruler MCP

**Q: How do I restart Ruler after pulling new code?**
A: Use the `--build` flag to rebuild the Docker image:
```bash
docker compose -p penpot -f docker-compose.yaml -f docker-compose.override.yaml up -d --build penpot-mcp
```

**Q: Why doesn't `restart` work after pulling updates?**
A: `restart` only restarts the container with existing code. The new Python code needs to be rebuilt into the image with `--build`.

**Q: How do I check if MCP is running?**
A: `docker ps | grep penpot-mcp`

**Q: How do I see the logs?**
A: `docker logs penpot-mcp` or `docker logs -f penpot-mcp` for live logs.

### Common Issues

**Q: Getting 401 Unauthorized errors on get-file calls.**
A: Set `PENPOT_BACKEND_URL=http://penpot-backend:6060` in your .env file and rebuild.

**Q: export_frame_png returns 400 error.**
A: Check that the penpot-exporter container is running: `docker ps | grep exporter`.

**Q: get_share_links SQL error about deleted_at column.**
A: Update to the latest version - this was fixed in a recent commit.

### Using Ruler

**Q: How do I create multiple shapes efficiently?**
A: Use `create_shapes_batch()` - it creates multiple shapes in 1 API call instead of 50+ individual calls.

**Q: Can I use component instances?**
A: Yes! Use `create_component_instance()` to place existing components on the canvas. Perfect for creating grids of the same component.

**Q: Can I import external SVG files?**
A: Yes! Use `import_svg()` to parse SVG strings into Penpot shapes.

**Q: How do I avoid passing file_id/page_id to every call?**
A: Use `ruler_set_context(file_id="...", page_id="...")` once, then omit those params from subsequent calls.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a PR

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Credits

- [Penpot](https://penpot.app) - The open-source design platform
- [ancrz/penpot-mcp-server](https://github.com/ancrz/penpot-mcp-server) - Base MCP implementation
- [Model Context Protocol](https://modelcontextprotocol.io) - The protocol

---

## Support

- Issues: https://github.com/yourusername/ruler/issues
- Discord: Join our community

---

**Ruler** - Building the future of AI-assisted design.
