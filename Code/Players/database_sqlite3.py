"""
For reproducibility, this is how the Players's Table was created:

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY NOT NULL,
    amq TEXT UNIQUE NOT NULL,

    rank TEXT DEFAULT 'None',
    elo INTEGER DEFAULT 0,

    list_name TEXT,
    list_from TEXT,
    list_sections TEXT,

    fav_1v1 INTEGER,
    hated_1v1 INTEGER,
    fav_2v2 INTEGER,
    hated_2v2 INTEGER,
    fav_4v4 INTEGER,
    hated_4v4 INTEGER,

    is_banned BOOLEAN DEFAULT 0,

    FOREIGN KEY (fav_1v1) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (hated_1v1) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (fav_2v2) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (hated_2v2) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (fav_4v4) REFERENCES gamemodes(id) ON DELETE SET NULL,
    FOREIGN KEY (hated_4v4) REFERENCES gamemodes(id) ON DELETE SET NULL
);
"""

import sqlite3

from Code.Utilities.database_connection_sqlite3 import connection_manager


class Players_Database:
    """Static class to handle connections with the Players Database."""
    
    @staticmethod
    @connection_manager
    def get_all_players(cur: sqlite3.Cursor = None) \
        -> list[tuple[int, str, str, int, str | None, str | None, str | None, int | None, int | None, int | None, int | None, int | None, int | None, bool]]:
        """
        Return a list of tuple containing the Players's data with the following order:
        - `discord_id`
        - `amq_name`
        - `rank`
        - `elo`
        - `list_name`
        - `list_from`
        - `list_sections`
        - `fav_1v1_gamemode_id`
        - `hated_1v1_gamemode_id`
        - `fav_2v2_gamemode_id`
        - `hated_2v2_gamemode_id`
        - `fav_4v4_gamemode_id`
        - `hated_4v4_gamemode_id`
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

    @staticmethod
    @connection_manager
    def change_player_list_data(
        discord_id: int,
        new_list_name: str,
        new_list_from: str,
        new_list_sections: str,
        cur: sqlite3.Cursor = None
    ) -> None:
        """
        Change the Player's list information from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_list_data_query = '''
            UPDATE players
            SET list_name = ?, list_from = ?, list_sections = ?
            WHERE id = ?
        '''
        player = (new_list_name, new_list_from, new_list_sections, discord_id)
        cur.execute(change_player_list_data_query, player)

    @staticmethod
    @connection_manager
    def change_player_preferred_gamemodes_data(
        discord_id: int,
        new_fav_1v1_gamemode_id: int,
        new_fav_2v2_gamemode_id: int,
        new_fav_4v4_gamemode_id: int,
        new_hated_1v1_gamemode_id: int,
        new_hated_2v2_gamemode_id: int,
        new_hated_4v4_gamemode_id: int,
        cur: sqlite3.Cursor = None
    ) -> None:
        """
        Change the Player's preferred gamemodes from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_preferred_gamemodes_data_query = '''
            UPDATE players
            SET fav_1v1 = ?, fav_2v2 = ?, fav_4v4 = ?, hated_1v1 = ?, hated_2v2 = ?, hated_4v4 = ?
            WHERE id = ?
        '''
        player = (new_fav_1v1_gamemode_id, new_fav_2v2_gamemode_id, new_fav_4v4_gamemode_id, new_hated_1v1_gamemode_id, new_hated_2v2_gamemode_id, new_hated_4v4_gamemode_id, discord_id)
        cur.execute(change_player_preferred_gamemodes_data_query, player)