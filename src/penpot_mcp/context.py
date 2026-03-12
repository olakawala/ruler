"""Session context manager for Ruler MCP.

Tracks current file_id/page_id to reduce repetitive parameter passing.
Session-based (in-memory) - context persists until MCP server restart.
"""

from __future__ import annotations

import threading
from typing import Any


class ContextManager:
    """Thread-safe in-memory context store for MCP session."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._context: dict[str, Any] = {}
        self._history: list[dict[str, Any]] = []

    def set(
        self, file_id: str | None = None, page_id: str | None = None
    ) -> dict[str, Any]:
        """Set the current context.

        Args:
            file_id: The file UUID to set as current.
            page_id: The page UUID to set as current.

        Returns:
            The updated context.
        """
        with self._lock:
            if file_id is not None:
                self._context["file_id"] = file_id
            if page_id is not None:
                self._context["page_id"] = page_id
            self._context["_updated"] = True
            return self.get()

    def get(self) -> dict[str, Any]:
        """Get the current context.

        Returns:
            Dict with file_id, page_id, and metadata.
        """
        with self._lock:
            return {
                "file_id": self._context.get("file_id"),
                "page_id": self._context.get("page_id"),
                "has_context": bool(self._context.get("file_id")),
            }

    def clear(self) -> dict[str, Any]:
        """Clear the current context.

        Returns:
            Empty context dict.
        """
        with self._lock:
            self._context.clear()
            return {"file_id": None, "page_id": None, "has_context": False}

    def resolve(
        self, file_id: str | None = None, page_id: str | None = None
    ) -> tuple[str, str]:
        """Resolve file_id and page_id, using context as fallback.

        Args:
            file_id: Provided file_id, or None to use context.
            page_id: Provided page_id, or None to use context.

        Returns:
            Tuple of (file_id, page_id), resolved from context if not provided.

        Raises:
            ValueError: If neither provided nor in context.
        """
        with self._lock:
            resolved_file = file_id or self._context.get("file_id")
            resolved_page = page_id or self._context.get("page_id")

            if not resolved_file:
                raise ValueError(
                    "file_id required: provide it explicitly or set context first with ruler_set_context()"
                )
            if not resolved_page:
                raise ValueError(
                    "page_id required: provide it explicitly or set context first with ruler_set_context()"
                )

            return resolved_file, resolved_page


# Global singleton instance
context = ContextManager()


def resolve_context(
    file_id: str | None = None,
    page_id: str | None = None,
    use_context: bool = True,
) -> tuple[str, str]:
    """Resolve file_id and page_id, optionally using session context as fallback.

    Args:
        file_id: Provided file_id, or None to use context.
        page_id: Provided page_id, or None to use context.
        use_context: If True, fall back to context when not provided.

    Returns:
        Tuple of (file_id, page_id), resolved from context if not provided.

    Raises:
        ValueError: If neither provided nor in context.
    """
    if use_context:
        return context.resolve(file_id=file_id, page_id=page_id)
    else:
        if not file_id:
            raise ValueError("file_id required")
        if not page_id:
            raise ValueError("page_id required")
        return file_id, page_id
