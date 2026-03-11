"""
JSX Exporter Module

Converts Penpot shapes to JSX/React/Vue/Svelte code.
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ShapeData:
    """Represents shape data from Penpot."""

    id: str
    name: str
    type: str
    x: float
    y: float
    width: float
    height: float
    fills: List[Dict] = field(default_factory=list)
    strokes: List[Dict] = field(default_factory=list)
    border_radius: float = 0
    opacity: float = 1.0
    layout: Optional[Dict] = None
    text: Optional[Dict] = None


@dataclass
class IntermediateRepresentation:
    """Intermediate representation for code generation."""

    id: str
    name: str
    type: str
    bounds: Dict[str, float]
    style: Dict[str, Any]
    children: List["IntermediateRepresentation"] = field(default_factory=list)
    text: Optional[str] = None


class JSXExporter:
    """Converts Penpot shapes to various code formats."""

    def __init__(self):
        self.framework = "react"
        self.styling = "inline"

    def convert_fill(self, fill: Dict) -> Dict:
        """Convert Penpot fill to style object."""
        style = {}

        if fill.get("fillColor"):
            style["backgroundColor"] = self._normalize_color(fill["fillColor"])

        if fill.get("fillOpacity"):
            style["opacity"] = fill["fillOpacity"]

        if fill.get("fillColorGradient"):
            style["background"] = self._convert_gradient(fill["fillColorGradient"])

        return style

    def convert_stroke(self, stroke: Dict) -> Dict:
        """Convert Penpot stroke to style object."""
        style = {}

        if stroke.get("strokeColor"):
            style["borderColor"] = self._normalize_color(stroke["strokeColor"])

        if stroke.get("strokeWidth"):
            style["borderWidth"] = f"{stroke['strokeWidth']}px"

        if stroke.get("strokeStyle"):
            style["borderStyle"] = stroke["strokeStyle"]

        return style

    def _normalize_color(self, color: str) -> str:
        """Normalize color to appropriate format."""
        return color

    def _convert_gradient(self, gradient: Dict) -> str:
        """Convert gradient to CSS."""
        return "linear-gradient(...)"

    def shape_to_ir(self, shape_data: ShapeData) -> IntermediateRepresentation:
        """Convert shape data to intermediate representation."""
        style = {}

        for fill in shape_data.fills:
            style.update(self.convert_fill(fill))

        for stroke in shape_data.strokes:
            style.update(self.convert_stroke(stroke))

        if shape_data.border_radius:
            style["borderRadius"] = f"{shape_data.border_radius}px"

        style["width"] = f"{shape_data.width}px"
        style["height"] = f"{shape_data.height}px"

        if shape_data.type == "frame":
            style["position"] = "relative"
            style["left"] = f"{shape_data.x}px"
            style["top"] = f"{shape_data.y}px"

        if shape_data.layout:
            style.update(self._convert_layout(shape_data.layout))

        return IntermediateRepresentation(
            id=shape_data.id,
            name=shape_data.name,
            type=shape_data.type,
            bounds={
                "x": shape_data.x,
                "y": shape_data.y,
                "width": shape_data.width,
                "height": shape_data.height,
            },
            style=style,
            text=shape_data.text.get("content") if shape_data.text else None,
        )

    def _convert_layout(self, layout: Dict) -> Dict:
        """Convert layout properties to CSS."""
        style = {}

        if layout.get("layoutType") == "flex":
            style["display"] = "flex"

            direction = layout.get("direction", "row")
            if direction == "column":
                style["flexDirection"] = "column"

            gap = layout.get("gap")
            if gap:
                style["gap"] = f"{gap}px"

            padding = layout.get("padding")
            if padding:
                style["padding"] = f"{padding}px"

            align = layout.get("alignItems")
            if align:
                style["alignItems"] = align

            justify = layout.get("justifyContent")
            if justify:
                style["justifyContent"] = justify

        return style

    def generate_react(self, ir: IntermediateRepresentation) -> str:
        """Generate React component code."""
        style_str = self._style_to_js(ir.style)

        children = ""
        if ir.text:
            children = f"\n  {ir.text}\n"
        elif ir.children:
            for child in ir.children:
                children += f"\n  {self.generate_react(child)}\n"

        component_name = self._to_pascal_case(ir.name)

        return f"""export function {component_name}({{ children }}) {{
  return (
    <div style={{{style_str}}}>{children}
    </div>
  );
}}"""

    def generate_vue(self, ir: IntermediateRepresentation) -> str:
        """Generate Vue component code."""
        style_str = self._style_to_css(ir.style)

        template = "<div>"
        if ir.text:
            template += ir.text
        elif ir.children:
            for child in ir.children:
                template += f"\n  {self._to_kebab_case(child.name)}"
        template += "</div>"

        return f"""<template>
  {template}
</template>

<script setup>
</script>

<style scoped>
.{self._to_kebab_case(ir.name)} {{
  {style_str}
}}
</style>"""

    def generate_svelte(self, ir: IntermediateRepresentation) -> str:
        """Generate Svelte component code."""
        style_str = self._style_to_css(ir.style)

        return f"""<script>
</script>

<div class="{self._to_kebab_case(ir.name)}" style="{style_str}">
  {ir.text or ""}
</div>

<style>
  .{self._to_kebab_case(ir.name)} {{
    {style_str}
  }}
</style>"""

    def generate_tailwind(self, ir: IntermediateRepresentation) -> str:
        """Generate React with Tailwind classes."""
        classes = self._styles_to_tailwind(ir.style)

        children = ir.text or ""

        component_name = self._to_pascal_case(ir.name)

        return f"""export function {component_name}({{ children }}) {{
  return (
    <div className="{classes}">{children}</div>
  );
}}"""

    def generate_html(self, ir: IntermediateRepresentation) -> str:
        """Generate plain HTML."""
        style_str = self._style_to_css(ir.style)

        return f"""<div style="{style_str}">
  {ir.text or ""}
</div>"""

    def _style_to_js(self, style: Dict) -> str:
        """Convert style dict to JS object string."""
        if not style:
            return ""

        pairs = []
        for key, value in style.items():
            js_key = self._to_camel_case(key)
            if isinstance(value, str):
                pairs.append(f"{js_key}: '{value}'")
            else:
                pairs.append(f"{js_key}: {value}")

        return ", ".join(pairs)

    def _style_to_css(self, style: Dict) -> str:
        """Convert style dict to CSS string."""
        if not style:
            return ""

        pairs = []
        for key, value in style.items():
            css_key = key.replace("_", "-")
            pairs.append(f"{css_key}: {value};")

        return "\n  ".join(pairs)

    def _styles_to_tailwind(self, style: Dict) -> str:
        """Convert style dict to Tailwind classes (simplified)."""
        classes = []

        if "backgroundColor" in style:
            classes.append("bg-white")

        if "borderRadius" in style:
            classes.append("rounded")

        if "display" in style and style["display"] == "flex":
            classes.append("flex")

        if "flexDirection" in style and style["flexDirection"] == "column":
            classes.append("flex-col")

        return " ".join(classes) if classes else ""

    def _to_camel_case(self, s: str) -> str:
        """Convert snake_case to camelCase."""
        parts = s.split("_")
        return parts[0] + "".join(p.title() for p in parts[1:])

    def _to_pascal_case(self, s: str) -> str:
        """Convert to PascalCase."""
        return "".join(word.title() for word in s.split())

    def _to_kebab_case(self, s: str) -> str:
        """Convert to kebab-case."""
        return s.lower().replace(" ", "-")

    async def export_shape(
        self, shape_data: ShapeData, framework: str = "react", styling: str = "inline"
    ) -> str:
        """Export a shape to code."""
        self.framework = framework
        self.styling = styling

        ir = self.shape_to_ir(shape_data)

        if framework == "react":
            if styling == "tailwind":
                return self.generate_tailwind(ir)
            return self.generate_react(ir)
        elif framework == "vue":
            return self.generate_vue(ir)
        elif framework == "svelte":
            return self.generate_svelte(ir)
        elif framework == "html":
            return self.generate_html(ir)

        return "# Unsupported framework"
