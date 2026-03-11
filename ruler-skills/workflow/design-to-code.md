---
name: Design to Code
category: workflow
description: How to extract code from Penpot designs for development use
triggers:
  - "export code"
  - "get code"
  - "design to code"
  - "generate code"
  - "extract code"
  - "convert to code"
---

# Design to Code Workflow

## Overview

This workflow guides you through converting Penpot designs into usable code for development. Ruler provides multiple export options for different frameworks.

## Export Options

| Method | Description | Best For |
|--------|-------------|----------|
| JSX Export | React components | React projects |
| Tailwind Export | Tailwind CSS classes | Tailwind projects |
| Vue Export | Vue components | Vue projects |
| Svelte Export | Svelte components | Svelte projects |
| HTML Export | Plain HTML | Static sites |

---

## Step 1: Prepare the Design

Before exporting, ensure your design is structured properly:

1. **Use frames for components** - Each component should be in its own frame
2. **Name elements clearly** - Use descriptive names
3. **Set up layout** - Use Flexbox for proper structure
4. **Group related elements** - Use groups for complex components

---

## Step 2: Choose Export Method

### For React Projects

```
ruler_export_react(
    file_id="<file-id>",
    page_id="<page-id>",
    shape_id="<component-id>",
    styling="inline"
)
```

Returns:
```jsx
export function MyComponent() {
  return (
    <div style={{
      display: 'flex',
      padding: '16px',
      backgroundColor: '#FFFFFF'
    }}>
      {/* content */}
    </div>
  );
}
```

### For Tailwind Projects

```
ruler_export_tailwind(
    file_id="<file-id>",
    page_id="<page-id>",
    shape_id="<component-id>"
)
```

Returns:
```jsx
<div className="flex p-4 bg-white">
  {/* content */}
</div>
```

### For Vue Projects

```
ruler_export_vue(
    file_id="<file-id>",
    page_id="<page-id>",
    shape_id="<component-id>"
)
```

Returns:
```vue
<template>
  <div class="component">
    <!-- content -->
  </div>
</template>

<style scoped>
.component {
  display: flex;
  padding: 16px;
}
</style>
```

---

## Step 3: Extract Design Tokens

Get colors and typography:

```
ruler_extract_tokens(file_id="<file-id>")
```

Returns:
```json
{
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#6B7280",
    "background": "#FFFFFF"
  },
  "typography": {
    "heading": {
      "fontFamily": "Inter",
      "fontSize": "32px",
      "fontWeight": "bold"
    },
    "body": {
      "fontFamily": "Inter", 
      "fontSize": "16px"
    }
  }
}
```

---

## Step 4: Get CSS for Specific Elements

For individual elements:

```
get_shape_css(
    file_id="<file-id>",
    page_id="<page-id>",
    shape_id="<element-id>"
)
```

Returns:
```css
.element {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  background-color: #3B82F6;
  border-radius: 6px;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 500;
}
```

---

## Step 5: Get Visual Reference

Always include a screenshot:

```
export_frame_png(
    file_id="<file-id>",
    page_id="<page-id>",
    object_id="<component-id>",
    scale=2
)
```

This returns a base64-encoded PNG that you can include in documentation or code comments.

---

## Complete Workflow Example

### Converting a Button Component

1. **Identify the component**
   - Frame name: "Primary Button"
   - Contains: Rectangle + Text

2. **Get the code**
   ```
   ruler_export_react(
       shape_id="<button-frame-id>",
       styling="inline"
   )
   ```

3. **Output**
   ```jsx
   export function PrimaryButton({ children }) {
     return (
       <button style={{
         display: 'inline-flex',
         alignItems: 'center',
         justifyContent: 'center',
         padding: '8px 16px',
         backgroundColor: '#3B82F6',
         borderRadius: '6px',
         color: '#FFFFFF',
         fontSize: '14px',
         fontWeight: '500',
         border: 'none',
         cursor: 'pointer'
       }}>
         {children || 'Button'}
       </button>
     );
   }
   ```

4. **Get screenshot**
   ```
   export_frame_png(shape_id="<button-frame-id>", scale=2)
   ```

---

## Tips for Better Exports

### Do:

- **Use consistent spacing** - Follow a grid system
- **Name everything** - Clear names help identify elements
- **Group logically** - Keep related elements together
- **Use design tokens** - Colors and typography should be consistent

### Don't:

- **Mix units** - Stick to pixels or percentages
- **Overlap elements** - This causes export issues
- **Use effects sparingly** - Complex shadows/blur may not export well
- **Forget mobile** - Export responsive variants separately

---

## Integration with Codebase

### Manual Integration

1. Copy exported code
2. Paste into your component file
3. Adjust as needed

### Automated Integration (Advanced)

Use Ruler with Claude Code or Cursor:

```
User: "Create a login form based on the Login Page design in Penpot"

Agent:
1. ruler_load_skill("login page")
2. Get design via MCP
3. ruler_export_react for each component
4. Generate complete form code
```

---

## Related Skills

- [Full Page Build](workflow/full-page-build.md)
- [Button Patterns](components/button-patterns.md)
- [Color Tokens](best-practices/color-tokens.md)
- [Typography Scale](best-practices/typography-scale.md)
