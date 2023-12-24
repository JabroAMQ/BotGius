import discord

from Code.Utilities.error_handler import error_handler_decorator

@error_handler_decorator()
async def to_webhook(
    interaction: discord.Interaction,
    webhook_name: str,
    channel: discord.TextChannel,
    message_content: str = '',
    embed: discord.Embed = None
):
    """Send a webhook to the specified `channel` with the `message_content` provided and with the name and avatar extracted from the `interaction`."""
    user_name = interaction.user.display_name
    user_avatar_url = interaction.user.display_avatar.url
    
    try:
        webhook = await channel.create_webhook(name=webhook_name)
        await webhook.send(content=message_content, embed=embed, username=user_name, avatar_url=user_avatar_url)
        await interaction.followup.send(content=f'{webhook_name} was completed successfully!', ephemeral=True)
    
    finally:
        await webhook.delete()