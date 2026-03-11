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
git clone https://github.com/yourusername/ruler.git
cd ruler/ruler-mcp

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your Penpot credentials

# Run the MCP server
python -m src.server
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
| `PENPOT_PUBLIC_URL` | `http://localhost:9001` | Public URL |
| `PENPOT_ACCESS_TOKEN` | - | API access token |
| `PENPOT_DB_HOST` | `penpot-postgres` | PostgreSQL host |
| `MCP_PORT` | `8787` | MCP server port |
| `RULER_SKILLS_PATH` | `./ruler-skills` | Skills directory |

### Penpot Setup

1. Enable access tokens in Penpot:
   ```
   PENPOT_FLAGS=enable-login-with-password enable-registration enable-access-tokens enable-plugins-runtime
   ```
2. Create an access token in Penpot profile settings
3. Add token to your `.env` file

---

### OpenCode Integration

Once Ruler MCP is running, connect it to OpenCode:

#### 1. Get Your MCP Server URL

- **Local:** `http://localhost:8787/mcp`
- **Cloud instance:** `http://<your-cloud-ip>:8787/mcp`

#### 2. Add to OpenCode

```bash
# Using OpenCode CLI
opencode mcp add ruler http://localhost:8787/mcp
```

Or manually add to your `.mcp.json`:

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

#### 3. Verify Connection

```bash
# Restart OpenCode
opencode

# Check MCP tools are loaded
/mcp
```

You should see 68+ Penpot tools available!

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP not found | Check MCP server is running: `docker ps \| grep penpot-mcp` |
| Connection refused | Ensure port 8787 is open in firewall |
| Tools not loading | Check logs: `docker logs penpot-mcp` |

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

### Claude Code

**File:** `~/.claude.json` or `.mcp.json`

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
