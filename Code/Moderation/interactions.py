import discord

from Commands.utilities import Tour_Helpers
from Code.Utilities.error_handler import error_handler_decorator
from Code.Utilities.to_chunks import to_chunks
from Code.Utilities.to_file import send_message_as_file
from Code.Gamemodes.controller import Main_Controller as Gamemodes_Controller
from Code.Players.controller import Players_Controller
from Code.Others.channels import Channels
from Code.Others.emojis import Emojis
from Code.Others.roles import Roles

@error_handler_decorator()
async def reset_data(interaction: discord.Interaction):
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


@error_handler_decorator()
async def ban_player(interaction: discord.Interaction, amq_name: str, is_banned: bool):
    """Interaction to handle the `/ban_player` command. It bans/unbans the `is_banned` field of the player with `name` == `amq_name`."""
    await interaction.response.defer(ephemeral=True)

    player_found, change_applied, player = Players_Controller().change_player_ban(amq_name, is_banned)
    if not player_found:
        content = f'A player with name "{amq_name}" couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    if not change_applied:
        content = f'The change wasn\'t applied since the {player.amq_name}\'s ban value is already {is_banned}'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    log_thread = await Channels().get_player_change_ban_thread(interaction.client)
    banned_value = 'banned' if player.is_banned else 'unbanned'
    content = f'{interaction.user.mention} has {banned_value} {player.discord_ping} ({player.amq_name})'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content=f'{player.discord_ping} ({player.amq_name}) has been {banned_value} successfully!', ephemeral=True)


async def ban_player_list(interaction: discord.Interaction, amq_name: str, is_list_banned: bool):
    """Interaction to handle the `/ban_player_list` command. It bans/unbans the `is_list_banned` field of the player with `name` == `amq_name`."""
    await interaction.response.defer(ephemeral=True)

    player_found, change_applied, player = Players_Controller().change_player_list_ban(amq_name, is_list_banned)
    if not player_found:
        content = f'A player with name "{amq_name}" couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    if not change_applied:
        content = f'The change wasn\'t applied since the {player.amq_name}\'s list ban value is already {is_list_banned}'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    log_thread = await Channels().get_player_change_list_ban_thread(interaction.client)
    banned_value = 'list banned' if player.is_list_banned else 'list unbanned'
    content = f'{interaction.user.mention} has {banned_value}{player.discord_ping} ({player.amq_name}) from watched tours'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content=f'{player.discord_ping} ({player.amq_name})\'s list has been {banned_value} successfully!', ephemeral=True)


@error_handler_decorator()
async def list_banned_players(interaction: discord.Interaction):
    """Interaction to handle the `/list_banned_players` command. It sends the user an embed to dm with the names of all the banned players."""
    await interaction.response.defer(ephemeral=True)

    banned_players = Players_Controller().get_all_banned_players()
    # Make sure there is at least one player banned to continue
    if not banned_players:
        content = 'Banned players list is empty!'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    banned_players_info = [f'{player.discord_ping} ({player.amq_name})' for player in banned_players]
    answer = to_chunks(banned_players_info)
    
    try:
        dmchannel = await interaction.user.create_dm()
        for message in answer:
            embed = discord.Embed(title='Banned players', description=message, color=discord.Color.green())
            await dmchannel.send(embed=embed)
        
        content = 'Banned list sent correctly!' if interaction.guild else 'I have sent you the response to DM'
        await interaction.followup.send(content=content, ephemeral=True)

    except discord.errors.Forbidden:
        await send_message_as_file(interaction, answer)


@error_handler_decorator()
async def list_watched_banned_players(interaction: discord.Interaction):
    """Interaction to handle the `/list_watched_banned_players` command. It sends the user an embed to dm with the names of all the watched banned players."""
    await interaction.response.defer(ephemeral=True)

    banned_players = Players_Controller().get_all_list_banned_players()
    # Make sure there is at least one player banned to continue
    if not banned_players:
        content = 'Banned players list is empty!'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    banned_players_info = [f'{player.discord_ping} ({player.amq_name})' for player in banned_players]
    answer = to_chunks(banned_players_info)
    
    try:
        dmchannel = await interaction.user.create_dm()
        for message in answer:
            embed = discord.Embed(title='Banned players from watched tours', description=message, color=discord.Color.green())
            await dmchannel.send(embed=embed)
        
        content = 'Banned list sent correctly!' if interaction.guild else 'I have sent you the response to DM'
        await interaction.followup.send(content=content, ephemeral=True)

    except discord.errors.Forbidden:
        await send_message_as_file(interaction, answer)