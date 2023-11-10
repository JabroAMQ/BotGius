import discord
from discord import app_commands

from Commands.base import Commands
from Code.Moderation import interactions

class Moderation_Commands(Commands):
    """Class that contains the Moderation related commands's headers to load into the Discord Client."""

    def __init__(self) -> None:
        """Initialize the Moderation_Commands class."""
        super().__init__()

    def load_commands(self, client : discord.Client) -> None:
        """
        Method that loads the "moderation" commands into the client's tree.
        - `/reset_data`
        """
        @client.tree.command(name='reset_data', description='Retrieve again the information from the sheets to keep it updated')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def reset_data(interaction : discord.Interaction):
            await interactions.reset_data(interaction)