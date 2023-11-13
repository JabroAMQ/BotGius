import discord
from discord import app_commands

from Commands.base import Commands
from Code.Players import interactions
from Code.Players.enums import List_From_Options, List_Sections_Options, Prefered_Gamemode_Options
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
        - `/player_get_profile`
        - `/player_change_list`
        - `/player_change_mode`
        - `/player_change_rank`
        - `/player_show_ranking`
        """
        @client.tree.command(name='player_register', description='Register yourself in the player\'s database')
        @app_commands.describe(amq_name='Your AMQ name')
        @app_commands.guild_only
        async def player_register(interaction : discord.Interaction, amq_name : str):
            await interactions.player_register(interaction, amq_name)

        @client.tree.command(name='player_change_amq', description='Update your AMQ name')
        @app_commands.describe(new_amq_name='Your new AMQ name')
        @app_commands.guild_only
        async def player_change_amq(interaction : discord.Interaction, new_amq_name : str):
            await interactions.player_change_amq(interaction, new_amq_name)


        @client.tree.command(name='player_get_profile', description='Get the profile of a given user')
        @app_commands.describe(amq_name='The amq name of the user', discord_name='The discord name of the user')
        @app_commands.guild_only
        async def player_get_profile(interaction : discord.Interaction, amq_name : str = '', discord_name : str = ''):
            await interactions.player_get_profile(interaction, amq_name, discord_name)

        @client.tree.command(name='player_change_list', description='Update your list information')
        @app_commands.describe(
            list_name='The name of your list',
            list_from='The platform where your list is from',
            list_sections='The sections of your list to use'
        )
        @app_commands.choices(
            list_from     = [app_commands.Choice(name=f, value=f) for f in [option.name for option in List_From_Options]],
            list_sections = [app_commands.Choice(name=c, value=c) for c in [option.name.replace('_', ' / ') for option in List_Sections_Options]]
        )
        @app_commands.guild_only
        async def player_change_list(
            interaction : discord.Interaction,
            list_name : str,
            list_from : app_commands.Choice[str],
            list_sections : app_commands.Choice[str]
        ):
            await interactions.player_change_list(interaction, list_name, list_from.value, list_sections.value)
        
        @client.tree.command(name='player_change_mode', description='Update your favourite or most hated gamemodes')
        @app_commands.describe(type='Which gamemode to update')
        @app_commands.choices(type=[app_commands.Choice(name=option.name, value=option.value) for option in Prefered_Gamemode_Options])
        @app_commands.guild_only
        async def player_change_mode(interaction : discord.Interaction, type : app_commands.Choice[int]):
            await interactions.player_change_mode(interaction, type)

        
        @client.tree.command(name='player_change_rank', description='Change the rank of a player')
        @app_commands.describe(
            amq_name='Your AMQ name of the player',
            new_rank = 'The new rank of the player'
        )
        @app_commands.choices(new_rank = [app_commands.Choice(name=rank_name, value=rank_name) for rank_name in Ranking().rank_names])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def player_change_rank(interaction : discord.Interaction, amq_name : str, new_rank : app_commands.Choice[str]):
            await interactions.player_change_rank(interaction, amq_name, new_rank.name)

        
        @client.tree.command(name='player_show_ranking', description='Display the ranking of all the players')
        @app_commands.describe(rank_page='Initial page of the ranking to display')
        @app_commands.choices(rank_page = [app_commands.Choice(name=rank_name, value=rank_name) for rank_name in Ranking().rank_names])
        @app_commands.guild_only
        async def player_show_ranking(interaction : discord.Interaction, rank_page : app_commands.Choice[str]):
            await interactions.player_show_ranking(interaction, rank_page.name)