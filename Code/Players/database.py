from os import getenv

import psycopg2, psycopg2.extras, psycopg2.extensions
from dotenv import load_dotenv

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
	ON DELETE SET NULL
);
"""

class Players_Database:
    """Static class to handle connections with the Players Database."""
    load_dotenv()
    _HOST = getenv('DATABASE_HOST')
    _DBNAME = getenv('DATABASE_NAME')
    _USER = getenv('DATABASE_USER')
    _PORT = getenv('DATABASE_PORT')
    _PASSWORD = getenv('DATABASE_PASSWORD')


    def _connection_manager(func : callable) -> callable:
        """
        Decorator to handle connections with the Players Database.
        :param func: The function to decorate
        :return: The decorated function

        This decorator establishes a connection with the Database, creates a cursor, and passes it to the decorated function.
        It then commits the changes and closes the connection after the function has completed.
        If an exception is raised, it rolls back the changes and raises the exception.

        Note:
        -----
        The changes will only be commited to the database once all the `func` function's lines (instructions) had been completed.\n
        This means that in the same function you can't, for instance, add a player and then try to retrieve some of its data (its id, for example)
        from the database as the player isn't stored in the database untill the commit is executed. Therefore you will need to split this functionallity
        into 2 different functions so you can: `1.- Add Player; 2.- Commit; 3.- Retrieve data from Player added`.
        """
        def wrapper(*args, **kwargs):
            conn, cur = Players_Database._connect_to_database()
            try:
                result = func(*args, **kwargs, cur=cur)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                Players_Database._close_connection(conn, cur)
            return result
        return wrapper
    

    @staticmethod
    def _connect_to_database() -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
        """Method in charge of establishing a connection with the Players Database."""
        conn = psycopg2.connect(
            host = Players_Database._HOST,
            dbname = Players_Database._DBNAME,
            user = Players_Database._USER,
            port = Players_Database._PORT,
            password = Players_Database._PASSWORD
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cur

    @staticmethod
    def _close_connection(conn : psycopg2.extensions.connection, cur : psycopg2.extensions.cursor) -> None:
        """Method in charge of closing the connection with the Players Database."""
        cur.close()
        conn.close()

    
    @staticmethod
    @_connection_manager
    def get_all_players(cur : psycopg2.extensions.cursor = None) \
        -> list[tuple[int, str, str, int, str | None, str | None, str | None, int | None, int | None, int | None, int | None, int | None, int | None]]:
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
        
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        get_all_players_query = 'SELECT * FROM players'
        cur.execute(get_all_players_query)
        return [tuple(record) for record in cur.fetchall()]
    
    @staticmethod
    @_connection_manager
    def add_player(discord_id : int, amq_name : str, cur : psycopg2.extensions.cursor = None) -> None:
        """
        Add a new Player to the Players Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        add_player_query = 'INSERT INTO players (id, amq) VALUES (%s, %s)'
        cur.execute(add_player_query, (discord_id, amq_name))


    @staticmethod
    @_connection_manager
    def change_player_amq(discord_id : int, new_amq_name : str, cur : psycopg2.extensions.cursor = None) -> None:
        """
        Change the Player's amq name to `new_amq_name` from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_amq_query = 'UPDATE players SET amq = %s WHERE id = %s'
        player = (new_amq_name, discord_id)
        cur.execute(change_player_amq_query, player)

    @staticmethod
    @_connection_manager
    def change_player_rank(discord_id : int, new_rank : str, cur : psycopg2.extensions.cursor = None) -> None:
        """
        Change the Player's rank to `new_rank` from the `discord_id` player in the Playerd's Database.
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        change_player_rank_query = 'UPDATE players SET rank = %s WHERE id = %s'
        player = (new_rank, discord_id)
        cur.execute(change_player_rank_query, player)

    @staticmethod
    @_connection_manager
    def change_player_list_data(
        discord_id : int,
        new_list_name : str,
        new_list_from : str,
        new_list_sections : str,
        cur : psycopg2.extensions.cursor = None
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
    @_connection_manager
    def change_player_preferred_gamemodes_data(
        discord_id : int,
        new_fav_1v1_gamemode_id : int,
        new_fav_2v2_gamemode_id : int,
        new_fav_4v4_gamemode_id : int,
        new_hated_1v1_gamemode_id : int,
        new_hated_2v2_gamemode_id : int,
        new_hated_4v4_gamemode_id : int,
        cur : psycopg2.extensions.cursor = None
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