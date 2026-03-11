"""
Versioning Module

Provides checkpoint functionality for AI workflows.
"""

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class CheckpointService:
    """Manages checkpoints for design versions."""

    def __init__(self, db_path: str):
        """Initialize the checkpoint service."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                id TEXT PRIMARY KEY,
                file_id TEXT NOT NULL,
                penpot_snapshot_id TEXT,
                label TEXT NOT NULL,
                description TEXT,
                ai_prompt TEXT,
                model_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_checkpoints_file_id 
            ON checkpoints(file_id)
        """)

        conn.commit()
        conn.close()

    async def create_checkpoint(
        self,
        file_id: str,
        label: str,
        description: str = "",
        ai_prompt: str = "",
        model_used: str = "",
    ) -> str:
        """Create a new checkpoint."""
        checkpoint_id = str(uuid.uuid4())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO checkpoints 
            (id, file_id, label, description, ai_prompt, model_used)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (checkpoint_id, file_id, label, description, ai_prompt, model_used),
        )

        conn.commit()
        conn.close()

        return checkpoint_id

    async def list_checkpoints(self, file_id: str) -> List[Dict]:
        """List all checkpoints for a file."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, file_id, label, description, ai_prompt, model_used, created_at
            FROM checkpoints
            WHERE file_id = ?
            ORDER BY created_at DESC
        """,
            (file_id,),
        )

        rows = cursor.fetchall()
        conn.close()

        checkpoints = []
        for row in rows:
            checkpoints.append(
                {
                    "id": row[0],
                    "file_id": row[1],
                    "label": row[2],
                    "description": row[3],
                    "ai_prompt": row[4],
                    "model_used": row[5],
                    "created_at": row[6],
                }
            )

        return checkpoints

    async def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore a file to a checkpoint."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT penpot_snapshot_id FROM checkpoints WHERE id = ?
        """,
            (checkpoint_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row and row[0]:
            return True

        return False

    async def compare_checkpoints(
        self, checkpoint_id_1: str, checkpoint_id_2: str
    ) -> Dict:
        """Compare two checkpoints."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, label, ai_prompt, created_at 
            FROM checkpoints 
            WHERE id IN (?, ?)
        """,
            (checkpoint_id_1, checkpoint_id_2),
        )

        rows = cursor.fetchall()
        conn.close()

        if len(rows) != 2:
            return {"error": "One or both checkpoints not found"}

        return {
            "checkpoint_1": {
                "id": rows[0][0],
                "label": rows[0][1],
                "ai_prompt": rows[0][2],
                "created_at": rows[0][3],
            },
            "checkpoint_2": {
                "id": rows[1][0],
                "label": rows[1][1],
                "ai_prompt": rows[1][2],
                "created_at": rows[1][3],
            },
            "comparison": "Visual comparison not yet implemented",
        }
