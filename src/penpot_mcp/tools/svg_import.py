"""SVG import tools - parse SVG strings and convert to Penpot shapes."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any


def parse_svg_to_shapes(
    svg_content: str,
    x: float = 0,
    y: float = 0,
) -> list[dict]:
    """Parse an SVG string and convert to Penpot shape specs.

    This is a best-effort parser that handles common SVG elements.
    Complex SVGs may need manual adjustment.

    Args:
        svg_content: The SVG string to parse.
        x: Base X position offset.
        y: Base Y position offset.

    Returns:
        List of shape specifications that can be passed to create_shapes_batch.

    Example:
        svg = '''<svg width="100" height="100">
            <rect x="10" y="10" width="80" height="80" fill="red"/>
            <circle cx="50" cy="50" r="20" fill="blue"/>
        </svg>'''

        shapes = parse_svg_to_shapes(svg, x=100, y=200)
        # Returns list of shape specs for create_shapes_batch
    """
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as e:
        raise ValueError(f"Invalid SVG content: {e}")

    # Get SVG dimensions
    width = _parse_length(root.get("width", "100"))
    height = _parse_length(root.get("height", "100"))

    shapes = []
    shape_index = 0

    # Process children
    for child in root:
        if child.tag.endswith("}") or child.tag.startswith("{"):
            # Strip namespace
            tag = child.tag.split("}")[-1]
        else:
            tag = child.tag

        shape_spec = _parse_element(tag, child, shape_index, x, y)
        if shape_spec:
            shapes.append(shape_spec)
            shape_index += 1

    return shapes


def _parse_element(
    tag: str, element: ET.Element, index: int, x: float, y: float
) -> dict | None:
    """Parse a single SVG element to a Penpot shape spec."""

    # Get common attributes
    elem_x = _parse_length(element.get("x", "0")) + x
    elem_y = _parse_length(element.get("y", "0")) + y
    elem_width = _parse_length(element.get("width", "100"))
    elem_height = _parse_length(element.get("height", "100"))
    fill = element.get("fill", "#000000")
    stroke = element.get("stroke")
    stroke_width = _parse_length(element.get("stroke-width", "1"))
    opacity = float(element.get("opacity", "1"))
    rx = _parse_length(element.get("rx", "0"))
    ry = _parse_length(element.get("ry", "0"))

    name = element.get("id") or f"{tag}_{index}"

    if tag == "rect":
        # Rectangle
        return {
            "type": "rect",
            "name": name,
            "x": elem_x,
            "y": elem_y,
            "width": elem_width,
            "height": elem_height,
            "fill_color": fill,
            "stroke_color": stroke,
            "stroke_width": stroke_width,
            "opacity": opacity,
            "border_radius": rx or ry,
        }

    elif tag == "circle":
        # Circle - use ellipse with equal dimensions
        cx = _parse_length(element.get("cx", "0")) + x
        cy = _parse_length(element.get("cy", "0")) + y
        r = _parse_length(element.get("r", "50"))
        return {
            "type": "ellipse",
            "name": name,
            "x": cx - r,
            "y": cy - r,
            "width": r * 2,
            "height": r * 2,
            "fill_color": fill,
            "stroke_color": stroke,
            "stroke_width": stroke_width,
            "opacity": opacity,
        }

    elif tag == "ellipse":
        # Ellipse
        cx = _parse_length(element.get("cx", "0")) + x
        cy = _parse_length(element.get("cy", "0")) + y
        rx = _parse_length(element.get("rx", "50"))
        ry = _parse_length(element.get("ry", "50"))
        return {
            "type": "ellipse",
            "name": name,
            "x": cx - rx,
            "y": cy - ry,
            "width": rx * 2,
            "height": ry * 2,
            "fill_color": fill,
            "stroke_color": stroke,
            "stroke_width": stroke_width,
            "opacity": opacity,
        }

    elif tag == "text":
        # Text element
        content = element.text or ""
        font_size = _parse_length(element.get("font-size", "16"))
        return {
            "type": "text",
            "name": name,
            "x": elem_x,
            "y": elem_y,
            "width": max(elem_width, 100),
            "height": max(font_size * 1.2, 20),
            "fill_color": fill,
            "content": content,
            "font_size": font_size,
            "font_family": element.get("font-family", "Inter"),
        }

    elif tag == "path":
        # Path - convert to Penpot path
        d = element.get("d", "")
        if d:
            return {
                "type": "path",
                "name": name,
                "x": elem_x,
                "y": elem_y,
                "width": elem_width,
                "height": elem_height,
                "fill_color": fill,
                "stroke_color": stroke,
                "stroke_width": stroke_width,
                "opacity": opacity,
                "path_data": d,
            }

    elif tag == "g":
        # Group - recursively parse children
        shapes = []
        child_index = 0
        for child in element:
            if child.tag.endswith("}") or child.tag.startswith("{"):
                child_tag = child.tag.split("}")[-1]
            else:
                child_tag = child.tag

            child_spec = _parse_element(child_tag, child, child_index, elem_x, elem_y)
            if child_spec:
                shapes.append(child_spec)
                child_index += 1

        if shapes:
            # Create a frame to hold the group
            return {
                "type": "frame",
                "name": name,
                "x": elem_x,
                "y": elem_y,
                "width": max(elem_width, 100),
                "height": max(elem_height, 100),
                "fill_color": None,
                "children": shapes,
            }

    # Unsupported element
    return None


def _parse_length(value: str) -> float:
    """Parse a length value, handling px, em, etc."""
    if not value:
        return 0

    # Remove common units
    value = value.strip().lower()
    for unit in ["px", "pt", "em", "rem", "%", "cm", "mm", "in"]:
        if value.endswith(unit):
            value = value[: -len(unit)]
            break

    try:
        return float(value)
    except ValueError:
        return 0
