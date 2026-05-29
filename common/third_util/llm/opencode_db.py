import json
import os
import sqlite3
import time

from typing import Optional


class OpencodeDb:
    DB_PATH = "~/.local/share/opencode/opencode.db"

    _conn: sqlite3.Connection

    _CAMEL_TO_SNAKE = {
        "sessionID": "session_id",
        "messageID": "message_id",
        "callID": "call_id",
        "modelID": "api_model_id",
        "providerID": "provider_id",
    }

    def __init__(self, db_path: Optional[str] = None):
        path = db_path or os.path.expanduser(self.DB_PATH)
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row

    def get_session(self, session_id: str) -> Optional[dict]:
        row = self._conn.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_sessions(
        self, directory: Optional[str] = None, limit: int = 20
    ) -> list[dict]:
        if directory:
            rows = self._conn.execute(
                "SELECT * FROM session WHERE directory = ? ORDER BY time_created DESC LIMIT ?",
                (directory, limit),
            )
        else:
            rows = self._conn.execute(
                "SELECT * FROM session ORDER BY time_created DESC LIMIT ?", (limit,)
            )
        return [dict(r) for r in rows.fetchall()]

    def get_messages(self, session_id: str) -> list[dict]:
        rows = self._conn.execute(
            "SELECT id, data FROM message WHERE session_id = ? ORDER BY time_created",
            (session_id,),
        ).fetchall()

        result = []
        for row in rows:
            msg_id = row["id"]
            msg_data = json.loads(row["data"])
            info = self._convert_keys(msg_data)

            part_rows = self._conn.execute(
                "SELECT data FROM part WHERE message_id = ? ORDER BY time_created",
                (msg_id,),
            ).fetchall()

            parts = [self._convert_keys(json.loads(pr["data"])) for pr in part_rows]
            result.append({"info": info, "parts": parts})

        return result

    def has_data(self, session_id: str) -> bool:
        row = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM message WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        return row["cnt"] > 0

    def has_assistant_messages(self, session_id: str) -> bool:
        row = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM part p JOIN message m ON p.message_id = m.id WHERE m.session_id = ? AND json_extract(p.data, '$.type') = 'text'",
            (session_id,),
        ).fetchone()
        return row["cnt"] > 0

    def get_session_duration(self, session_id: str) -> Optional[int]:
        rows = self._conn.execute(
            "SELECT MIN(time_created) as t1, MAX(time_created) as t2 FROM part WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if rows and rows["t1"] and rows["t2"]:
            return int((rows["t2"] - rows["t1"]) / 1000)
        return None

    def get_tool_stats(self, session_id: str) -> dict:
        rows = self._conn.execute(
            "SELECT json_extract(data, '$.tool') as tool_name, COUNT(*) as cnt FROM part WHERE session_id = ? AND json_extract(data, '$.type') = 'tool' GROUP BY tool_name ORDER BY cnt DESC",
            (session_id,),
        ).fetchall()
        return {r["tool_name"]: r["cnt"] for r in rows}

    def get_message_count(self, session_id: str) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM message WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        return row["cnt"]

    def wait_for_data(
        self, session_id: str, timeout: int = 900, interval: float = 1.0
    ) -> list[dict]:
        start = time.time()
        while time.time() - start < timeout:
            if self.has_assistant_messages(session_id):
                return self.get_messages(session_id)
            time.sleep(interval)
        return []

    def _convert_keys(self, data: dict) -> dict:
        result = {}
        for k, v in data.items():
            new_k = self._CAMEL_TO_SNAKE.get(k, k)
            result[new_k] = v
        return result
