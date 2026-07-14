import asyncpg
from Code.Utilities.database_connection_postgreql import connection_manager


class Players_Database:
    """Static class to handle connections with the Players Database."""
    
    @staticmethod
    @connection_manager
    async def get_all_players(conn: asyncpg.Connection = None) -> list[tuple[int, str, str, bool, bool]]:
        """
        Return a list of tuples containing the Players's data with the following order:
        - `discord_id`
        - `amq_name`
        - `rank`
        - `is_banned`
        - `is_list_banned`
        
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        get_all_players_query = 'SELECT id, amq, rank, is_banned, is_list_banned FROM players'
        result = await conn.fetch(get_all_players_query)
        return [tuple(record) for record in result]

    @staticmethod
    @connection_manager
    async def add_player(discord_id: int, amq_name: str, conn: asyncpg.Connection = None) -> None:
        """
        Add a new Player to the Players Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        add_player_query = 'INSERT INTO players (id, amq) VALUES ($1, $2)'
        await conn.execute(add_player_query, discord_id, amq_name)

    @staticmethod
    @connection_manager
    async def change_player_amq(discord_id: int, new_amq_name: str, conn: asyncpg.Connection = None) -> None:
        """
        Change the Player's amq name to `new_amq_name` from the `discord_id` player in the Players Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        change_player_amq_query = 'UPDATE players SET amq = $1 WHERE id = $2'
        await conn.execute(change_player_amq_query, new_amq_name, discord_id)

    @staticmethod
    @connection_manager
    async def change_player_rank(discord_id: int, new_rank: str, conn: asyncpg.Connection = None) -> None:
        """
        Change the Player's rank to `new_rank` from the `discord_id` player in the Players Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        change_player_rank_query = 'UPDATE players SET rank = $1 WHERE id = $2'
        await conn.execute(change_player_rank_query, new_rank, discord_id)

    @staticmethod
    @connection_manager
    async def change_is_banned(discord_id: int, is_banned: bool, conn: asyncpg.Connection = None) -> None:
        """
        Change the Player's "is_banned" attribute to `is_banned` from the `discord_id` player in the Players Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        change_player_is_banned_query = 'UPDATE players SET is_banned = $1 WHERE id = $2'
        await conn.execute(change_player_is_banned_query, is_banned, discord_id)

    @staticmethod
    @connection_manager
    async def change_is_list_banned(discord_id: int, is_list_banned: bool, conn: asyncpg.Connection = None) -> None:
        """
        Change the Player's "is_list_banned" attribute to `is_list_banned` from the `discord_id` player in the Players Database.
        Do NOT add a `conn` value, its a placeholder whose value will be replaced.
        """
        change_player_is_list_banned_query = 'UPDATE players SET is_list_banned = $1 WHERE id = $2'
        await conn.execute(change_player_is_list_banned_query, is_list_banned, discord_id)