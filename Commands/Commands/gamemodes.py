import discord
from discord import app_commands

from Commands.base import Commands
from Code.Gamemodes import interactions
from Code.Rolls.enums import Rolls_Enum, Roll_Gamemode

class Gamemodes_Commands(Commands):
    """Class that contains the Gamemodes related commands's headers to load into the Discord Client."""
    def __init__(self) -> None:
        """Initialize the Gamemodes_Commands class."""
        super().__init__()

    def load_commands(self, client: discord.Client) -> None:
        """
        Method that loads the "gamemodes" commands into the client's tree.
        - `/gamemode_add`
        - `/gamemode_delete`
        - `/gamemode_edit`
        - `/gamemode_code`
        - `/gamemode_info`
        - `/roll`
        - `/roll_gamemode`
        """
        @client.tree.command(name='gamemode_add', description='Add a new gamemode to the list of gamemodes')
        @app_commands.describe(
            name='The name of the gamemode',
            size='The number of players PER TEAM',
            code='The AMQ code of the gamemode (lobby settings)',
            is_it_watched='Whether the gamemode is watched (hybrid counts as watched)',
            is_random_dist_rollable='Whether random is a rollable watched distribution (ignore if not watched)',
            is_weighted_dist_rollable='Whether weighted is a rollable watched distribution (ignore if not watched)',
            is_equal_dist_rollable='Whether equal is a rollable watched distribution (ignore if not watched)'
        )
        @app_commands.choices(size=[app_commands.Choice(name=str(i), value=i) for i in [1, 2, 3, 4]])
        @app_commands.choices(is_it_watched=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.choices(is_random_dist_rollable=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.choices(is_weighted_dist_rollable=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.choices(is_equal_dist_rollable=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.guild_only
        @app_commands.check(self.is_user_admin)
        async def gamemode_add(
            interaction: discord.Interaction,
            name: str,
            size: app_commands.Choice[int],
            code: str,
            is_it_watched: app_commands.Choice[int],
            is_random_dist_rollable: app_commands.Choice[int],
            is_weighted_dist_rollable: app_commands.Choice[int],
            is_equal_dist_rollable: app_commands.Choice[int]
        ):
            is_it_watched = bool(is_it_watched.value)
            is_random_dist_rollable = bool(is_random_dist_rollable.value)
            is_weighted_dist_rollable = bool(is_weighted_dist_rollable.value)
            is_equal_dist_rollable = bool(is_equal_dist_rollable.value)
            await interactions.gamemode_add(interaction, name, size.value, code, is_it_watched, is_random_dist_rollable, is_weighted_dist_rollable, is_equal_dist_rollable)


        @client.tree.command(name='gamemode_delete', description='Delete a gamemode from the list of gamemodes')
        @app_commands.describe(gamemode_name='The name of the gamemode to delete')
        @app_commands.guild_only
        @app_commands.check(self.is_user_admin)
        async def gamemode_delete(interaction: discord.Interaction, gamemode_name: str):
            await interactions.gamemode_delete(interaction, gamemode_name)


        @client.tree.command(name='gamemode_edit', description='Edit property values of a gamemode')
        @app_commands.describe(
            gamemode_name='The name of the gamemode to edit',
            new_name='The new name that the gamemode will have',
            new_code='The new code that the gamemode will have',
            new_random_song_distribution='Whether random is now a rollable watched distribution',
            new_weighted_song_distribution='Whether weighted is now a rollable watched distribution',
            new_equal_song_distribution='Whether equal is now a rollable watched distribution'
        )
        @app_commands.choices(new_random_song_distribution=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.choices(new_weighted_song_distribution=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.choices(new_equal_song_distribution=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.guild_only
        @app_commands.check(self.is_user_admin)
        async def gamemode_edit(
            interaction: discord.Interaction,
            gamemode_name: str,
            new_name: str = None,
            new_code: str = None,
            new_random_song_distribution: app_commands.Choice[int] = None,
            new_weighted_song_distribution: app_commands.Choice[int] = None,
            new_equal_song_distribution: app_commands.Choice[int] = None
        ):
            new_random_song_distribution = bool(new_random_song_distribution.value) if new_random_song_distribution is not None else None
            new_weighted_song_distribution = bool(new_weighted_song_distribution.value) if new_weighted_song_distribution is not None else None
            new_equal_song_distribution = bool(new_equal_song_distribution.value) if new_equal_song_distribution is not None else None
            await interactions.gamemode_edit(
                interaction, gamemode_name, new_name, new_code, new_random_song_distribution, new_weighted_song_distribution, new_equal_song_distribution
            )


        @client.tree.command(name='gamemode_code', description='Gives you the amq code (room settings) of a gamemode')
        @app_commands.describe(gamemode_name='The name of the gamemode which code you want to get')
        async def gamemode_code(interaction: discord.Interaction, gamemode_name: str):
            await interactions.get_code(interaction, gamemode_name)


        @client.tree.command(name='gamemode_info', description='Gives you the description of a gamemode')
        @app_commands.describe(gamemode_name='The name of the gamemode which description you want to get')
        async def gamemode_code(interaction: discord.Interaction, gamemode_name: str):
            await interactions.get_info(interaction, gamemode_name)


        @client.tree.command(name='roll', description='For rolling stuff (no gamemodes)')
        @app_commands.describe(type='Type of stuff to roll')
        @app_commands.choices(type=[app_commands.Choice(name=type.name.replace('_', ' ').capitalize(), value=type.value) for type in Rolls_Enum])
        async def roll(interaction: discord.Interaction, type: app_commands.Choice[int]):
            await interactions.roll(interaction, type.value)


        @client.tree.command(name='roll_gamemode', description='For rolling gamemodes')
        @app_commands.describe(type='Type of stuff to roll')
        @app_commands.choices(type=[app_commands.Choice(name=type.name.replace('_', ' ').capitalize(), value=type.value) for type in Roll_Gamemode])
        async def roll_gamemode(interaction: discord.Interaction, type: app_commands.Choice[int]):
            await interactions.roll_gamemode(interaction, type.value)