# Ruler Skills

This directory contains the skill library for Ruler - a collection of pre-built prompts and guides designed to help AI agents work effectively with Penpot designs.

## Structure

```
skills/
├── _core/                    # Core skill infrastructure
│   ├── __init__.py
│   ├── loader.py             # Skill loading and management
│   └── registry.py           # Skill registration
│
├── design-basics/            # Fundamental design operations
│   ├── create-frame.md
│   ├── add-rectangle.md
│   ├── add-text.md
│   ├── styling-fills.md
│   ├── styling-strokes.md
│   └── layout-flexbox.md
│
├── components/               # Component patterns
│   ├── button-patterns.md
│   ├── input-fields.md
│   ├── cards.md
│   ├── navigation.md
│   ├── modals.md
│   └── lists.md
│
├── pages/                   # Full page templates
│   ├── landing-page.md
│   ├── dashboard.md
│   ├── login-page.md
│   ├── settings-page.md
│   └── profile-page.md
│
├── workflow/                 # AI workflow guides
│   ├── full-page-build.md
│   ├── iterate-with-ai.md
│   ├── design-to-code.md
│   └── responsive-variants.md
│
└── best-practices/          # Design guidelines
    ├── naming-conventions.md
    ├── color-tokens.md
    ├── typography-scale.md
    └── spacing-system.md
```

## Quick Start

1. Place this folder in your Ruler MCP server's skills directory
2. Configure the path in your environment: `RULER_SKILLS_PATH=/path/to/skills`
3. AI agents can now use skills via MCP tools

## Usage

AI agents can load skills using the `ruler_load_skill` MCP tool:

```
User: "Create a button component"
Agent: calls ruler_load_skill("create button")
→ Returns: Button creation skill with steps and examples
```

## Skill Format

Each skill is a markdown file with YAML frontmatter:

```yaml
---
name: create-button
category: components
description: How to create button components in Penpot
triggers:
  - "create a button"
  - "add button component"
  - "make a button"
---
```

## License

MIT License - See LICENSE file for details.
