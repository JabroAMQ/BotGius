import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Utilities.to_chunks import to_chunks
from Code.Utilities.to_file import send_message_as_file
from Code.Utilities.to_webhook import to_webhook
from Code.Gamemodes.controller import Main_Controller as Gamemodes_Controller
from Code.Players.controller import Players_Controller
from Code.Others.emojis import Emojis
from Code.Others.channels import Channels

async def _validate_image(interaction: discord.Interaction, image: discord.Attachment) -> bool:
    """Ensure that the `image` attachment is a valid image and not too large."""
    # Ensure the attachment is an image
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp') # Check extension to guard against spoofed non-image files
    if not image.content_type or not image.content_type.startswith('image/') or not image.filename.lower().endswith(allowed_extensions):
        content = f'The only allowed image formats are PNG, JPG, JPEG, GIF, and WEBP. Please upload a valid image.'
        await interaction.response.send_message(content, ephemeral=True)
        return False
    
    # Check if the image is too large
    # NOTE not tested (nitro needed)
    if image.size > 8 * 1024 * 1024:  # 8 MB limit
        size_mb = image.size / (1024 * 1024)
        content = f'The image you uploaded is too large ({size_mb:.2f} MB). Please upload an image smaller than 8 MB.'
        await interaction.response.send_message(content, ephemeral=True)
        return False
    
    return True


@error_handler_decorator()
async def info(interaction: discord.Interaction, type: discord.app_commands.Choice[int]):
    """Interaction to handle the `/info` command. It sends embeds to dm with the information asked for in the `type` command parameter."""
    await interaction.response.defer(ephemeral=True)
    raw_answer = Gamemodes_Controller().info(type.value)
    answer = to_chunks(raw_answer)

    try:
        dmchannel = await interaction.user.create_dm()
        for message in answer:
            embed = discord.Embed(title=type.name, description=message, color=discord.Color.green())
            await dmchannel.send(embed=embed)
        
        content = 'Info sent correctly!' if interaction.guild else 'I have sent you the response to DM'
        await interaction.followup.send(content=content, ephemeral=True)

    except discord.errors.Forbidden:
        await send_message_as_file(interaction, answer)
        

async def feedback(interaction: discord.Interaction, image: discord.Attachment = None):
    """Interaction to handle the `/feedback` command. It sends the `feedback` to the feedback channel."""

    class Feedback_Modal(discord.ui.Modal, title='Feedback'):
        def __init__(self, image: discord.Attachment = None):
            super().__init__()
            self.image = image
        
        name = discord.ui.TextInput(
            label='Name',
            style=discord.TextStyle.short,
            placeholder='Your amq name would be used if left empty',
            default='',
            required=False,
            max_length=50
        )

        feedback = discord.ui.TextInput(
            label='Feedback',
            style=discord.TextStyle.long,
            placeholder='Feedback is not something like "vortex tour when"',
            required=True,
            max_length=1000
        )

        @error_handler_decorator()
        async def on_submit(self, new_interaction: discord.Interaction):
            await new_interaction.response.defer(ephemeral=True)

            if self.name.value:
                player_name = self.name
            else:
                player = Players_Controller().get_player(new_interaction.user.id)
                player_name = player.amq_name if player is not None else 'Not Registered'

            embed = discord.Embed(title='Feedback', color=discord.Colour.green())
            embed.add_field(name='From', value=player_name, inline=False)
            embed.add_field(name='Content', value=self.feedback, inline=False)
            if self.image:
                embed.set_image(url=self.image.url)
            
            feedback_channel = Channels().get_feedback_channel(new_interaction.client)
            host_channel = Channels().get_host_channel(new_interaction.client)
            await to_webhook(interaction=new_interaction, webhook_name='Feedback', channel=feedback_channel, embed=embed, inform=False)
            await to_webhook(interaction=new_interaction, webhook_name='Feedback', channel=host_channel, embed=embed)

    if image:
        image_ok = await _validate_image(interaction, image)
        if not image_ok:
            return

    await interaction.response.send_modal(Feedback_Modal(image))


async def report(interaction: discord.Interaction, image: discord.Attachment = None):
    """Interaction to handle the `/report` command. It sends the report about toxic behavior to a channel only visible to a few specific hosts."""

    class Report_Modal(discord.ui.Modal, title='Report'):
        def __init__(self, image: discord.Attachment = None):
            super().__init__()
            self.image = image

        name = discord.ui.TextInput(
            label='Name',
            style=discord.TextStyle.short,
            placeholder='Your amq name would be used if left empty',
            default='',
            required=False,
            max_length=50
        )

        feedback = discord.ui.TextInput(
            label='Report',
            style=discord.TextStyle.long,
            placeholder='Report the toxic behavior here (who and why)',
            required=True,
            max_length=1000
        )

        @error_handler_decorator()
        async def on_submit(self, new_interaction: discord.Interaction):
            await new_interaction.response.defer(ephemeral=True)

            if self.name.value:
                player_name = self.name
            else:
                player = Players_Controller().get_player(new_interaction.user.id)
                player_name = player.amq_name if player is not None else 'Not Registered'

            embed = discord.Embed(title='Report', color=discord.Colour.red())
            embed.add_field(name='From', value=player_name, inline=False)
            embed.add_field(name='Content', value=self.feedback, inline=False)
            if self.image:
                embed.set_image(url=self.image.url)
            
            report_channel = Channels().get_report_channel(new_interaction.client)
            await to_webhook(interaction=new_interaction, webhook_name='Report', channel=report_channel, embed=embed)

    if image:
        image_ok = await _validate_image(interaction, image)
        if not image_ok:
            return

    await interaction.response.send_modal(Report_Modal(image))


@error_handler_decorator()
async def pick(interaction: discord.Interaction, decision: str):
    """Interaction to handle the `/pick` command. It sends the `pick` to the pick channel."""
    await interaction.response.defer(ephemeral=True)

    picks_channel = Channels().get_picks_channel(interaction.client)
    player = Players_Controller().get_player(interaction.user.id)
    player_name = player.amq_name if player is not None else 'Not Registered'

    embed = discord.Embed(title='Pick', color=discord.Colour.green())
    embed.add_field(name='From', value=player_name, inline=False)
    embed.add_field(name='Content', value=decision, inline=False)
    
    await to_webhook(interaction=interaction, webhook_name='Pick', channel=picks_channel, embed=embed)


@error_handler_decorator()
async def poll(interaction: discord.Interaction, poll_name: str, options: list[str]):
    """Interaction to handle the `/poll` command. It sends an embed with the options provided adding one reaction per possible option."""
    await interaction.response.defer(ephemeral=False)
    reactions = Emojis().get_poll_emojis(len(options))

    poll_options = [f'{reaction} {option}' for option, reaction in zip(options, reactions)]
    poll_options = '\n'.join(poll_options)
    embed = discord.Embed(title=poll_name, description=poll_options, color=discord.Color.green())
    message = await interaction.followup.send(embed=embed, ephemeral=False, wait=True)
    
    [await message.add_reaction(reaction) for reaction in reactions]