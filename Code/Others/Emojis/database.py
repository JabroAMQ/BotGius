"""
For reproducibility, this is how the Players's Table was created:

CREATE TABLE IF NOT EXISTS emojis (
    emoji_id INTEGER PRIMARY KEY,
    emoji_name TEXT UNIQUE NOT NULL,
    host_id INTEGER,
    is_join BOOLEAN NOT NULL,
    is_leave BOOLEAN NOT NULL,
    is_poll BOOLEAN NOT NULL
);
"""
import sqlite3

from Code.Utilities.database_connection_sqlite3 import connection_manager

class Emojis_Database:
    """Static class to handle connections with the Emojis Database."""
    
    @staticmethod
    @connection_manager
    def get_all_emojis(cur: sqlite3.Cursor = None) -> list[tuple[int, str, int | None, bool, bool, bool]]:
        """
        Return a list of tuple containing the Emoji's data with the following order:
        - `emoji_id`: `int`
        - `emoji_name`: `str`
        - `host_id`: `int | None`
        - `is_join`: `bool`
        - `is_leave`: `bool`
        - `is_poll`: `bool`
        
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        get_all_emojis_query = 'SELECT * FROM emojis'
        cur.execute(get_all_emojis_query)
        return [tuple(record) for record in cur.fetchall()]
    

    @staticmethod
    @connection_manager
    def add_custom_emoji(emoji_id: int, emoji_name: str, host_id: int, is_join: bool, cur: sqlite3.Cursor = None) -> bool:
        """
        Add a custom host emoji (Join or Leave).
        
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        add_emoji_query = 'INSERT INTO emojis (emoji_id, emoji_name, host_id, is_join, is_leave, is_poll) VALUES (?, ?, ?, ?, ?, ?)'
        cur.execute(add_emoji_query, (emoji_id, emoji_name, host_id, int(is_join), int(not is_join), 0))


    @staticmethod
    @connection_manager
    def delete_custom_emoji(emoji_id: int, cur: sqlite3.Cursor = None) -> bool:
        """
        Delete a custom host emoji (Join or Leave) given the `emoji_id`.
        
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        delete_emoji_query = 'DELETE FROM emojis WHERE emoji_id = ?'
        cur.execute(delete_emoji_query, (emoji_id,))