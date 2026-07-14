import asyncpg

from Code.Utilities.database_connection_postgreql import connection_manager

class Gamemodes_Database:
    """Static class to handle connections with the Gamemodes Database."""

    @staticmethod
    @connection_manager
    async def add_gamemode(
        name: str,
        size: int,
        code: str,
        watched_song_selection: bool,
        random_song_distribution: bool,
        weighted_song_distribution: bool,
        equal_song_distribution: bool,
        conn: asyncpg.Connection = None
    ) -> int:
        """
        Add a new Gamemode to the Gamemodes Database and return its auto-generated ID.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        sql_add_gamemode = '''
            INSERT INTO gamemodes (name, size, code, watched, random, weighted, equal) 
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        '''
        new_id = await conn.fetchval(sql_add_gamemode, name, size, code, watched_song_selection, random_song_distribution, weighted_song_distribution, equal_song_distribution)
        return new_id


    @staticmethod
    @connection_manager
    async def get_all_gamemodes(conn: asyncpg.Connection = None) -> list[tuple[str, int, str, bool, bool, bool, bool, int]]:
        """
        Return all the Gamemodes stored in the Database as tuples.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        sql_get_all_gamemodes = 'SELECT name, size, code, watched, random, weighted, equal, id FROM gamemodes'
        records = await conn.fetch(sql_get_all_gamemodes)        
        return [tuple(record) for record in records]


    @staticmethod
    @connection_manager
    async def delete_gamemode(name: str, conn: asyncpg.Connection = None) -> None:
        """
        Delete a Gamemode from the Database given its `name`.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        sql_delete_gamemode = 'DELETE FROM gamemodes WHERE name = $1'        
        await conn.execute(sql_delete_gamemode, name)


    @staticmethod
    @connection_manager
    async def edit_gamemode(
        id: int,
        new_name: str,
        new_code: str,
        new_random_song_distribution: bool,
        new_weighted_song_distribution: bool,
        new_equal_song_distribution: bool,
        conn: asyncpg.Connection = None
    ) -> None:
        """
        Given a gamemode `id`, modify the gamemode related with the `new_...` provided values.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        sql_edit_gamemode = '''
            UPDATE gamemodes
            SET name = $1, code = $2, random = $3, weighted = $4, equal = $5
            WHERE id = $6
        '''        
        await conn.execute(sql_edit_gamemode, new_name, new_code, new_random_song_distribution, new_weighted_song_distribution, new_equal_song_distribution, id)