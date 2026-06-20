import discord
from discord import app_commands

from Commands.base import Commands
from Code.Others import interactions
from Code.Others.Emojis import interactions as interactions_emojis
from Code.Gamemodes.enums import InfoType

class Others_Commands(Commands):
    """Class that contains the "Others" related commands's headers to load into the Discord Client."""

    def __init__(self) -> None:
        """Initialize the Others_Commands class."""
        super().__init__()


    def load_commands(self, client: discord.Client) -> None:
        """
        Method that loads the "others" commands into the client's tree.
        - `/info`
        - `/feedback`
        - `/report`
        - `/pick`
        - `/poll`
        - `/emoji_add`
        - `/emoji_delete`
        - `/emoji_check`
        """
        @client.tree.command(name='info', description='Check stored information (gamemodes, artists, metronomes, etc.)')
        @app_commands.describe(type='The type of list you want to retrieve')
        @app_commands.choices(type=[app_commands.Choice(name=option.name.replace('_', ' ').capitalize(), value=option.value) for option in InfoType])
        async def info(interaction: discord.Interaction, type: app_commands.Choice[int]):
            await interactions.info(interaction, type)


        @client.tree.command(name='feedback', description='Send a feedback message to admins and tour helpers')
        @app_commands.guild_only
        @app_commands.describe(image="Optional image to attach with your feedback")
        async def feedback(interaction: discord.Interaction, image: discord.Attachment = None):
            await interactions.feedback(interaction, image)

        @client.tree.command(name='report', description='Report some toxic behavior that only a few specific hosts would be able to see')
        @app_commands.guild_only
        @app_commands.describe(image="Optional image to attach with your feedback")
        async def report(interaction: discord.Interaction, image: discord.Attachment = None):
            await interactions.report(interaction, image)
        
        @client.tree.command(name='pick', description='Send a tour decision message to a channel that can only be seen by admins and tour helpers')
        @app_commands.describe(decision='The decision you want to send')
        @app_commands.guild_only
        async def pick(interaction: discord.Interaction, decision: str):
            await interactions.pick(interaction, decision)


        @client.tree.command(name='poll', description='Make a poll')
        @app_commands.describe(
            poll_name='The name of the poll',
            option1='1st poll option',
            option2='2nd poll option',
            option3='3rd poll option',
            option4='4th poll option',
            option5='5th poll option',
            option6='6th poll option',
            option7='7th poll option',
            option8='8th poll option',
            option9='9th poll option'
        )
        @app_commands.guild_only
        async def poll(
            interaction: discord.Interaction,
            poll_name: str,
            option1: str,
            option2: str,
            option3: str = '',
            option4: str = '',
            option5: str = '',
            option6: str = '',
            option7: str = '',
            option8: str = '',
            option9: str = ''
        ):
            all_options = [option1, option2, option3, option4, option5, option6, option7, option8, option9]
            poll_options = [option for option in all_options if option]
            await interactions.poll(interaction, poll_name, poll_options)


        @client.tree.command(name='emoji_add', description='Add your custom emoji (join/leave)')
        @app_commands.describe(emoji = 'The emoji you want to upload as a file', is_join = 'Whether the emoji being uploaded is for the "Join" one ("Leave" otherwise)')
        @app_commands.choices(is_join=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def emoji_add(interaction: discord.Interaction, emoji: discord.Attachment, is_join: app_commands.Choice[int]):
            is_join = bool(is_join.value)
            await interactions_emojis.emoji_add(interaction, emoji, is_join)


        @client.tree.command(name='emoji_delete', description='Delete one of your custom emoji (join/leave)')
        @app_commands.describe(is_join = 'Whether you want to delete your "Join" emoji (or "Leave" otherwise)')
        @app_commands.choices(is_join=[app_commands.Choice(name=str(i), value=int(i)) for i in [True, False]])
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def emoji_delete(interaction: discord.Interaction, is_join: app_commands.Choice[int]):
            is_join = bool(is_join.value)
            await interactions_emojis.emoji_delete(interaction, is_join)


        @client.tree.command(name='emoji_check', description='Show how your "Join" and "Leave" buttons look currently when hosting a tour')
        @app_commands.guild_only
        @app_commands.check(self.is_user_tour_helper)
        async def emoji_check(interaction: discord.Interaction):
            await interactions_emojis.emoji_check(interaction)