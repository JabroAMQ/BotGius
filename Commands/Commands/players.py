import discord
from discord import app_commands

from Commands.base import Commands
from Code.Players import interactions
from Code.Players.main_ranking import Ranking

class Players_Commands(Commands):
    """Class that contains the Players related commands's headers to load into the Discord Client."""
    def __init__(self) -> None:
        """Initialize the Players_Commands class."""
        super().__init__()


    def load_commands(self, client: discord.Client) -> None:
        """
        Method that loads the "players" commands into the client's tree.
        - `/player_register`
        - `/player_change_amq`
        - `/player_change_other_amq`
        - `/player_get_profile`
        - `/player_change_list`
        - `/player_change_mode`
        - `/player_change_rank`
        - `/player_show_ranking`
        """
        @client.tree.command(name='player_register', description='Register yourself in the player\'s database')
        @app_commands.describe(amq_name='Your AMQ name')
        @app_commands.guild_only
        async def player_register(interaction: discord.Interaction, amq_name: str):
            await interactions.player_register(interaction, amq_name)


        @client.tree.command(name='player_change_amq', description='Update your AMQ name')
        @app_commands.describe(new_amq_name='Your new AMQ name')
        @app_commands.guild_only
        async def player_change_amq(interaction: discord.Interaction, new_amq_name: str):
            await interactions.player_change_amq(interaction, new_amq_name)

        @client.tree.command(name='player_change_other_amq', description='Change the AMQ name of another player')
        @app_commands.describe(player_old_amq='The player\'s old AMQ name', player_new_amq='The player\'s new AMQ name')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def player_change_old_amq(interaction: discord.Interaction, player_old_amq: str, player_new_amq: str):
            await interactions.player_change_other_amq(interaction, player_old_amq, player_new_amq)


        @client.tree.command(name='player_get_profile', description='Get the profile of a given user')
        @app_commands.describe(amq_name='The amq name of the user', discord_name='The discord name of the user')
        @app_commands.guild_only
        async def player_get_profile(interaction: discord.Interaction, amq_name: str = '', discord_name: str = ''):
            await interactions.player_get_profile(interaction, amq_name, discord_name)


        @client.tree.command(name='player_change_rank', description='Change the rank of a player')
        @app_commands.describe(
            amq_name='The AMQ name of the player',
            new_rank = 'The new rank of the player'
        )
        @app_commands.choices(new_rank = [app_commands.Choice(name=rank_name, value=rank_name) for rank_name in Ranking().rank_names])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def player_change_rank(interaction: discord.Interaction, amq_name: str, new_rank: app_commands.Choice[str]):
            await interactions.player_change_rank(interaction, amq_name, new_rank.name)

        
        @client.tree.command(name='player_show_ranking', description='Display the ranking of all the players')
        @app_commands.describe(rank_page='Initial page of the ranking to display')
        @app_commands.choices(rank_page = [app_commands.Choice(name=rank_name, value=rank_name) for rank_name in Ranking().rank_names])
        @app_commands.guild_only
        async def player_show_ranking(interaction: discord.Interaction, rank_page: app_commands.Choice[str]):
            await interactions.player_show_ranking(interaction, rank_page.name)