import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime


def extract_prompt_from_trajectory(task_dir: Path) -> str:
    """从 trajectory.json 中提取 instruction 字段并去除 <task> 标签。"""
    traj_path = task_dir / "trajectory.json"
    if not traj_path.exists():
        return ""
    try:
        with open(traj_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return ""
    if isinstance(data, dict):
        instruction = data.get("instruction", "")
    elif isinstance(data, list) and len(data) > 0:
        instruction = data[0].get("instruction", "")
    else:
        return ""
    if not instruction:
        return ""
    instruction = re.sub(r'^<task>\s*', '', instruction)
    instruction = re.sub(r'\s*</task>\s*$', '', instruction)
    return instruction.strip()

DB_PATH = Path(__file__).parent / "results.db"


def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qc_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_name TEXT NOT NULL,
            passed INTEGER NOT NULL,
            failure_reason TEXT,
            batch_num TEXT,
            created_at TEXT NOT NULL,
            prompt TEXT
        )
    """)
    conn.commit()
    conn.close()


def _migrate_db():
    """Add missing columns to existing database."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE qc_results ADD COLUMN prompt TEXT")
    except sqlite3.OperationalError:
        pass  # column already exists
    conn.commit()
    conn.close()


def save_result(data_name: str, passed: bool, failure_reason: str = "", batch_num: str = "", prompt: str = ""):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO qc_results (data_name, passed, failure_reason, batch_num, created_at, prompt) VALUES (?, ?, ?, ?, ?, ?)",
        (data_name, 1 if passed else 0, failure_reason, batch_num, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prompt)
    )
    conn.commit()
    conn.close()
