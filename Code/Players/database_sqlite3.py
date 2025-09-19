"""
For reproducibility, this is how the Players's Table was created:

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY NOT NULL,
    amq TEXT UNIQUE NOT NULL,
    rank TEXT DEFAULT 'None',
    is_banned BOOLEAN DEFAULT 0
);
"""
import sqlite3

from Code.Utilities.database_connection_sqlite3 import connection_manager

class Players_Database:
    """Static class to handle connections with the Players Database."""
    
    @staticmethod
    @connection_manager
    def get_all_players(cur: sqlite3.Cursor = None) -> list[tuple[int, str, str, bool]]:
        """
        Return a list of tuple containing the Players's data with the following order:
        - `discord_id`
        - `amq_name`
        - `rank`
        - `is_banned`
        
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        get_all_players_query = 'SELECT * FROM players'
        cur.execute(get_all_players_query)
        return [tuple(record) for record in cur.fetchall()]
    
    @staticmethod
    @connection_manager
    def add_player(discord_id: int, amq_name: str, cur: sqlite3.Cursor = None) -> None:
        """
        Add a new Player to the Players Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        add_player_query = 'INSERT INTO players (id, amq) VALUES (?, ?)'
        cur.execute(add_player_query, (discord_id, amq_name))


    @staticmethod
    @connection_manager
    def change_player_amq(discord_id: int, new_amq_name: str, cur: sqlite3.Cursor = None) -> None:
        """
        Change the Player's amq name to `new_amq_name` from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_amq_query = 'UPDATE players SET amq = ? WHERE id = ?'
        player = (new_amq_name, discord_id)
        cur.execute(change_player_amq_query, player)

    @staticmethod
    @connection_manager
    def change_player_rank(discord_id: int, new_rank: str, cur: sqlite3.Cursor = None) -> None:
        """
        Change the Player's rank to `new_rank` from the `discord_id` player in the Player's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_rank_query = 'UPDATE players SET rank = ? WHERE id = ?'
        player = (new_rank, discord_id)
        cur.execute(change_player_rank_query, player)

    @staticmethod
    @connection_manager
    def change_is_baned(discord_id: int, is_banned: bool, cur: sqlite3.Cursor = None) -> None:
        """
        Change the Player's "is_banned" attribute to `is_banned` from the `discord_id` player in the Player's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_is_banned_query = 'UPDATE players SET is_banned = ? WHERE id = ?'
        player = (is_banned, discord_id)
        cur.execute(change_player_is_banned_query, player)