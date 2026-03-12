"""Component, design token, color, and typography reading/writing tools."""

from __future__ import annotations

from typing import Any

from penpot_mcp.services.api import api


async def _get_file_data(file_id: str) -> dict:
    return await api.command("get-file", {"id": file_id, "components-v2": True})


async def get_component_instances(file_id: str) -> list[dict]:
    """List all components defined in a file.

    Args:
        file_id: The file UUID.
    """
    file_data = await _get_file_data(file_id)
    data = file_data.get("data", {})

    components = data.get("components", {})
    result = []
    for comp_id, comp in components.items():
        result.append(
            {
                "id": comp_id,
                "name": comp.get("name"),
                "path": comp.get("path"),
                "main_instance_id": comp.get("main-instance-id"),
                "main_instance_page": comp.get("main-instance-page"),
                "annotation": comp.get("annotation"),
            }
        )
    return result


async def create_component_instance(
    file_id: str,
    page_id: str,
    component_id: str,
    x: float = 0,
    y: float = 0,
    name: str | None = None,
    component_file_id: str | None = None,
) -> dict:
    """Create an instance of an existing component on a page.

    This creates a reference to a component rather than duplicating shapes.
    Changes to the component will propagate to all instances.

    Args:
        file_id: The file UUID (where to place the instance).
        page_id: The page UUID.
        component_id: The component UUID to instantiate.
        x: X position for the instance (default 0).
        y: Y position for the instance (default 0).
        name: Optional name for the instance.
        component_file_id: File containing the component. If different from file_id,
                         the component is from a shared library.

    Returns:
        Dict with instance_id, component_id, and position.

    Example:
        # Get available components
        components = get_component_instances(file_id)

        # Create 4 instances in a grid
        for i in range(4):
            create_component_instance(
                file_id, page_id,
                component_id=components[0]["id"],
                x=i * 200, y=0
            )
    """
    from penpot_mcp.services.changes import (
        ROOT_FRAME_ID,
        apply_changes,
        change_add_obj,
        new_uuid,
    )

    # Get component file - defaults to same file
    comp_file = component_file_id or file_id

    # Get the component definition to find its bounds
    file_data = await _get_file_data(comp_file)
    components = file_data.get("data", {}).get("components", {})
    component = components.get(component_id, {})

    # Get the main instance to determine size
    main_instance_id = component.get("main-instance-id")
    width = 100
    height = 100

    if main_instance_id:
        # Try to get dimensions from the main instance
        pages = file_data.get("data", {}).get("pages-index", {})
        for page_data in pages.values():
            objects = page_data.get("objects", {})
            main_inst = objects.get(main_instance_id, {})
            width = main_inst.get("width", 100)
            height = main_inst.get("height", 100)
            break

    instance_id = new_uuid()

    # Create the instance - a shape that references the component
    # The key is setting component-id and component-file
    obj: dict[str, Any] = {
        "id": instance_id,
        "type": "frame",
        "name": name or f"{component.get('name', 'Component')} Instance",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "component-id": component_id,
        "component-file": comp_file,
        "shapes": [],
        "hide-in-viewer": False,
    }

    change = change_add_obj(page_id, ROOT_FRAME_ID, obj)
    await apply_changes(file_id, [change])

    return {
        "instance_id": instance_id,
        "component_id": component_id,
        "component_file": comp_file,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "name": obj["name"],
    }


async def get_design_tokens(file_id: str) -> dict:
    """Get all design tokens (colors, typographies, components) from a file.

    Provides a consolidated view of the file's design system.

    Args:
        file_id: The file UUID.
    """
    file_data = await _get_file_data(file_id)
    data = file_data.get("data", {})

    return {
        "colors": _extract_colors(data),
        "typographies": _extract_typographies(data),
        "components_count": len(data.get("components", {})),
        "media_count": len(data.get("media", {})),
    }


async def get_colors_library(file_id: str) -> list[dict]:
    """Get all colors defined in a file's library.

    Args:
        file_id: The file UUID.
    """
    file_data = await _get_file_data(file_id)
    data = file_data.get("data", {})
    return _extract_colors(data)


async def get_typography_library(file_id: str) -> list[dict]:
    """Get all typographies defined in a file's library.

    Args:
        file_id: The file UUID.
    """
    file_data = await _get_file_data(file_id)
    data = file_data.get("data", {})
    return _extract_typographies(data)


def _extract_colors(data: dict) -> list[dict]:
    """Extract color definitions from file data."""
    colors = data.get("colors", {})
    result = []
    for color_id, color in colors.items():
        result.append(
            {
                "id": color_id,
                "name": color.get("name"),
                "color": color.get("color"),
                "opacity": color.get("opacity"),
                "gradient": color.get("gradient"),
                "path": color.get("path"),
            }
        )
    return result


def _extract_typographies(data: dict) -> list[dict]:
    """Extract typography definitions from file data."""
    typographies = data.get("typographies", {})
    result = []
    for typo_id, typo in typographies.items():
        result.append(
            {
                "id": typo_id,
                "name": typo.get("name"),
                "font_family": typo.get("font-family"),
                "font_id": typo.get("font-id"),
                "font_size": typo.get("font-size"),
                "font_style": typo.get("font-style"),
                "font_variant_id": typo.get("font-variant-id"),
                "font_weight": typo.get("font-weight"),
                "letter_spacing": typo.get("letter-spacing"),
                "line_height": typo.get("line-height"),
                "text_transform": typo.get("text-transform"),
                "path": typo.get("path"),
            }
        )
    return result
