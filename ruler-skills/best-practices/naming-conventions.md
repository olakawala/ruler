---
name: Naming Conventions
category: best-practices
description: Best practices for naming elements in Penpot for AI and team collaboration
triggers:
  - "naming"
  - "conventions"
  - "naming convention"
  - "structure"
---

# Naming Conventions

## Overview

Consistent naming makes designs easier to navigate, export, and maintain. Good names help AI agents understand your design structure.

## Why Naming Matters

- **AI Understanding** - Agents find elements by name
- **Team Clarity** - Everyone knows what's what
- **Code Export** - Exported code uses element names
- **Version Control** - Easier to track changes

---

## Frame Naming

### Use Descriptive Names

| ❌ Bad | ✅ Good |
|--------|---------|
| Frame 1 | Header |
| Rectangle 2 | Hero Background |
| Group 3 | Navigation Menu |
| Frame 4 | Feature Card |

### Naming Patterns

| Pattern | Example | Use For |
|---------|---------|---------|
| `{Component}` | Button, Card, Input | Components |
| `{Section}` | Hero, Features, Footer | Page sections |
| `{State}` | Button Hover, Input Focus | Interactive states |
| `{Variant}` | Primary Button, Dark Card | Component variants |

---

## Element Naming

### General Rules

1. **Use PascalCase** - `HeroSection`, `SubmitButton`
2. **Be specific** - `LoginFormEmailInput` not `Input`
3. **Use common prefixes**:
   - `btn-` for buttons
   - `icon-` for icons
   - `img-` for images
   - `txt-` for text elements

### Examples

| ❌ Bad | ✅ Good |
|--------|---------|
| Text | Hero Headline |
| Rectangle | Card Background |
| Ellipse | Avatar Circle |
| Path | Logo Icon |
| Group | Social Links |

---

## Page Structure

### Recommended Hierarchy

```
File: Landing Page
├── Page: Desktop
│   ├── Frame: Header
│   │   ├── Logo
│   │   ├── Nav Menu
│   │   └── CTA Button
│   Section
│   │ ├── Frame: Hero   ├── Hero Background
│   │   ├── Hero Headline
│   │   ├── Hero Subtext
│   │   └── Hero CTA Group
│   │       ├── Primary Button
│   │       └── Secondary Button
│   ├── Frame: Features Section
│   │   ├── Section Header
│   │   └── Feature Card Group
│   │       ├── Feature Card 1
│   │       ├── Feature Card 2
│   │       └── Feature Card 3
│   └── Frame: Footer
└── Page: Mobile
    └── ...
```

---

## Component Naming

### Base Components

| Component | Naming | Example |
|-----------|--------|---------|
| Button | `{Variant} {Type}` | Primary Button, Ghost Button |
| Input | `{Purpose} {Type}` | Email Input, Search Input |
| Card | `{Purpose} Card | Feature Card, Product Card |
| Modal | `{Purpose} Modal | Login Modal, Confirm Modal |
| Dropdown | `{Purpose} Dropdown | Language Dropdown |
| Badge | `{Type} Badge | New Badge, Status Badge |

### With States

| State | Naming | Example |
|-------|--------|---------|
| Default | `{Name}` | Button |
| Hover | `{Name} Hover` | Button Hover |
| Active | `{Name} Active` | Button Active |
| Disabled | `{Name} Disabled` | Button Disabled |

---

## Practical Examples

### Login Form

```
Login Page
├── Login Form Container
│   ├── Login Header
│   ├── Email Input Field
│   │   ├── Email Label
│   │   └── Email Input
│   ├── Password Input Field
│   │   ├── Password Label
│   │   └── Password Input
│   ├── Remember Me Checkbox
│   ├── Login Submit Button
│   └── Forgot Password Link
```

### Dashboard

```
Dashboard Page
├── Sidebar
│   ├── Logo
│   ├── Nav Items Group
│   │   ├── Dashboard Nav Item
│   │   ├── Projects Nav Item
│   │   └── Settings Nav Item
│   └── User Profile
├── Main Content
│   ├── Page Header
│   │   ├── Title
│   │   └── Action Buttons
│   ├── Stats Cards Row
│   │   ├── Total Users Card
│   │   ├── Active Projects Card
│   │   └── Revenue Card
│   └── Recent Activity Table
```

---

## Tips for AI Workflows

### When Working with AI Agents

1. **Name sections clearly** - AI finds "Hero Section" easily
2. **Group related elements** - Use groups with clear names
3. **Label interactive elements** - "Submit Button" not just "Button"
4. **Use consistent patterns** - Same structure across pages

### Example Prompts

```
Good: "Change the Hero Section background color"
     → Clear target, AI finds it easily

Bad:  "Make the top part blue"
     → Ambiguous, AI doesn't know which element
```

---

## Related Skills

- [Full Page Build](workflow/full-page-build.md)
- [Color Tokens](best-practices/color-tokens.md)
- [Spacing System](best-practices/spacing-system.md)
