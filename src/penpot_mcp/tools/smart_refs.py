"""Smart reference resolution - convert shape names to UUIDs."""

from __future__ import annotations

from penpot_mcp.services.api import api
from penpot_mcp.tools.shapes import _get_page_objects


async def resolve_shape_by_name(
    file_id: str,
    page_id: str,
    shape_identifier: str,
) -> str:
    """Resolve a shape identifier to its UUID.

    If the identifier is already a valid UUID, returns it as-is.
    If it's a name, searches the page for a matching shape and returns its ID.

    Args:
        file_id: The file UUID.
        page_id: The page UUID.
        shape_identifier: Either a shape UUID or a shape name.

    Returns:
        The shape UUID.

    Raises:
        ValueError: If the shape is not found or identifier is invalid.
    """
    import uuid

    # Check if it's already a valid UUID
    try:
        uuid.UUID(shape_identifier)
        return shape_identifier
    except (ValueError, TypeError):
        pass

    # It's a name - search for it
    file_data = await api.command("get-file", {"id": file_id, "components-v2": True})
    objects = _get_page_objects(file_data, page_id)

    # Try exact match first
    for obj_id, obj in objects.items():
        if obj.get("name") == shape_identifier:
            return obj_id

    # Try case-insensitive match
    shape_lower = shape_identifier.lower()
    for obj_id, obj in objects.items():
        if obj.get("name", "").lower() == shape_lower:
            return obj_id

    raise ValueError(
        f"Shape not found: '{shape_identifier}'. Available shapes: {list(objects.keys())[:10]}..."
    )


async def resolve_shapes_by_names(
    file_id: str,
    page_id: str,
    shape_identifiers: list[str],
) -> list[str]:
    """Resolve multiple shape identifiers to UUIDs.

    Args:
        file_id: The file UUID.
        page_id: The page UUID.
        shape_identifiers: List of shape UUIDs or names.

    Returns:
        List of shape UUIDs.
    """
    return [
        await resolve_shape_by_name(file_id, page_id, identifier)
        for identifier in shape_identifiers
    ]
