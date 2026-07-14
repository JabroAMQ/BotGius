import asyncpg

from Code.Utilities.database_connection_postgreql import connection_manager


class Emojis_Database:
    """Static class to handle connections with the Emojis Database."""
    
    @staticmethod
    @connection_manager
    async def get_all_emojis(conn: asyncpg.Connection = None) -> list[tuple[int, str, int | None, bool, bool, bool]]:
        """
        Return a list of tuples containing the Emoji's data with the following order:
        - `emoji_id`: `int`
        - `emoji_name`: `str`
        - `host_id`: `int | None`
        - `is_join`: `bool`
        - `is_leave`: `bool`
        - `is_poll`: `bool`
        
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        get_all_emojis_query = 'SELECT emoji_id, emoji_name, host_id, is_join, is_leave, is_poll FROM emojis'
        records = await conn.fetch(get_all_emojis_query)
        return [tuple(record) for record in records]
    

    @staticmethod
    @connection_manager
    async def add_custom_emoji(emoji_id: int, emoji_name: str, host_id: int, is_join: bool, conn: asyncpg.Connection = None) -> None:
        """
        Add a custom host emoji (Join or Leave).
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        add_emoji_query = '''
            INSERT INTO emojis (emoji_id, emoji_name, host_id, is_join, is_leave, is_poll) 
            VALUES ($1, $2, $3, $4, $5, $6)
        '''
        await conn.execute(add_emoji_query, emoji_id, emoji_name, host_id, is_join, not is_join, False)


    @staticmethod
    @connection_manager
    async def delete_custom_emoji(emoji_id: int, conn: asyncpg.Connection = None) -> None:
        """
        Delete a custom host emoji (Join or Leave) given the `emoji_id`.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        delete_emoji_query = 'DELETE FROM emojis WHERE emoji_id = $1'
        await conn.execute(delete_emoji_query, emoji_id)