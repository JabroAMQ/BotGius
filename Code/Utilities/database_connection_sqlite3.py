import os
import sqlite3

DB_PATH = os.path.join('Database', 'database.db')

def _connect_to_database() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    return conn, cur

def _close_connection(conn: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    cur.close()
    conn.close()

def connection_manager(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        conn, cur = _connect_to_database()
        try:
            result = func(*args, **kwargs, cur=cur)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            _close_connection(conn, cur)
        return result
    return wrapper
