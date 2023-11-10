import discord

from Commands.utilities import Tour_Helpers
from Code.Utilities.error_handler import error_handler_decorator
from Code.Gamemodes.controller import Main_Controller as Gamemodes_Controller
from Code.Others.channels import Channels
from Code.Others.emojis import Emojis
from Code.Others.roles import Roles

@error_handler_decorator()
async def reset_data(interaction : discord.Interaction):
    """
    Interaction to handle the `/reset_data` command.\n
    It reloads some of the bot's data so that reseting the bot when an external data change is made is not needed.\n
    Useful when:
    - Changes in the yaml files are made
    - Changes in the google spreadsheets (main one / global players one) are made
    """
    await interaction.response.defer(ephemeral=True)

    Gamemodes_Controller()._set_data()
    Channels()._set_data()
    Emojis()._set_data()
    Roles()._set_data()
    Tour_Helpers()._set_data()

    content = 'The lists were updated successfully!'
    await interaction.followup.send(content=content, ephemeral=True)