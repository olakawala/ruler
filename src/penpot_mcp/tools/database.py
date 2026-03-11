"""Direct database query tool for advanced Penpot exploration.

Note: Penpot uses singular table names (e.g., 'file' not 'files',
'project' not 'projects', 'team' not 'teams').
"""

from __future__ import annotations

from penpot_mcp.services.db import db


async def query_database(sql: str) -> list[dict]:
    """Execute a read-only SQL query against the Penpot database.

    This is a power tool for advanced queries not covered by other tools.
    Only SELECT statements are allowed.

    Note: Penpot uses singular table names (e.g., 'file' not 'files').

    Args:
        sql: SQL SELECT query to execute.
    """
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        return [{"error": "Only SELECT queries are allowed for safety"}]

    # Block dangerous patterns
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    for word in forbidden:
        if f" {word} " in f" {normalized} " or normalized.startswith(word):
            return [{"error": f"Forbidden SQL keyword: {word}"}]

    # Check for common mistake: 'files' instead of 'file'
    if " from files " in f" {normalized} " or normalized.startswith(
        "select * from files"
    ):
        return [
            {
                "error": "Table 'files' does not exist. Penpot uses singular names. Try 'file' instead."
            }
        ]

    rows = await db.fetch(sql)
    # Convert non-serializable types
    result = []
    for row in rows:
        clean = {}
        for k, v in row.items():
            if hasattr(v, "isoformat"):
                clean[k] = v.isoformat()
            elif isinstance(v, bytes):
                clean[k] = f"<binary {len(v)} bytes>"
            elif isinstance(v, (dict, list, str, int, float, bool)) or v is None:
                clean[k] = v
            else:
                clean[k] = str(v)
        result.append(clean)
    return result


async def get_webhooks(team_id: str) -> list[dict]:
    """List webhooks configured for a team.

    Args:
        team_id: The team UUID.
    """
    rows = await db.get_webhooks(team_id)
    return [
        {
            "id": str(r["id"]),
            "uri": r["uri"],
            "mtype": r["mtype"],
            "is_active": r["is_active"],
            "error_code": r.get("error_code"),
            "error_count": r.get("error_count"),
            "created_at": r["created_at"].isoformat() if r["created_at"] else None,
        }
        for r in rows
    ]
