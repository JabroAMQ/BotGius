from os import getenv

import psycopg2, psycopg2.extras, psycopg2.extensions
from dotenv import load_dotenv

"""
For reproducibility, this is how the Gamemodes's Table was created:

CREATE TABLE IF NOT EXISTS gamemodes(
	
	name VARCHAR(50) UNIQUE NOT NULL,
	size INT NOT NULL,
	code VARCHAR(200) NOT NULL,
	
	watched BOOL NOT NULL,
	random BOOL NOT NULL,
	weighted BOOL NOT NULL,
	equal BOOL NOT NULL,

    id SERIAL PRIMARY KEY
);
"""

class Gamemodes_Database:
    """Static class to handle connections with the Gamemodes Database."""
    load_dotenv()
    _HOST = getenv('DATABASE_HOST')
    _DBNAME = getenv('DATABASE_NAME')
    _USER = getenv('DATABASE_USER')
    _PORT = getenv('DATABASE_PORT')
    _PASSWORD = getenv('DATABASE_PASSWORD')


    def _connection_manager(func : callable) -> callable:
        """
        Decorator to handle connections with the Gamemodes Database.
        :param func: The function to decorate
        :return: The decorated function

        This decorator establishes a connection with the Database, creates a cursor, and passes it to the decorated function.
        It then commits the changes and closes the connection after the function has completed.
        If an exception is raised, it rolls back the changes and raises the exception.

        Note:
        -----
        The changes will only be commited to the database once all the `func` function's lines (instructions) had been completed.\n
        This means that in the same function you can't, for instance, add a gamemode and then try to retrieve some of its data (its id, for example)
        from the database as the gamemode isn't stored in the database untill the commit is executed. Therefore you will need to split this functionallity
        into 2 different functions so you can: `1.- Add Gamemode; 2.- Commit; 3.- Retrieve data from Gamemode added`.
        """
        def wrapper(*args, **kwargs):
            conn, cur = Gamemodes_Database._connect_to_database()
            try:
                result = func(*args, **kwargs, cur=cur)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                Gamemodes_Database._close_connection(conn, cur)
            return result
        return wrapper
    

    @staticmethod
    def _connect_to_database() -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
        """Method in charge of establishing a connection with the Gamemodes Database."""
        conn = psycopg2.connect(
            host = Gamemodes_Database._HOST,
            dbname = Gamemodes_Database._DBNAME,
            user = Gamemodes_Database._USER,
            port = Gamemodes_Database._PORT,
            password = Gamemodes_Database._PASSWORD
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cur

    @staticmethod
    def _close_connection(conn : psycopg2.extensions.connection, cur : psycopg2.extensions.cursor) -> None:
        """Method in charge of closing the connection with the Gamemodes Database."""
        cur.close()
        conn.close()


    @staticmethod
    @_connection_manager
    def _add_gamemode(
        name : str,
        size : int,
        code : str,
        watched_song_selection : bool,
        random_song_distribution : bool,
        weighted_song_distribution : bool,
        equal_song_distribution : bool,
        cur : psycopg2.extensions.cursor = None
    ) -> None:
        """
        Add a new Gamemode to the Gamemodes Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.\n
        Gamemode data stored = `(name, size, code, watched_song_selection, random_song_distribution, weighted_song_distribution, equal_song_distribution, id)`.\n
        `id` will be calculated automatically by the database.
        """
        sql_add_gamemode = 'INSERT INTO gamemodes (name, size, code, watched, random, weighted, equal) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        gamemode = (name, size, code, watched_song_selection, random_song_distribution, weighted_song_distribution, equal_song_distribution)
        cur.execute(sql_add_gamemode, gamemode)

    @staticmethod
    @_connection_manager
    def _get_gamemode_id(name : str, cur : psycopg2.extensions.cursor = None) -> int:
        """
        Return the Database's ID of a Gamemode given its `name`.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        sql_get_gamemode_id = 'SELECT id FROM gamemodes WHERE name = %s'
        gamemode = (name,)
        cur.execute(sql_get_gamemode_id, gamemode)
        id = cur.fetchone()[0]
        return id
    
    @staticmethod
    def add_gamemode(
        name : str,
        size : int,
        code : str,
        watched_song_selection : bool,
        random_song_distribution : bool,
        weighted_song_distribution : bool,
        equal_song_distribution : bool
    ) -> int:
        """
        Add a new Gamemode to the Gamemodes Database.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.\n
        Gamemode data stored = `(id, name, size, code, watched_song_selection, random_song_distribution, weighted_song_distribution, equal_song_distribution)`.\n
        The gamemode's `id`, which is calculated automatically by the database, will be returned.
        """
        Gamemodes_Database._add_gamemode(name, size, code, watched_song_selection, random_song_distribution, weighted_song_distribution, equal_song_distribution)
        return Gamemodes_Database._get_gamemode_id(name)

    @staticmethod
    @_connection_manager
    def get_all_gamemodes(cur : psycopg2.extensions.cursor = None) -> list[tuple[str, int, str, bool, bool, bool, bool, int]]:
        """
        Return all the Gamemodes stored in the Database as tuples containing:
        - `name` : `str`
            The Gamemode's name.
        - `size` : `int`
            How many players per team does the Gamemode require.
        - `code` : `str`
            The Code to set the Gamemode's rules in the AMQ lobby.
        - `watched_song_selection` : `bool`
            Whether the gamemode has watched (or random) song selection.
        - `random_song_distribution` : `bool`
            Whether the gamemode has random song distribution as a possible distribution roll.
        - `weighted_song_distribution` : `bool`
            Whether the gamemode has weighted song distribution as a possible distribution roll.
        - `equal_song_distribution` : `bool`
            Whether the gamemode has equal song distribution as a possible distribution roll.
        - `id` : `int`
            The Gamemode's ID in the database.

        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        sql_get_all_gamemodes = 'SELECT * FROM gamemodes'
        cur.execute(sql_get_all_gamemodes)
        return [tuple(record) for record in cur.fetchall()]
    

    @staticmethod
    @_connection_manager
    def delete_gamemode(name : str, cur : psycopg2.extensions.cursor = None) -> None:
        """
        Delete a Gamemode from the Database given its `name`.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        sql_delete_gamemode = 'DELETE FROM gamemodes WHERE name = %s'
        gamemode = (name,)
        cur.execute(sql_delete_gamemode, gamemode)

    
    @staticmethod
    @_connection_manager
    def edit_gamemode(
        id : int,
        new_name : str,
        new_code : str,
        new_random_song_distribution : bool,
        new_weighted_song_distribution : bool,
        new_equal_song_distribution : bool,
        cur : psycopg2.extensions.cursor = None
    ) -> None:
        """
        Given a gamemode `id`, modify the gamemode related with the `new_...` provided values.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.\n
        """
        sql_edit_gamemode = '''
            UPDATE gamemodes
            SET name = %s, code = %s,random = %s, weighted = %s, equal = %s
            WHERE id = %s
        '''
        gamemode = (new_name, new_code, new_random_song_distribution, new_weighted_song_distribution, new_equal_song_distribution, id)
        cur.execute(sql_edit_gamemode, gamemode)