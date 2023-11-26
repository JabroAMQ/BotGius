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