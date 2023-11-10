import discord
from discord import app_commands

from Commands.base import Commands
from Code.Tours import interactions
from Code.Tours.enums import Teams
from Code.Rolls.enums import Roll_Teams, Roll_Gamemode

class Tours_Commands(Commands):
    """Class that contains the Tours related commands's headers to load into the Discord Client."""
    def __init__(self) -> None:
        """Initialize the Tours_Commands class."""
        super().__init__()


    def load_commands(self, client: discord.Client) -> None:
        """
        Method that loads the "tours" commands into the client's tree.
        - `/tour_create`
        - `/tour_edit`
        - `/tour_quit`
        - `/tour_players_add`
        - `/tour_players_remove`
        - `/tour_players_list`
        - `/tour_players_ping`
        - `/tour_end`
        - `/team_players_add`
        - `/team_players_remove`
        - `/team_randomize`
        - `/team_get_all_roles`
        - `/roll_groups`
        - `/roll_blind_crews`
        """
        @client.tree.command(name='tour_create', description='Creates a new tour')
        @app_commands.describe(
            timer='Number of minutes before sign ups get closed',
            size='Maximum number of tour players',
            info='Tour\'s description'
        )
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def tour_create(
            interaction : discord.Interaction,
            timer : app_commands.Range[int, 1, 180] = None,
            size : app_commands.Range[int, 8, 128] = None,
            info : str = ''
        ):
            await interactions.tour_create(interaction, timer, size, info)


        @client.tree.command(name='tour_edit', description='Edit some parameters from the active tour')
        @app_commands.describe(
            timer='Number of minutes before sign ups get closed',
            size='Maximum number of tour players',
            looking_for_players = 'Whether player can still join at least to the queue',
            info='Tour\'s description'
        )
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def tour_edit(
            interaction : discord.Interaction,
            timer : app_commands.Range[int, 1, 180] = None,
            size : app_commands.Range[int, 8, 128] = None,
            looking_for_players : bool = None,
            info : str = None
        ):
            await interactions.tour_edit(interaction, timer, size, looking_for_players, info)


        
        @client.tree.command(name='tour_quit', description='Allows you to leave the current tour')
        @app_commands.guild_only
        async def tour_quit(interaction : discord.Interaction):
            await interactions.tour_quit(interaction)
        

        @client.tree.command(name='tour_players_add', description='Manually add players to the tour')
        @app_commands.describe(players='AMQ name of the player(s) to add')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def tour_players_add(interaction : discord.Interaction, players : str):
            await interactions.tour_players_add(interaction, players)

        
        @client.tree.command(name='tour_players_remove', description='Manually remove players to the tour')
        @app_commands.describe(players='AMQ name of the player(s) to remove')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def tour_players_remove(interaction : discord.Interaction, players : str):
            await interactions.tour_players_remove(interaction, players)


        @client.tree.command(name='tour_players_list', description='Return the list of players that joined the tour')
        @app_commands.guild_only
        async def tour_players_list(interaction : discord.Interaction):
            await interactions.tour_players_list(interaction)


        @client.tree.command(name='tour_players_ping', description='Ping the players (not queue) that joined the tour')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def tour_players_ping(interaction : discord.Interaction):
            await interactions.tour_players_ping(interaction)


        @client.tree.command(name='tour_end', description='End the tour that is currently active')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def tour_end(interaction : discord.Interaction):
            await interactions.tour_end(interaction)


        @client.tree.command(name='team_players_list', description='Return the list of players from each team')
        @app_commands.guild_only
        async def team_players_list(interaction : discord.Interaction):
            await interactions.team_players_list(interaction)


        @client.tree.command(name='team_players_add', description='Add players to a team')
        @app_commands.describe(
            team='The team to add the players to',
            players='AMQ name of the player(s) to add'
        )
        @app_commands.choices(team=[app_commands.Choice(name=team.name.replace('_', ' '), value=team.value) for team in Teams])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def team_players_add(interaction : discord.Interaction, team : app_commands.Choice[int], players : str):
            await interactions.team_players_add(interaction, team.value, players)


        @client.tree.command(name='team_players_remove', description='Remove players from a team')
        @app_commands.describe(
            team='The team to remove the players from',
            players='AMQ name of the player(s) to remove'
        )
        @app_commands.choices(team=[app_commands.Choice(name=team.name.replace('_', ' '), value=team.value) for team in Teams])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def team_players_remove(interaction : discord.Interaction, team : app_commands.Choice[int], players : str):
            await interactions.team_players_remove(interaction, team.value, players)


        @client.tree.command(name='team_randomize', description='Split the players into teams based on the selected criteria')
        @app_commands.describe(number_of_teams='Number of teams to split the players into', criteria='Type of randomization to apply')
        @app_commands.choices(number_of_teams=[app_commands.Choice(name=i, value=i) for i in [2, 3, 4, 5, 6, 7, 8]])
        @app_commands.choices(criteria=[app_commands.Choice(name=type.name.replace('_', ' ').capitalize(), value=type.value) for type in Roll_Teams])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def team_randomize(interaction : discord.Interaction, number_of_teams : app_commands.Choice[int], criteria : app_commands.Choice[int]):
            await interactions.team_randomize(interaction, number_of_teams.value, criteria.value)


        @client.tree.command(name='team_get_all_roles', description='Add all team roles to the user')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def team_get_all_roles(interaction : discord.Interaction):
            await interactions.team_get_all_roles(interaction)


        @client.tree.command(name='roll_groups', description='Split the players into groups based on the selected criteria')
        @app_commands.describe(number_of_groups='Number of groups to split the players into', criteria='Type of randomization to apply')
        @app_commands.choices(criteria=[app_commands.Choice(name=type.name.replace('_', ' ').capitalize(), value=type.value) for type in Roll_Teams])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def roll_groups(interaction : discord.Interaction, number_of_groups : int, criteria : app_commands.Choice[int]):
            await interactions.roll_groups(interaction, number_of_groups, criteria.value)


        @client.tree.command(name='roll_blind_crews', description='Roll a blind crews round')
        @app_commands.describe(gamemodes='Which gamemodes to roll')
        @app_commands.choices(gamemodes=[app_commands.Choice(name=type.name.replace('_', ' ').capitalize(), value=type.value) for type in Roll_Gamemode])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def roll_blind_crews(interaction : discord.Interaction, gamemodes : app_commands.Choice[int]):
            await interactions.roll_blind_crews(interaction, gamemodes.value)