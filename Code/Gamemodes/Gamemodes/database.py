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

import psycopg2, psycopg2.extras, psycopg2.extensions

from Code.Utilities.database_connection import connection_manager


class Gamemodes_Database:
    """Static class to handle connections with the Gamemodes Database."""

    @staticmethod
    @connection_manager
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
    @connection_manager
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
    @connection_manager
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
    @connection_manager
    def delete_gamemode(name : str, cur : psycopg2.extensions.cursor = None) -> None:
        """
        Delete a Gamemode from the Database given its `name`.\n
        Do NOT add a `cur` value, its a placeholder which value will be replaced.
        """
        sql_delete_gamemode = 'DELETE FROM gamemodes WHERE name = %s'
        gamemode = (name,)
        cur.execute(sql_delete_gamemode, gamemode)


    @staticmethod
    @connection_manager
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