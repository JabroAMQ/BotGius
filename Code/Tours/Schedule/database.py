"""
For reproducibility, this is how the Scheduled_Tours's Table was created:

CREATE TABLE IF NOT EXISTS scheduled_tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    host TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    updated_at INTEGER
);
"""
import sqlite3

from Code.Utilities.database_connection_sqlite3 import connection_manager


class Scheduled_Tours_Database:
    """Static class to handle connections with the Players Database."""
    @staticmethod
    @connection_manager
    def _add_scheduled_tour(description: str, host: str, timestamp: int, created_at: int, cur: sqlite3.Cursor = None) -> None:
        """
        Add a new Scheduled_Tour to the Scheduled_Tours Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        add_scheduled_tour_query = 'INSERT INTO scheduled_tours (description, host, timestamp, created_at) VALUES (?, ?, ?, ?)'
        cur.execute(add_scheduled_tour_query, (description, host, timestamp, created_at))

    @staticmethod
    @connection_manager
    def _get_scheduled_tour_id(description: str, host: str, timestamp: int, cur: sqlite3.Cursor = None) -> int:
        """
        Return the Database's ID of a Scheduled_Tour given its `description`, `timestamp` and `host`.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        get_scheduled_tour_id_query = 'SELECT id FROM scheduled_tours WHERE description = ? AND host = ? AND timestamp = ?'
        cur.execute(get_scheduled_tour_id_query, (description, host, timestamp))
        id = cur.fetchone()[0]
        return id

    @staticmethod
    def add_scheduled_tour(description: str, host: str, timestamp: int, created_at: int, cur: sqlite3.Cursor = None) -> int:
        """
        Add a new Scheduled_Tour to the Scheduled_Tours Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        Scheduled_Tours_Database._add_scheduled_tour(description, host, timestamp, created_at)
        return Scheduled_Tours_Database._get_scheduled_tour_id(description, host, timestamp)


    @staticmethod
    @connection_manager
    def get_all_scheduled_tours(cur: sqlite3.Cursor = None) -> list[tuple[int, str, str, int, int, int]]:
        """
        Return a list of tuple containing the Scheduled_Tours's data with the following order:
        - `id`
        - `description`
        - `host`
        - `timestamp`
        - `created_at`
        - `updated_at`

        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        get_all_scheduled_tours_query = 'SELECT * FROM scheduled_tours'
        cur.execute(get_all_scheduled_tours_query)
        return [tuple(record) for record in cur.fetchall()]

    
    @staticmethod
    @connection_manager
    def delete_scheduled_tour(id: int, cur: sqlite3.Cursor = None) -> None:
        """
        Remove a Scheduled_Tour from the Scheduled_Tours Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        remove_scheduled_tour_query = 'DELETE FROM scheduled_tours WHERE id = ?'
        cur.execute(remove_scheduled_tour_query, (id,))