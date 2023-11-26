import os

import dotenv
import discord

from Commands.utilities import load_app_commands, load_controllers

class BotGius(discord.Client):
    """A custom Discord client class for hosting AMQ tours."""

    def __init__(self):
        """Initialize the BotGius client."""
        super().__init__(intents=discord.Intents.all())
        self.sync_commands = False
        self.tree = discord.app_commands.CommandTree(self)
        load_app_commands(self)
        load_controllers()

        @self.tree.error
        async def on_app_command_error(interaction : discord.Interaction, error : discord.app_commands.AppCommandError):
            """
            Handler for app commands's highest level errors.\n
            This is, errors that may occure due to checks done before the command's code itself is executed (e.g. syntax errors in the command's header).\n
            For generic error handling that may occure during the command's execution check `Code/Utilities/error_handler/`, which contain a decorator that
            all commands should call.
            """
            if isinstance(error, discord.app_commands.errors.CheckFailure):
                await interaction.response.send_message(content='You don\'t have permissions to use this command', ephemeral=True)
            else:
                # NOTE this should never be reached
                print('Unhandled app_commands top level error!')
                raise error
    

    async def setup_hook(self):
        """Hook to set up bot commands, used for syncing with Discord."""
        if self.sync_commands:
            commands = await self.tree.sync()
            print(f'Synced {len(commands)} commands.')


    async def on_ready(self):
        """Event handler for when the bot is ready."""
        print(f'Logged in as {self.user} (ID: {self.user.id})')


dotenv.load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
client = BotGius()
client.run(TOKEN)