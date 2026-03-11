---
name: Create Frame
category: design-basics
description: How to create frames (artboards) in Penpot for organizing designs
triggers:
  - "create a frame"
  - "add frame"
  - "new frame"
  - "make an artboard"
  - "create container"
---

# Creating Frames in Penpot

## Overview

Frames (also called artboards or containers) are the fundamental building blocks for organizing content in Penpot. They provide layout capabilities and serve as containers for grouping related elements.

## When to Use Frames

- Create page sections (header, hero, content, footer)
- Build reusable components
- Define responsive breakpoints
- Group related elements together

## Steps to Create a Frame

### 1. Using the Create Frame Tool

Use the `create_frame` MCP tool:

```
create_frame(
    file_id="<file-uuid>",
    page_id="<page-uuid>",
    x=100,
    y=100,
    width=800,
    height=600,
    name="Hero Section",
    fill_color="#FFFFFF",
    border_radius=0
)
```

### 2. Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| file_id | string | required | UUID of the file |
| page_id | string | required | UUID of the page |
| x | number | 0 | X position |
| y | number | 0 | Y position |
| width | number | 300 | Frame width |
| height | number | 300 | Frame height |
| name | string | "Frame" | Frame name |
| fill_color | string | "#FFFFFF" | Background color |
| fill_opacity | number | 1.0 | Background opacity |
| stroke_color | string | null | Border color |
| stroke_width | number | 1.0 | Border width |
| border_radius | number | 0 | Corner radius |
| clip_content | boolean | true | Clip children at bounds |

### 3. Adding Layout Properties

Frames support Flexbox layout. Configure with `set_layout`:

```
set_layout(
    file_id="<file-uuid>",
    page_id="<page-uuid>",
    frame_id="<frame-uuid>",
    layout_type="flex",
    direction="column",
    gap=16,
    padding=24,
    align_items="center",
    justify_content="flex-start"
)
```

## Layout Types

| Type | Description |
|------|-------------|
| flex | Flexbox layout (most common) |
| grid | CSS Grid layout |

## Flex Direction

| Value | Description |
|-------|-------------|
| row | Horizontal layout |
| column | Vertical layout |

## Example: Hero Section Frame

```
1. Create frame: width=1200, height=600, fill_color="#1a1a2e"
2. Set layout: direction="column", gap=24, padding=48
3. Add content inside the frame
```

## Best Practices

1. **Name frames descriptively** - Use names like "Header", "Footer", "Login Form"
2. **Use consistent padding** - Define padding variables for reuse
3. **Set up layout early** - Configure Flexbox before adding children
4. **Consider responsiveness** - Use percentage widths or constraints

## Common Frame Sizes

| Frame Type | Width | Height |
|------------|-------|--------|
| Desktop | 1440 | 900+ |
| Tablet | 768 | 1024 |
| Mobile | 375 | 812 |
| Card | 300 | 200 |
| Button | auto | 40-48 |

## Related Skills

- [Layout Flexbox](design-basics/layout-flexbox.md)
- [Add Rectangle](design-basics/add-rectangle.md)
- [Styling Fills](design-basics/styling-fills.md)
