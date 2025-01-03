import discord
from discord import app_commands

from Commands.base import Commands
from Code.Moderation import interactions

class Moderation_Commands(Commands):
    """Class that contains the Moderation related commands's headers to load into the Discord Client."""

    def __init__(self) -> None:
        """Initialize the Moderation_Commands class."""
        super().__init__()

    def load_commands(self, client: discord.Client) -> None:
        """
        Method that loads the "moderation" commands into the client's tree.
        - `/reset_data`
        - `/ban_player`
        - `/list_banned_players`
        """
        @client.tree.command(name='reset_data', description='Retrieve again the information from the sheets to keep it updated')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def reset_data(interaction: discord.Interaction):
            await interactions.reset_data(interaction)

        
        @client.tree.command(name='ban_player', description='Ban/Unban a player')
        @app_commands.describe(
            amq_name='The AMQ name of the player',
            is_now_banned='Whether you want to ban (True) or unban (False) the user'    
        )
        @app_commands.choices(is_now_banned=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def ban_player(interaction: discord.Interaction, amq_name: str, is_now_banned: app_commands.Choice[int]):
            is_now_banned = bool(is_now_banned.value)
            await interactions.ban_player(interaction, amq_name, is_now_banned)


        @client.tree.command(name='list_banned_players', description='List all banned players')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def list_banned_players(interaction: discord.Interaction):
            await interactions.list_banned_players(interaction)