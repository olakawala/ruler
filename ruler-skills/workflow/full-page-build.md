---
name: Full Page Build
category: workflow
description: Complete workflow for building a full page with AI using Ruler and Penpot
triggers:
  - "build a page"
  - "create a page"
  - "design a page"
  - "make a landing page"
  - "build ui"
---

# Full Page Build Workflow

## Overview

This workflow guides you through creating a complete page design in Penpot using AI assistance. Follow these steps for optimal results.

## Workflow Stages

```
Stage 1: Plan      → Define requirements
Stage 2: Structure → Create page framework  
Stage 3: Components → Build key components
Stage 4: Content   → Add content
Stage 5: Refine    → Polish and iterate
```

---

## Stage 1: Plan

### Before starting, gather:

1. **Page type** - Landing, dashboard, login, etc.
2. **Key sections** - Header, hero, features, footer
3. **Color scheme** - Brand colors, backgrounds
4. **Typography** - Font families, sizes
5. **Responsive** - Desktop, tablet, mobile

### Prompt Example

```
Create a landing page for a SaaS product called "TaskFlow".
Include:
- Navigation header with logo and menu
- Hero section with headline, subtext, and CTA button
- Features section with 3 feature cards
- Testimonials section
- Footer with links

Brand colors: Blue (#2563EB), White, Dark gray (#1F2937)
Font: Inter
```

---

## Stage 2: Structure

### Step-by-Step

1. **Create new file**
   ```
   create_file(project_id="<project-id>", name="TaskFlow Landing Page")
   ```

2. **Create page frames** - One per section
   
   ```
   # Desktop frame (1440x900)
   create_frame(x=0, y=0, width=1440, height=900, name="Desktop")
   
   # Add viewport frames inside
   create_frame(x=0, y=0, width=1440, height=800, name="Hero Section")
   create_frame(x=0, y=800, width=1440, height=600, name="Features Section")
   create_frame(x=0, y=1400, width=1440, height=400, name="Footer")
   ```

3. **Set up layout** - Use Flexbox for each section
   ```
   set_layout(frame_id="<hero-id>", direction="column", gap=24, padding=48)
   set_layout(frame_id="<features-id>", direction="row", gap=24, padding=48)
   ```

---

## Stage 3: Components

### Build reusable components first:

1. **Navigation Bar**
   - Logo (text or image)
   - Menu items (Home, Features, Pricing, About)
   - CTA button

2. **Hero Section**
   - Headline text
   - Subtext  
   - Primary CTA
   - Secondary CTA or image

3. **Feature Cards**
   - Icon
   - Title
   - Description

4. **Footer**
   - Logo
   - Link columns
   - Copyright

### Example: Building the Header

```
# Create header frame
create_frame(
   width=1440, 
   height=80, 
   name="Header",
   fill_color="#FFFFFF"
)

# Set horizontal layout
set_layout(
   frame_id="<header-id>",
   direction="row",
   gap=32,
   padding="0 48"
)

# Add logo
create_text(text="TaskFlow", font_size=24, font_weight="bold")

# Add menu items
create_text(text="Home", font_size=14)
create_text(text="Features", font_size=14)
create_text(text="Pricing", font_size=14)

# Add CTA button
create_frame(width=100, height=40, name="Header CTA", fill_color="#2563EB")
```

---

## Stage 4: Content

### Add text content:

1. **Hero Headline**
   ```
   create_text(
       text="Streamline Your Workflow",
       font_size=56,
       font_weight="bold",
       fill_color="#1F2937"
   )
   ```

2. **Hero Subtext**
   ```
   create_text(
       text="TaskFlow helps teams collaborate and ship faster",
       font_size=20,
       fill_color="#6B7280"
   )
   ```

### Add images (via upload):
```
upload_media(
    file_id="<file-id>",
    name="Hero Image", 
    url="https://example.com/image.png"
)
```

---

## Stage 5: Refine

### Review and adjust:

1. **Check spacing** - Consistent gaps and padding
2. **Verify colors** - Use design tokens
3. **Test responsiveness** - Create mobile variants
4. **Export for code** - Get screenshots and CSS

### Export commands:
```
# Get screenshot
export_frame_png(
    file_id="<file-id>", 
    page_id="<page-id>", 
    object_id="<frame-id>",
    scale=2
)

# Get CSS
get_shape_css(
    file_id="<file-id>",
    page_id="<page-id>",
    shape_id="<frame-id>"
)
```

---

## AI Iteration Workflow

### The Loop

```
1. Make changes
2. Get screenshot
3. Review
4. Iterate or approve
```

### Example Iteration

```
User: "Make the hero button blue instead of green"

AI Agent:
1. Find the CTA button in the hero
2. set_fill(shape_id="<cta-id>", color="#2563EB")
3. export_frame_png() - get updated screenshot
4. Show user for approval
```

---

## Version Control

### Before major changes, create checkpoint:

```
ruler_create_checkpoint(
    file_id="<file-id>",
    label="Before hero redesign",
    ai_prompt="Change hero button to blue"
)
```

This allows easy rollback if needed.

---

## Checklist

Before finishing, verify:

- [ ] All sections present
- [ ] Consistent spacing
- [ ] Brand colors used
- [ ] Typography hierarchy clear
- [ ] Mobile variant created (if needed)
- [ ] Export taken for reference

---

## Related Skills

- [Create Frame](design-basics/create-frame.md)
- [Button Patterns](components/button-patterns.md)
- [Design to Code](workflow/design-to-code.md)
- [Naming Conventions](best-practices/naming-conventions.md)
