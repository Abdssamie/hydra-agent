from abc import ABC
from typing import List
import json
from llama_index.core.storage.chat_store import BaseChatStore, SimpleChatStore
from llama_index.core.llms import ChatMessage
from pydantic import ConfigDict, PrivateAttr
import psycopg2


class PostgresChatStore(BaseChatStore, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # ✅ Allow non-Pydantic attributes

    _db_url: str = PrivateAttr()  # ✅ This prevents Pydantic from validating `db_url`
    _conn: psycopg2.extensions.connection = PrivateAttr()
    _cursor: psycopg2.extensions.cursor = PrivateAttr()

    def __init__(self, db_url: str):
        super().__init__()
        self._db_url = db_url
        self._conn = psycopg2.connect(self._db_url)
        self._cursor = self._conn.cursor()
        self._setup_table()

    @classmethod
    def class_name(cls) -> str:
        """Get class name."""
        return "PostgresChatStore"

    def _setup_table(self):
        """Create chat_messages table if it doesn't exist."""
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id SERIAL PRIMARY KEY,
                key TEXT NOT NULL,
                message JSONB NOT NULL
            )
        """)
        self._conn.commit()

    def set_messages(self, key: str, messages: List[ChatMessage]) -> None:
        """Store chat messages for a key (replaces old messages)."""
        with self._conn:
            with self._conn.cursor() as cursor:
                cursor.execute("DELETE FROM chat_messages WHERE key = %s", (key,))
                cursor.executemany(
                    "INSERT INTO chat_messages (key, message) VALUES (%s, %s)",
                    [(key, json.dumps(msg.model_dump())) for msg in messages]
                )

    def get_messages(self, key: str) -> List[ChatMessage]:
        """Retrieve chat messages for a key."""
        self._cursor.execute("SELECT message FROM chat_messages WHERE key = %s", (key,))
        rows = self._cursor.fetchall()
        return [ChatMessage(**row[0]) for row in rows if row[0] is not None]

    def add_message(self, key: str, message: ChatMessage) -> None:
        """Add a single chat message."""
        self._cursor.execute(
            "INSERT INTO chat_messages (key, message) VALUES (%s, %s)",
            [key, json.dumps(message.model_dump())]
        )
        self._conn.commit()

    def delete_last_message(self, key: str) -> None:
        """Delete the last chat message for a given key."""
        self._cursor.execute(
            "DELETE FROM chat_messages "
            "WHERE id = (SELECT id FROM chat_messages WHERE key = %s ORDER BY id DESC LIMIT 1)",
            (key,)
        )
        self._conn.commit()

    def delete_messages(self, key: str) -> None:
        """Delete all messages for a key."""
        self._cursor.execute("DELETE FROM chat_messages WHERE key = %s", (key,))
        self._conn.commit()

    def get_keys(self) -> List[str]:
        """Get all chat keys."""
        self._cursor.execute("SELECT DISTINCT key FROM chat_messages")
        keys = [row[0] for row in self._cursor.fetchall()]
        return keys

    def delete_message(self, key: str, idx: int) -> None:
        """Delete a message at a specific index."""
        self._cursor.execute("""
            DELETE FROM chat_messages 
            WHERE id = (
                SELECT id FROM chat_messages 
                WHERE key = %s 
                ORDER BY id ASC 
                LIMIT 1 OFFSET %s
            ) 
            RETURNING id;
        """, (key, idx))

        deleted_row = self._cursor.fetchone()  # Fetch the deleted row's ID

        if deleted_row is None:
            print("Error: No message found at the given index.")  # Handle case when index is out of bounds
        else:
            self._conn.commit()
            print(f"Message at index {idx} deleted successfully.")

    def close(self):
        """Close the database connection."""
        self._conn.close()
