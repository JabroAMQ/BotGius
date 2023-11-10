import os

import dotenv
import discord

from Commands.utilities import load_app_commands, load_controllers

class BotGius(discord.Client):
    """A custom Discord client class for hosting AMQ tours."""

    def __init__(self, intents: discord.Intents, sync_commands : bool):
        """
        Initialize the BotGius client.

        Parameters:
        -----------
        - `intents` : `discord.Intents`
            Permissions that the client has.
        - `sync_commands` : `bool`
            Whether to synchronize client commands with Discord.
        """
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.sync_commands = sync_commands
        load_app_commands(self)
        load_controllers()
    
    async def setup_hook(self):
        """Hook to set up bot commands, used for syncing with Discord."""
        if self.sync_commands:
            commands = await self.tree.sync()
            print(f'Synced {len(commands)} commands.')

    async def on_ready(self):
        """Event handler for when the bot is ready."""
        print(f'Logged in as {self.user} (ID: {self.user.id})')


dotenv.load_dotenv('.env')          # Private, it isn't added to the GitHub repository
TOKEN = os.getenv('DISCORD_TOKEN')

sync_commands = False               # Set to True to sync new commands
client = BotGius(intents=discord.Intents.all(), sync_commands=sync_commands)

client.run(TOKEN)