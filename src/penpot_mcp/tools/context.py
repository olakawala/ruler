"""Context management tools - set, get, clear session context."""

from __future__ import annotations

from penpot_mcp.context import context


async def set_context(file_id: str, page_id: str | None = None) -> dict:
    """Set the current context for subsequent operations.

    This lets you avoid passing file_id and page_id to every tool.
    The context persists for the duration of the MCP server session.

    Args:
        file_id: The file UUID to set as current.
        page_id: Optional page UUID. If not provided, you must set it later.

    Returns:
        The current context after setting.

    Example:
        # Set context once
        set_context(file_id="abc-123", page_id="xyz-789")

        # Later calls can omit file_id and page_id (if using use_context=True)
        get_page_objects(page_id="xyz-789")  # uses file_id from context
    """
    result = context.set(file_id=file_id, page_id=page_id)
    return {
        "status": "ok",
        "file_id": result["file_id"],
        "page_id": result["page_id"],
        "message": "Context updated. Use ruler_get_context() to see current context.",
    }


async def get_context() -> dict:
    """Get the current session context.

    Returns:
        Current file_id and page_id if set, or null values if not set.

    Example:
        ctx = get_context()
        if ctx["has_context"]:
            print(f"Working with file: {ctx['file_id']}")
    """
    result = context.get()
    return {
        "file_id": result["file_id"],
        "page_id": result["page_id"],
        "has_context": result["has_context"],
    }


async def clear_context() -> dict:
    """Clear the current session context.

    Returns:
        Confirmation that context was cleared.

    Example:
        clear_context()  # Reset to no context
    """
    context.clear()
    return {
        "status": "ok",
        "message": "Context cleared. All context values are now null.",
        "file_id": None,
        "page_id": None,
        "has_context": False,
    }
