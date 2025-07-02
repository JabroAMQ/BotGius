"""
For reproducibility, this is how the Players's Table was created:

CREATE TABLE IF NOT EXISTS players(

	id	BIGINT PRIMARY KEY NOT NULL,
	amq	VARCHAR(50) UNIQUE NOT NULL,
	
	rank VARCHAR(20) DEFAULT 'None',
	elo INT DEFAULT 0,
	
	list_name VARCHAR(50),
	list_from VARCHAR(20),
	list_sections VARCHAR(20),
	
	fav_1v1 INT,
	FOREIGN KEY (fav_1v1)
	REFERENCES gamemodes (id)
	ON DELETE SET NULL,
	
	hated_1v1 INT,
	FOREIGN KEY (hated_1v1)
	REFERENCES gamemodes (id)
	ON DELETE SET NULL,
	
	fav_2v2 INT,
	FOREIGN KEY (fav_2V2)
	REFERENCES gamemodes (id)
	ON DELETE SET NULL,
	
	hated_2v2 INT,
	FOREIGN KEY (hated_2v2)
	REFERENCES gamemodes (id)
	ON DELETE SET NULL,
	
	fav_4v4 INT,
	FOREIGN KEY (fav_4v4)
	REFERENCES gamemodes (id)
	ON DELETE SET NULL,
	
	hated_4v4 INT,
	FOREIGN KEY (hated_4v4)
	REFERENCES gamemodes (id)
	ON DELETE SET NULL,

    is_banned BOOL DEFAULT False
);
"""

import psycopg2, psycopg2.extensions

from Code.Utilities.database_connection_postgreql import connection_manager


class Players_Database:
    """Static class to handle connections with the Players Database."""
    
    @staticmethod
    @connection_manager
    def get_all_players(cur: psycopg2.extensions.cursor = None) \
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
    def add_player(discord_id: int, amq_name: str, cur: psycopg2.extensions.cursor = None) -> None:
        """
        Add a new Player to the Players Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        add_player_query = 'INSERT INTO players (id, amq) VALUES (%s, %s)'
        cur.execute(add_player_query, (discord_id, amq_name))


    @staticmethod
    @connection_manager
    def change_player_amq(discord_id: int, new_amq_name: str, cur: psycopg2.extensions.cursor = None) -> None:
        """
        Change the Player's amq name to `new_amq_name` from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_amq_query = 'UPDATE players SET amq = %s WHERE id = %s'
        player = (new_amq_name, discord_id)
        cur.execute(change_player_amq_query, player)

    @staticmethod
    @connection_manager
    def change_player_rank(discord_id: int, new_rank: str, cur: psycopg2.extensions.cursor = None) -> None:
        """
        Change the Player's rank to `new_rank` from the `discord_id` player in the Player's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_rank_query = 'UPDATE players SET rank = %s WHERE id = %s'
        player = (new_rank, discord_id)
        cur.execute(change_player_rank_query, player)

    @staticmethod
    @connection_manager
    def change_is_baned(discord_id: int, is_banned: bool, cur: psycopg2.extensions.cursor = None) -> None:
        """
        Change the Player's "is_banned" attribute to `is_banned` from the `discord_id` player in the Player's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_is_banned_query = 'UPDATE players SET is_banned = %s WHERE id = %s'
        player = (is_banned, discord_id)
        cur.execute(change_player_is_banned_query, player)

    @staticmethod
    @connection_manager
    def change_player_list_data(
        discord_id: int,
        new_list_name: str,
        new_list_from: str,
        new_list_sections: str,
        cur: psycopg2.extensions.cursor = None
    ) -> None:
        """
        Change the Player's list information from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_list_data_query = '''
            UPDATE players
            SET list_name = %s, list_from = %s, list_sections = %s
            WHERE id = %s
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
        cur: psycopg2.extensions.cursor = None
    ) -> None:
        """
        Change the Player's preferred gamemodes from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_preferred_gamemodes_data_query = '''
            UPDATE players
            SET fav_1v1 = %s, fav_2v2 = %s, fav_4v4 = %s, hated_1v1 = %s, hated_2v2 = %s, hated_4v4 = %s
            WHERE id = %s
        '''
        player = (new_fav_1v1_gamemode_id, new_fav_2v2_gamemode_id, new_fav_4v4_gamemode_id, new_hated_1v1_gamemode_id, new_hated_2v2_gamemode_id, new_hated_4v4_gamemode_id, discord_id)
        cur.execute(change_player_preferred_gamemodes_data_query, player)