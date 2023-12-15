import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Players.controller import Players_Controller
from Code.Players.player import Player
from Code.Players.main_ranking import Ranking
from Code.Players.enums import Prefered_Gamemode_Options
from Code.Gamemodes.controller import Main_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode
from Code.Others.channels import Channels

@error_handler_decorator()
async def player_register(interaction : discord.Interaction, amq_name : str):
    """Interaction to handle the `/player_register` command. It stores in the player's Database and Catalog the new player created with the provided information."""
    await interaction.response.defer(ephemeral=True)
    register_ok, other_player_ping = Players_Controller().register_player(discord_id=interaction.user.id, amq_name=amq_name)
    amq_name = discord.utils.escape_markdown(amq_name)

    if not register_ok:
        if other_player_ping is None:
            content = 'You are already registered!\nIf you want to change your amq name use `/player_change_amq` instead'
        else:
            content = f'`{amq_name}` is already used as the `amq_name` of {other_player_ping}.'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    log_thread = await Channels().get_player_register_thread(interaction.client)
    content = f'{interaction.user.mention} registered as **{amq_name}**'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content='Registration complete successfully!', ephemeral=True)

@error_handler_decorator()
async def player_change_amq(interaction : discord.Interaction, new_amq_name : str):
    """Interaction to handle the `/player_change_amq` command. It modifies the `amq_name` field of the player using the command."""
    await interaction.response.defer(ephemeral=True)

    # NOTE Adding any other "new_amq_name" restriction needed?
    # (Doing the checks here instead of in controller to obtain easier the modified name for log purposes)
    # Make sure the name does not contains spaces
    new_amq_name = new_amq_name.replace(' ', '_')
    
    change_amq_ok, log_value = Players_Controller().change_player_amq(discord_id=interaction.user.id, new_amq_name=new_amq_name)
    
    if not change_amq_ok:
        if log_value is None:
            content = 'You are not registered in the players\'s database. Use `/player_register` instead.'
        else:
            content = f'The change couldn\'t be applied as `{discord.utils.escape_markdown(new_amq_name)}` is already used as the `amq_name` of {log_value}.'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    log_thread = await Channels().get_player_change_amq_thread(interaction.client)
    content = f'{interaction.user.mention} changed their AMQ name:\n'
    content += f'Old AMQ Name: **{discord.utils.escape_markdown(log_value)}**\n'
    content += f'New AMQ Name: **{discord.utils.escape_markdown(new_amq_name)}**'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content='AMQ name changed successfully!', ephemeral=True)


@error_handler_decorator()
async def player_change_other_amq(interaction : discord.Interaction, player_old_amq : str, player_new_amq : str):
    """Interaction to handle the `/player_change_other_amq` command. It modifies the `amq_name` field of the player with `amq_name == player_old_amq`."""
    await interaction.response.defer(ephemeral=True)

    # NOTE Make sure to match these restrictions with the player_change_amq ones
    player_new_amq = player_new_amq.replace(' ', '_')
    
    # Get the discord id of the player with amq name == player_old_amq
    player = Players_Controller().get_player(player_old_amq)

    if player is None:
        content = f'A player with a similar enough amq_name to "**{player_old_amq}**" couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    try:
        player_discord = await interaction.client.fetch_user(player.discord_id)
        player_mention = player_discord.mention if player_discord.mention else player_discord.name
    except (discord.errors.NotFound, discord.errors.HTTPException):
        player_mention = '(???)'

    change_amq_ok, log_value = Players_Controller().change_player_amq(discord_id=player.discord_id, new_amq_name=player_new_amq)
    
    if not change_amq_ok:
        content = f'The change couldn\'t be applied as `{discord.utils.escape_markdown(player_new_amq)}` is already used as the `amq_name` of {log_value}.'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    log_thread = await Channels().get_player_change_amq_thread(interaction.client)
    content = f'{interaction.user.mention} changed the AMQ name of {player_mention}:\n'
    content += f'Old AMQ Name: **{discord.utils.escape_markdown(log_value)}**\n'
    content += f'New AMQ Name: **{discord.utils.escape_markdown(player_new_amq)}**'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content=f'AMQ name of {player_mention} changed successfully!', ephemeral=True)


@error_handler_decorator()
async def player_get_profile(interaction : discord.Interaction, amq_name : str, discord_name : str):
    """
    Interaction to handle the `/player_get_profile` command. It displays an embed with information abou the user
    and a view with 2 buttons that allows the users to display more information abou them.
    """

    class Player_Get_Profile_View(discord.ui.View):

        def __init__(self, player : Player, initial_page : int):
            super().__init__(timeout=180)
            self.player = player
            self.current_page = initial_page

        @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.green)
        async def previous_profile_page(self, new_interaction : discord.Interaction, _ : discord.ui.Button):
            embed, self.current_page = await self.player.get_profile_embed(new_interaction.client, self.current_page - 1)
            await new_interaction.response.edit_message(embed=embed)

        @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.green)
        async def next_profile_page(self, new_interaction : discord.Interaction, _ : discord.ui.Button):
            embed, self.current_page = await self.player.get_profile_embed(new_interaction.client, self.current_page + 1)
            await new_interaction.response.edit_message(embed=embed)


    await interaction.response.defer(ephemeral=False)
    
    # Obtain the player:
    # - If neither amq_name nor discord_name were provided -> obtain the player who is using the command
    # - If both amq_name and discord_name were provided -> amq_name value is used (discord_name is ignored)
    if not amq_name and not discord_name:
        player = Players_Controller().get_player(interaction.user.id)
    elif not amq_name:
        player = Players_Controller().get_player_from_discord_name(interaction.guild, discord_name)
    else:
        player = Players_Controller().get_player(amq_name)
    
    # Check if player was obtained successfully
    if player is None:
        content = 'I couldn\'t find a player with the provided argument :('
        await interaction.followup.send(content=content, ephemeral=False)
        return

    embed, initial_page = await player.get_profile_embed(interaction.client)
    view = Player_Get_Profile_View(player=player, initial_page=initial_page)
    await interaction.followup.send(embed=embed, view=view, ephemeral=False)


@error_handler_decorator()
async def player_change_list(interaction : discord.Interaction, new_list_name : str, new_list_from : str, new_list_sections : str):
    """Interaction to handle the `/player_change_list` command. It modifies the list fields of the player using the command."""
    await interaction.response.defer(ephemeral=True)

    change_list_ok, log = Players_Controller().change_player_list(
        discord_id=interaction.user.id,
        new_list_name=new_list_name,
        new_list_from=new_list_from,
        new_list_sections=new_list_sections
    )

    if not change_list_ok:
        content = 'You are not registered in the players\'s database. Use `/player_register` first.'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    content = f'Changes applied successfully!\n\nThis is your current list information:\n{log}'
    await interaction.followup.send(content=content, ephemeral=True)


@error_handler_decorator()
async def player_change_mode(interaction : discord.Interaction, type : discord.app_commands.Choice[int]):
    """Interaction to handle the `/player_change_mode` command. It modifies the `type` field of the player using the command."""
    
    class Gamemodes_Dropdown(discord.ui.Select):
        
        def __init__(self, option : int, gamemodes : list[Gamemode]):
            options = [discord.SelectOption(label=gamemode.name, value=gamemode.id) for gamemode in gamemodes]
            super().__init__(placeholder='Choose Gamemode', options=options)
            self.option = option

        async def callback(self, new_interaction: discord.Interaction):
            await new_interaction.response.defer(ephemeral=True)
            Players_Controller().change_player_prefered_gamemodes(discord_id=new_interaction.user.id, prefered_gamemode_option=self.option, gamemode_id=int(self.values[0]))
            content = Players_Controller().get_player(id_or_name=new_interaction.user.id).display_gamemodes_info()
            await new_interaction.followup.send(content=content, ephemeral=True)
    

    class Gamemodes_Dropdown_View(discord.ui.View):
        
        def __init__(self, option : int, gamemodes : list[Gamemode]):
            super().__init__(timeout=180)

            # Splitting gamemodes list into sublists with a max size of 25 gamemodes (max gamemodes that can be displayable into a select menu)
            # We then show as many select menus as sublists are:
            # 1: if 25 gamemodes or less
            # 2: if +25 gamemodes and 50 gamemodes or less
            # ...
            n = 25
            gamemodes_sublists = [gamemodes[i:i + n] for i in range(0, len(gamemodes), n)]
            for gamemode_sublist in gamemodes_sublists:
                self.add_item(Gamemodes_Dropdown(option, gamemode_sublist))
    

    await interaction.response.defer(ephemeral=True)
    gamemodes = Main_Controller().get_gamemodes()

    enum_option = Prefered_Gamemode_Options(type.value)
    match enum_option:
        case Prefered_Gamemode_Options.Fav_1v1_Gamemode | Prefered_Gamemode_Options.Hated_1v1_Gamemode:
            gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 1]
        case Prefered_Gamemode_Options.Fav_2v2_Gamemode | Prefered_Gamemode_Options.Hated_2v2_Gamemode:
            gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 2]
        case Prefered_Gamemode_Options.Fav_4v4_Gamemode | Prefered_Gamemode_Options.Hated_4v4_Gamemode:
            gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 4]
        case _:
            raise ValueError('Invalid type chosen!')
    
    content = 'If you see more than one menu to select, this means that all possible options could\'t be shown in one menu'
    view = Gamemodes_Dropdown_View(option=type.value, gamemodes=sorted(gamemodes))
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def player_change_ban(interaction : discord.Interaction, amq_name : str, is_banned : bool):
    """Interaction to handle the `/player_change_ban` command. It bans/unbans the `is_banned` field of the player with `name` == `amq_name`."""
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
    banned_value = "banned" if player.is_banned else "unbanned"
    content = f'{interaction.user.mention} has {banned_value} {player.discord_ping} ({player.amq_name})'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content=f'{player.discord_ping} ({player.amq_name}) has been {banned_value} successfully!', ephemeral=True)


@error_handler_decorator()
async def player_change_rank(interaction : discord.Interaction, amq_name : str, new_rank : str):
    """Interaction to handle the `/player_change_rank` command. It modifies the `rank` field of the player with `name` == `amq_name`."""
    await interaction.response.defer(ephemeral=True)

    applied, player, old_rank = Players_Controller().change_player_rank(amq_name, new_rank)
    if not applied:
        content = f'A player with name "{amq_name}" couldn\'t be found'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    log_thread = await Channels().get_player_change_rank_thread(interaction.client)
    content = f'{interaction.user.mention} modified the rank of {player.discord_ping} ({player.amq_name})\n'
    content += f'- **Old Rank:** {old_rank}\n'
    content += f'- **New Rank:** {player.rank.name}'
    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())
    await interaction.followup.send(content='Rank modified successfully!', ephemeral=True)


@error_handler_decorator()
async def player_show_ranking(interaction : discord.Interaction, rank_page : str):
    """
    Interaction to handle the `/player_show_ranking` command. It displays an embed with all the players that have `rank_page` as their Rank
    and a view with 2 buttons that allows the users to display the information about other ranks.
    """

    class Player_Show_Ranking_View(discord.ui.View):

        def __init__(self, initial_page : int):
            super().__init__(timeout=180)
            self.current_page = initial_page

        @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.green)
        async def show_previous_page(self, new_interaction : discord.Interaction, _ : discord.ui.Button):
            embed, self.current_page = Ranking().get_rank_embed(new_interaction.guild, self.current_page - 1)
            await new_interaction.response.edit_message(embed=embed)

        @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.green)
        async def show_next_page(self, new_interaction : discord.Interaction, _ : discord.ui.Button):
            embed, self.current_page = Ranking().get_rank_embed(new_interaction.guild, self.current_page + 1)
            await new_interaction.response.edit_message(embed=embed)


    await interaction.response.defer(ephemeral=False)

    rank = Ranking().get_rank(rank_page)
    embed, initial_page = Ranking().get_rank_embed(interaction.guild, rank.value)
    view = Player_Show_Ranking_View(initial_page)

    await interaction.followup.send(embed=embed, view=view, ephemeral=False)