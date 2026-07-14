import os
from typing import Callable, Any, Optional

import asyncpg
from dotenv import load_dotenv

load_dotenv()
_database_url = os.getenv('DATABASE_URL')
_pool: Optional[asyncpg.Pool] = None

async def _initialize_db_pool() -> None:
    """Initialize the connection pool for PostgreSQL using asyncpg."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            _database_url,
            min_size=1,
            max_size=5,
            command_timeout=15.0
        )

async def close_db_pool() -> None:
    """Close the connection pool for PostgreSQL if it has been initialized."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

def connection_manager(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for managing database connections with a connection pool."""
    async def wrapper(*args, **kwargs):
        global _pool
        if _pool is None:
            await _initialize_db_pool()
        
        async with _pool.acquire() as conn:
            async with conn.transaction():
                try:
                    kwargs['conn'] = conn
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    raise e
            
    return wrapper