import os
from abc import ABC
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


class AbstractRepository(ABC):
    """Abstract repository providing database connection management."""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self, conn):
        """Context manager for database cursors with dict-like results."""
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
        finally:
            cursor.close()
