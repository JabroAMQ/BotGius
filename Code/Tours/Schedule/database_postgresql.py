import asyncpg

from Code.Utilities.database_connection_postgreql import connection_manager

class Scheduled_Tours_Database:
    """Static class to handle connections with the Scheduled_Tours Database."""

    @staticmethod
    @connection_manager
    async def add_scheduled_tour(
        guild_id: int, 
        description: str, 
        host: str, 
        timestamp: int, 
        created_at: int, 
        conn: asyncpg.Connection = None
    ) -> int:
        """
        Add a new Scheduled_Tour to the Scheduled_Tours Database and return its auto-generated ID.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        add_scheduled_tour_query = '''
            INSERT INTO scheduled_tours (guild_id, description, host, timestamp, created_at) 
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        '''
        tour_id = await conn.fetchval(
            add_scheduled_tour_query, 
            guild_id, 
            description, 
            host, 
            timestamp, 
            created_at
        )
        return tour_id


    @staticmethod
    @connection_manager
    async def get_all_scheduled_tours(conn: asyncpg.Connection = None) -> list[tuple[int, int, str, str, int, int, int]]:
        """
        Return a list of tuples containing the Scheduled_Tours's data with the following order:
        - `id`
        - `guild_id`
        - `description`
        - `host`
        - `timestamp`
        - `created_at`
        - `updated_at`

        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        get_all_scheduled_tours_query = 'SELECT id, guild_id, description, host, timestamp, created_at, updated_at FROM scheduled_tours'
        records = await conn.fetch(get_all_scheduled_tours_query)
        return [tuple(record) for record in records]

    
    @staticmethod
    @connection_manager
    async def delete_scheduled_tour(id: int, conn: asyncpg.Connection = None) -> None:
        """
        Remove a Scheduled_Tour from the Scheduled_Tours Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        remove_scheduled_tour_query = 'DELETE FROM scheduled_tours WHERE id = $1'
        await conn.execute(remove_scheduled_tour_query, id)


    @staticmethod
    @connection_manager
    async def edit_scheduled_tour(
        id: int, 
        description: str, 
        host: str, 
        timestamp: int, 
        updated_at: int, 
        conn: asyncpg.Connection = None
    ) -> None:
        """
        Edit a Scheduled_Tour from the Scheduled_Tours Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        edit_scheduled_tour_query = '''
            UPDATE scheduled_tours
            SET description = $1, host = $2, timestamp = $3, updated_at = $4
            WHERE id = $5
        '''
        await conn.execute(edit_scheduled_tour_query, description, host, timestamp, updated_at, id)