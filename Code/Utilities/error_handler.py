import traceback
import socket

import discord
import aiohttp
import asyncpg

def print_exception(error: Exception) -> None:
    """
    Analyzes the exception deeply and prints it with the appropriate level of detail:
    - Network/Infrastructure errors (External): A clean, single-line log.
    - Code bugs (Internal): The full, detailed traceback to help debug.
    """
    NETWORK_EXCEPTIONS = (
        discord.errors.HTTPException,       # General Discord API connection failures
        discord.errors.NotFound,            # Expired interactions or webhooks
        discord.errors.DiscordServerError,  # Discord infrastructure outages
        asyncpg.exceptions.PostgresError,   # Internal PostgreSQL errors (Neon.tech)
        asyncpg.exceptions.InterfaceError,  # Connection pool drops or timeouts
        aiohttp.ClientError,                # Internet drops or DNS resolution failures
        socket.error,                       # OS-level network socket failures
        TimeoutError                        # Network request timeout expirations
    )

    # NOTE Inspect error.__cause__ in case aiohttp wrapped a socket error (e.g., gaierror)
    is_network_issue = isinstance(error, NETWORK_EXCEPTIONS) or (error.__cause__ and isinstance(error.__cause__, NETWORK_EXCEPTIONS))
    if is_network_issue:
        print(f'[🌐 NETWORK/HOSTING ERROR] {type(error).__name__}: {error}')
        if error.__cause__:
            print(f'   └── Caused by -> {type(error.__cause__).__name__}: {error.__cause__}')
    else:
        print('\n' + '='*20 + " 🛑 REAL BUG DETECTED " + '='*20)
        traceback.print_exception(type(error), error, error.__traceback__)
        print('='*62 + '\n')


async def _interaction_error_handler(interaction: discord.Interaction, error: Exception):
    """
    Base error handler for interactions. Supports:    
    - `discord.errors.HTTPException` and `discord.errors.NotFound`: When a HTTP errors occures when sending the response or when discord losses the interaction,
    it tells the user to try again as the error should not be repeated again.
    
    - Default case: In case the error wasn't handled before, it tells the user that an unknown error occured and ask o tries again or inform Jabro.
    """
    print_exception(error)

    if isinstance(error, (discord.errors.HTTPException, discord.errors.NotFound)):
        msg = 'There was an error when sending you the answer. Please, try using the command again'
    else:
        msg = 'An unknown error occured... Please try again and if the issue persists tell it to Jabro (<@427868172666929160>)'

    try:
        await interaction.followup.send(content=msg, ephemeral=True)
    except Exception:
        pass

def error_handler_decorator():
    """Decorator in charge of handling the most common exceptions that can occur during a `discord.Interaction`."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                # Search for discord.Interaction in both args and kwargs
                interaction = next((arg for arg in list(args) + list(kwargs.values()) if isinstance(arg, discord.Interaction)), None)
                if interaction is None:
                    raise ValueError('No discord.Interaction instance found in arguments.')
                
                await func(*args, **kwargs)
            except Exception as error:
                await _interaction_error_handler(interaction, error)

        return wrapper
    return decorator