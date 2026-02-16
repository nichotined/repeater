from datetime import datetime, timezone
from pathlib import Path
import sqlite3


class Database:
    def __init__(self, database: str = "local.db"):
        self.database = database
        self.connection: sqlite3.Connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.database)

    def init_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS histories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        data TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
        )
        self.connection.commit()

    def get_by_name(self, name: str):
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT id, name, data FROM histories where name like '%{name}%'"
        )
        data = cursor.fetchall()
        if data:
            return data
        else:
            print(f"No data matching {name}")
            return None

    def fetch_one_by_name(self, name: str):
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT id, name, data FROM histories where name like '%{name}%'"
        )
        data = cursor.fetchone()
        if data:
            return data
        else:
            print(f"No data matching {name}")
            return None

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, name FROM histories")
        data = cursor.fetchall()
        if data:
            return data
        else:
            print(f"Database looks empty")
            return None

    def append(self, name: str, data: str):
        now = datetime.now(timezone.utc).isoformat()
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO histories (name, data, created_at) VALUES (?, ?, ?)",
            (name, data, now),
        )
        self.connection.commit()
