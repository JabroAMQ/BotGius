import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Others.Emojis.controller import Emojis_Controller

async def _show_preview(interaction: discord.Interaction) -> discord.ui.View:
    """Shows how the host's "Join" and "Leave" buttons look currently when hosting a tour"""
    emoji_join, emoji_leave = Emojis_Controller().get_tour_emojis(interaction.user.id)

    class Tour_Create_Preview(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label='Join', emoji=emoji_join, style=discord.ButtonStyle.green)
        async def join(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            await new_interaction.followup.send(content=emoji_join, ephemeral=True)

        @discord.ui.button(label='Leave', emoji=emoji_leave, style=discord.ButtonStyle.green)
        async def leave(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            await new_interaction.followup.send(content=emoji_leave, ephemeral=True)

    return Tour_Create_Preview()

@error_handler_decorator()
async def emoji_add(interaction: discord.Interaction, emoji: discord.Attachment, is_join: bool):
    """Interaction to handle the `/emoji_add` command. It uploads the `emoji` file to the bot as the custom join/leave emoji, depending of the `is_join` value."""
    await interaction.response.defer(ephemeral=True)
    
    emoji_added = await Emojis_Controller().add_emoji(interaction, emoji, is_join)
    if not emoji_added:
        content = 'There was an error while uploading the emoji. Please try again later'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    content = f'Emoji added successfully! Current `/tour_create` buttons preview:'
    view = await _show_preview(interaction)
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def emoji_delete(interaction: discord.Interaction, is_join: bool):
    """Interaction to handle the `/emoji_delete` command. It removes the host's custom join/leave emoji, depending of the `is_join` value."""
    await interaction.response.defer(ephemeral=True)

    emoji_found, emoji_deleted = await Emojis_Controller().delete_emoji(interaction, is_join)
    if not emoji_found:
        content = f'You don\'t have a custom emoji to delete for `is_join={is_join}`\nCurrent `/tour_create` buttons preview:'
        view = await _show_preview(interaction)
        await interaction.followup.send(content=content, view=view, ephemeral=True)
        return

    if not emoji_deleted:
        content = 'There was an error while deleting the emoji. Please try again later'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    content = f'Emoji deleted successfully! Current `/tour_create` buttons preview:'
    view = await _show_preview(interaction)
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def emoji_check(interaction: discord.Interaction):
    """Interaction to handle the `/emoji_check` command. It shows how the host's "Join" and "Leave" buttons look currently when hosting a tour."""
    await interaction.response.defer(ephemeral=True)

    content = f'Current `/tour_create` buttons preview:'
    view = await _show_preview(interaction)
    await interaction.followup.send(content=content, view=view, ephemeral=True)