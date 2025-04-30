import traceback

import discord

def print_exception(error: Exception) -> None:
    """Print a exception to console without raising it."""
    traceback.print_exception(type(error), error, error.__traceback__)


async def _interaction_error_handler(interaction: discord.Interaction, error: Exception):
    """
    Base error handler for interactions. Supports:    
    - `discord.errors.HTTPException` and `discord.errors.NotFound`: When a HTTP errors occures when sending the response or when discord losses the interaction,
    it tells the user to try again as the error should not be repeated again.
    
    - Default case: In case the error wasn't handled before, it tells the user that an unknown error occured and ask o tries again or inform Jabro.
    """
    if isinstance(error, (discord.errors.HTTPException, discord.errors.NotFound)):
        await interaction.followup.send(content='There was a error when sending you the answer. Please, try using the command again', ephemeral=True)

    else:
        await interaction.followup.send(content='An unknown error occured... Please try again and if the issue persists tell it to Jabro (<@427868172666929160>)', ephemeral=True)
        print_exception(error)


def error_handler_decorator():
    """Decorator in charge of handling the most common exceptions that can occure during a `discord.Interaction`."""
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