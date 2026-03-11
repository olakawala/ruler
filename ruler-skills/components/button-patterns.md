---
name: Button Patterns
category: components
description: How to create various button component patterns in Penpot
triggers:
  - "create a button"
  - "add button"
  - "make a button"
  - "button component"
  - "primary button"
  - "secondary button"
---

# Button Component Patterns

## Overview

Buttons are interactive UI elements that trigger actions. This skill covers creating various button styles and states in Penpot.

## Button Types

### 1. Primary Button

The main call-to-action button.

**Structure:**
- Background: Brand color (typically blue or primary color)
- Text: White, centered
- Border radius: 6-8px
- Padding: 12px 24px

**Implementation:**
```
1. create_frame(
   width=120, 
   height=44, 
   name="Primary Button",
   fill_color="#3B82F6",
   border_radius=6,
   clip_content=true
)

2. create_text(
   text="Click Me",
   font_size=14,
   font_weight="bold",
   fill_color="#FFFFFF",
   text_align="center"
)
```

### 2. Secondary Button

Outlined variant for less prominent actions.

**Structure:**
- Background: Transparent
- Border: 1-2px solid brand color
- Text: Brand color
- Border radius: 6-8px

**Implementation:**
```
create_frame(
   width=120,
   height=44,
   name="Secondary Button",
   fill_color="transparent",
   stroke_color="#3B82F6",
   stroke_width=2,
   border_radius=6
)
```

### 3. Ghost Button

Text-only button for minimal UI.

**Structure:**
- No background
- No border
- Text only
- Subtle hover effect

**Implementation:**
```
create_frame(
   width=100,
   height=40,
   name="Ghost Button",
   fill_color="transparent"
)
```

### 4. Icon Button

Button with icon only.

**Structure:**
- Square or circular
- Icon centered
- Used for actions like close, menu, search

**Implementation:**
```
create_ellipse(
   width=40,
   height=40,
   name="Icon Button",
   fill_color="#6B7280"
)
```

## Button States

| State | Visual Change |
|-------|---------------|
| Default | Base styling |
| Hover | Slightly lighter/darker |
| Active/Pressed | Darker shade |
| Disabled | 50% opacity |

## Creating Interactive Buttons

### With Hover Interaction

Use interaction panels in Penpot UI:
1. Select the button frame
2. Add hover interaction
3. Set target fill color

## Button Component Best Practices

1. **Consistent height** - Use 36-48px for standard buttons
2. **Clear labels** - Use action verbs: "Submit", "Save", "Cancel"
3. ** Adequate touch target** - Minimum 44x44px for mobile
4. **Visual hierarchy** - Primary > Secondary > Ghost

## Example: Full Button Set

```
# Primary Button
- Frame: 120x44, fill=#3B82F6, radius=6
- Text: "Get Started", white, 14px bold

# Secondary Button  
- Frame: 100x44, stroke=#3B82F6, radius=6
- Text: "Learn More", #3B82F6, 14px

# Ghost Button
- Frame: 80x40, transparent
- Text: "Skip", #6B7280, 14px
```

## Using with Layout

Buttons often appear in rows:

```
Parent Frame (horizontal layout, gap=12):
├── Primary Button
├── Secondary Button
└── Ghost Button
```

## Related Skills

- [Create Frame](design-basics/create-frame.md)
- [Layout Flexbox](design-basics/layout-flexbox.md)
- [Add Text](design-basics/add-text.md)
