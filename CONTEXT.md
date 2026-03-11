# Ruler Context

**AI Agent Context File for Ruler**

This document provides context for AI agents working with Ruler.

---

## What is Ruler?

Ruler is a self-hosted design platform for vibe coding. It connects AI agents to Penpot designs via MCP (Model Context Protocol).

**Use case:** AI agents can read, create, and modify designs - then export the designs as code.

---

## Connection

**MCP Endpoint:** `http://<host>:8787/mcp`

**Required credentials:**
- `PENPOT_ACCESS_TOKEN` - Penpot API token
- Access to Penpot instance (local or cloud)

---

## Key Workflows

### 1. Design to Code

```python
# 1. Get design
get_shape_details(file_id, page_id, shape_id)

# 2. Export as code
ruler_export_react(file_id, page_id, shape_id)

# 3. Get visual reference
export_frame_png(file_id, page_id, shape_id, scale=2)
```

### 2. Create Design with AI

```python
# 1. Load skill for guidance
ruler_load_skill("create button")

# 2. Create elements
create_frame(file_id, page_id, x=0, y=0, width=100, height=40, name="Button")
create_text(file_id, page_id, text="Click Me", ...)

# 3. Export result
export_frame_png(...)
```

### 3. Version Control

```python
# Before making changes
ruler_auto_checkpoint(file_id, ai_prompt="Change button color")

# Make changes
set_fill(file_id, page_id, shape_id, color="#FF0000")

# If unhappy, restore
ruler_restore_checkpoint(checkpoint_id)
```

---

## Available Tools

### Quick Reference

| Category | Tools | Purpose |
|----------|-------|---------|
| **Projects** | `list_projects`, `list_files` | Find designs |
| **Read** | `get_shape_details`, `get_shape_css`, `get_shape_tree` | Understand designs |
| **Create** | `create_frame`, `create_rectangle`, `create_text` | Build designs |
| **Modify** | `set_fill`, `set_stroke`, `move_shape`, `resize_shape` | Edit designs |
| **Export** | `export_frame_png`, `export_frame_svg` | Get visual output |
| **Ruler JSX** | `ruler_export_react`, `ruler_export_tailwind` | Get code |
| **Ruler Version** | `ruler_create_checkpoint`, `ruler_restore_checkpoint` | Version control |
| **Ruler Skills** | `ruler_load_skill` | Get guidance |

---

## Skills System

Ruler has a skill system that provides step-by-step guidance for common tasks.

### How to Use Skills

```python
# Load relevant skill
ruler_load_skill("create button")

# Returns:
# # Button Component Creation
# 
# ## Steps
# 1. Create frame
# 2. Add text
# ...
```

### Available Skills

| Trigger | Description |
|---------|-------------|
| "create a button" | Button component patterns |
| "create a frame" | Frame/artboard creation |
| "build a page" | Full page workflow |
| "design to code" | Export workflow |
| "naming" | Best practices |

---

## Common Patterns

### Find a Design

```python
# List projects
list_projects()

# List files in project
list_files(project_id="<uuid>")

# Get file details
get_file_pages(file_id="<uuid>")
```

### Create a Simple UI

```python
# 1. Create container frame
create_frame(
    file_id="<file>",
    page_id="<page>",
    x=100, y=100,
    width=400, height=300,
    name="Card",
    fill_color="#FFFFFF"
)

# 2. Add content
create_text(
    file_id="<file>",
    page_id="<page>",
    text="Hello World",
    font_size=24
)

# 3. Get screenshot
export_frame_png(
    file_id="<file>",
    page_id="<page>",
    object_id="<frame-id>",
    scale=2
)
```

### Export for Development

```python
# Get React code
ruler_export_react(
    file_id="<file>",
    page_id="<page>",
    shape_id="<component-id>"
)

# Get Tailwind
ruler_export_tailwind(
    file_id="<file>",
    page_id="<page>",
    shape_id="<component-id>"
)

# Get CSS only
get_shape_css(
    file_id="<file>",
    page_id="<page>",
    shape_id="<component-id>"
)
```

---

## Important Notes

### Coordinates
- Penpot uses top-left origin (0,0)
- Units are in pixels

### IDs
- All IDs are UUIDs (e.g., `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`)

### Getting IDs
- Use `list_projects()` → get project UUID
- Use `list_files(project_id="<uuid>")` → get file UUID
- Use `get_file_pages(file_id="<uuid>")` → get page UUIDs

### Naming
- Use clear, descriptive names for shapes
- This helps AI understand the design

---

## Error Handling

If a tool fails:
1. Check the error message
2. Verify file_id, page_id, shape_id are correct
3. Use `get_page_objects()` to see available shapes

---

## File Locations

```
ruler-mcp/
├── src/
│   ├── penpot_mcp/     # Original MCP tools (68 tools)
│   └── ruler_ext/      # Ruler custom tools
│       ├── jsx_exporter/
│       ├── versioning/
│       ├── skills/
│       └── enhanced_tools/
├── ruler-skills/       # Skill markdown files
└── TOOLS.md           # Full tool documentation
```

---

## Getting Help

1. **Skills:** Use `ruler_load_skill("<task>")` for guidance
2. **List tools:** Use `ruler_list_skills()` to see available skills
3. **Tool docs:** See `TOOLS.md` for full tool reference

---

**Remember:** Use checkpoints before major changes with `ruler_auto_checkpoint()` so you can easily rollback!
