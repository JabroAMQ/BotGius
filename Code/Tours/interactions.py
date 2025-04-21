import re
from copy import copy

import discord

from Code.Utilities.error_handler import error_handler_decorator
from Code.Tours.controller import Tours_Controller
from Code.Tours.tour import Tour
from Code.Tours.team import Team
from Code.Players.controller import Players_Controller
from Code.Players.player import Player
from Code.Rolls.teams import Teams_Roll
from Code.Rolls.blind_crews import Blind_Crews
from Code.Rolls.enums import Roll_Teams, Roll_Gamemode
from Code.Others.channels import Channels
from Code.Others.emojis import Emojis
from Code.Others.roles import Roles


async def _log_command(interaction: discord.Interaction, command_name: str, tour: Tour, args: list[str]):
    """
    Auxiliar method for logging tour commands that modify/ends the tour being hosted at the moment.\n
    Current commands that are logged:
    - `/tour_edit`
    - `/tour_players_add`
    - `/tour_players_remove`
    - `/tour_players_ping`
    - `/tour_end`
    - `/team_players_add`
    - `/team_players_remove`
    - `/team_randomize`
    - `/roll_groups`
    - `/roll_blind_crews`
    """
    user: Player = Players_Controller().get_player(interaction.user.id)
    host: Player = Players_Controller().get_player(tour.host.id)
    
    # TODO Should we only log the command if someone who is not the original host is trying to modify the tour's data?
    """
    if user.id == host.id:
        return
    """

    log_thread = await Channels().get_commands_usage_thread(interaction.client)
    args = [f'- {arg}\n' for arg in args if arg is not None]
    content = f'{user.discord_ping} ({user.amq_name}) used command `/{command_name}` in {host.discord_ping} ({host.amq_name})\'s tour'
    if args:
        content += ' with parameters:\n'
        content += ''.join(args)

    await log_thread.send(content=content, allowed_mentions=discord.AllowedMentions.none())


@error_handler_decorator()
async def tour_create(interaction: discord.Interaction, timer: int = None, size: int = None, info: str = '', custom_ping: str = ''):
    """Interaction to handle the `/tour_create` command. It creates a new tour and stores it in the tours's catalog."""
    await interaction.response.defer(ephemeral=True)
    join_emoji, leave_emoji = Emojis().get_tour_emojis(interaction.user.id)


    class Tour_Create_View(discord.ui.View):
        def __init__(self, tour: Tour):
            super().__init__(timeout=18000)     # 5 hours timeout
            self.tour = tour

        @discord.ui.button(label='Join', emoji=join_emoji, style=discord.ButtonStyle.green)
        async def join(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)

            # Make sure tour is still active...
            if not self.tour.is_tour_active:
                content = 'This tour has already ended'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            # Get the player who is trying to join the tour
            player = Players_Controller().get_player(new_interaction.user.id)
            if player is None:
                content = 'You need to register first! (`/player_register`)'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            # Make sure that the player is not banned
            # NOTE we add it here to make it easier to send a different response
            # Also we let tour helpers add banned people from `/tour_players_add` command (ban only affect if joning through this button)
            if player.is_banned:
                content = 'You couldn\'t join the tour because you are banned :worried:'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            # Try to add the player to the tour and inform the user about the result
            join_ok, in_players_list = self.tour.add_player(player)
            if not join_ok:
                content = 'You couldn\'t join the tour. This can happen for one of the following reasons:\n'
                content += '- You are already in the players\'s list / queue\n'
                content += '- The tour\'s sign ups are already closed'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            list_added_to = 'players\'s list' if in_players_list else 'queue'
            content = f'You were added to the **{list_added_to}** successfully!\n'
            content += 'Remember that you have to leave the tour if you can no longer play'
            await new_interaction.followup.send(content=content, ephemeral=True)

            # Modify the player's message accordingly
            players = tour.display_tour_players_and_queue()
            await tour.players_message.edit(content=players)


        @discord.ui.button(label='Leave', emoji=leave_emoji, style=discord.ButtonStyle.green)
        async def leave(self, new_interaction: discord.Interaction, _: discord.Button):
            # Make sure tour is still active...
            if not self.tour.is_tour_active:
                content = 'This tour has already ended'
                await new_interaction.response.send_message(content=content, ephemeral=True)
                return
            
            await tour_quit(interaction=new_interaction, tour=self.tour)


    # Create a new tour
    tour = Tours_Controller().start_new_tour(
        host=interaction.user,
        guild=interaction.guild,
        timer=timer,
        size=size,
        elo=False,
        info=info
    )

    pings = Roles().get_ping_roles() if not custom_ping else custom_ping
    emoji = Emojis().get_other_emoji('20espiando')
    content = f'{pings} {emoji}'
    embed = tour.generate_join_embed()
    view = Tour_Create_View(tour=tour)
    players = tour.display_tour_players_and_queue()
    
    tour.join_message = await interaction.channel.send(content=content, embed=embed, view=view)
    tour.players_message = await interaction.channel.send(content=players)

    await interaction.followup.send(content='Tour set up successfully!', ephemeral=True)


@error_handler_decorator()
async def tour_edit(interaction: discord.Interaction, timer: int | None, max_size: int | None, is_open: bool | None, info: bool | None):
    """Interaction to handel the `/tour_edit` command. It allows the host to modify sign-ups related parameters's values from the active tour."""
    await interaction.response.defer(ephemeral=True)

    # Make sure at least one value was provided
    if timer is None and max_size is None and is_open is None and info is None:
        content = 'At least one parameter must be provided!'
        await interaction.followup.send(content=content, ephemeral=True)
        return

    # Get the tour that is currently active
    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
     
    content = 'This is the result:\n'
    queue_to_player_list = False        # whether to try to move queue to player list after applying the tour changes
    player_list_to_queue = False        # whether to try to move player list to queue (max size has been reduced to a value lower than the current player list size)


    if timer is not None:
        queue_to_player_list = True
        tour.timer = timer
        content += '- Timer modified successfully.\n'

    if max_size is not None:
        if max_size < len(tour.players):
            player_list_to_queue = True
        else:
            queue_to_player_list = True
        
        tour.max_players_size = max_size
        content += '- Max Size modified successfully.\n'

    if is_open is not None:
        queue_to_player_list = True
        tour.is_tour_open = is_open
        content += '- "Looking for players" modified successfully.\n'

    if info is not None:
        tour.tour_info = info
        content += '- Info modified successfully\n'


    # Move some players to the queue if max size was reduced
    if player_list_to_queue:
        content += '\n**These players were moved from the players\'s list to the top of the queue:**\n'
        moved_players = []

        while len(tour.players) > max_size:
            # Move the last players that joined the players's list to the top of the queue (priority over other queue people that were never in the players's list)
            last_player = tour.players[-1]
            moved_players.insert(0, discord.utils.escape_markdown(last_player.amq_name))
            await tour.from_player_list_to_queue(interaction.client, last_player)
        content += ', '.join(moved_players)

        # Display the players's list / queue changes
        players = tour.display_tour_players_and_queue()
        await tour.players_message.edit(content=players)


    # Move queue to player list if new timer, max size was increased or tour sign ups were reopened
    elif queue_to_player_list:
        # We need to create a copy as tour.queue is going to be modified in tour.add_player()
        queue_copy = copy(tour.queue)
        [tour.add_player(player, privileged=True) for player in queue_copy]
        
        # Display the players's list / queue changes
        players = tour.display_tour_players_and_queue()
        await tour.players_message.edit(content=players)
    

    # Display the embed changes and inform the host about the result
    embed = tour.generate_join_embed()
    await tour.join_message.edit(embed=embed)
    await interaction.followup.send(content=content, ephemeral=True)
    
    # Log the command usage
    args = [
        f'`timer`: **{timer}**' if timer is not None else None,
        f'`max_size`: **{max_size}**' if max_size is not None else None,
        f'`is_open`: **{is_open}**' if is_open is not None else None,
        f'`info`: **{discord.utils.escape_markdown(info)}**' if info is not None else None
    ]
    await _log_command(interaction, 'tour_edit', tour, args)


@error_handler_decorator()
async def tour_quit(interaction: discord.Interaction, tour: Tour = None):
    """
    Interaction to handle the `/tour_quit` command. It allows the player to leave a tour.\n
    `tour` argument is added so that this function can be reused from `/tour_create`'s `Leave` button.
    """
    await interaction.response.defer(ephemeral=True)

    # If no tour added, get current tour
    if tour is None:
        tour = await Tours_Controller().get_current_tour(interaction)
        if tour is None:
            content = 'There is not a tour active at the moment'
            await interaction.followup.send(content=content, ephemeral=True)
            return
    
    # Get the player who is trying to leave the tour
    player = Players_Controller().get_player(interaction.user.id)
    leave_ok, from_players_list = await tour.remove_player(interaction.client, player) if player is not None else (False, False)

    if not leave_ok:
        content = 'You were not in the tour\'s players list / queue...'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Modify the player's message accordingly
    players = tour.display_tour_players_and_queue()
    await tour.players_message.edit(content=players)

    # Inform the player
    content = 'You have successfully left the tour'
    await interaction.followup.send(content=content, ephemeral=True)
    
    # Inform the host that the player left
    await _inform_host_player_left(interaction=interaction, tour=tour, player=player, from_players_list=from_players_list)


async def _inform_host_player_left(interaction: discord.Interaction, tour: Tour, player: Player, from_players_list: bool):
    """Method to send a dm message to the host when a player leaves the tour they are hosting."""
    content = f'A player left the tour:\n{tour.join_message.jump_url}'

    player_from = 'Players\'s list' if from_players_list else 'Queue'
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name=interaction.user.global_name, icon_url=interaction.user.display_avatar)
    embed.add_field(name='Discord Nickname', value=interaction.user.display_name, inline=False)
    embed.add_field(name='AMQ Name', value=discord.utils.escape_markdown(player.amq_name), inline=False)
    embed.add_field(name='From', value=player_from, inline=False)
    
    try:
        await tour.host.send(content=content, embed=embed)
    except discord.errors.Forbidden:
        # host has dms closed, we don't send them the embed then
        pass


@error_handler_decorator()
async def tour_players_add(interaction: discord.Interaction, players_str: str):
    """Interaction to handle the `/tour_players_add` command. It allows the host to manually add some players to the tour."""
    await interaction.response.defer(ephemeral=True)

    # Get the tour that is currently active
    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    players_list, queue, not_added, not_found = [[] for _ in range(4)]
    players_str = re.sub(' +', ' ', players_str)
    for player_name in players_str.split(' '):
        # Obtain the players from the input string of the host
        player = Players_Controller().get_player(player_name)
        if player is None:
            player_name = discord.utils.escape_markdown(player_name)
            not_found.append(player_name)
            continue

        # Add the players
        join_ok, in_players_list = tour.add_player(player=player, privileged=True)
        player_name = discord.utils.escape_markdown(player.amq_name)

        if not join_ok:
            not_added.append(player_name)
        elif not in_players_list:
            queue.append(player_name)
        else:
            players_list.append(player_name)

    # Inform the host
    content = 'This is the result:\n'
    if players_list:
        content += f'- **To players list:** {", ".join(players_list)}\n'
    if queue:
        content += f'- **To queue:** {", ".join(queue)}\n'
    if not_added:
        content += f'- **Not added** (already in tour?): {", ".join(not_added)}\n'
    if not_found:
        content += f'- **Couldn\'t find player from name provided:** {", ".join(not_found)}'
    await interaction.followup.send(content=content, ephemeral=True)

    # Modify the player's message accordingly
    tour_players = tour.display_tour_players_and_queue()
    await tour.players_message.edit(content=tour_players)

    # Log the command usage
    args = [f'`players`: **{discord.utils.escape_markdown(players_str)}**']
    await _log_command(interaction, 'tour_players_add', tour, args)


@error_handler_decorator()
async def tour_players_remove(interaction: discord.Interaction, players_str: str):
    """Interaction to handle the `/tour_players_remove` command. It allows the host to manually remove some players from the tour."""
    await interaction.response.defer(ephemeral=True)
    
    # Get the tour that is currently active
    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    from_players_list, from_queue, not_in_tour, not_found = [[] for _ in range(4)]
    players_str = re.sub(' +', ' ', players_str)
    for player_name in players_str.split(' '):
        # Obtain the players from the input string of the host
        player = Players_Controller().get_player(player_name)
        if player is None:
            player_name = discord.utils.escape_markdown(player_name)
            not_found.append(player_name)
            continue

        # Remove the players
        removed, from_active = await tour.remove_player(client=interaction.client, player=player)
        player_name = discord.utils.escape_markdown(player.amq_name)

        if not removed:
            not_in_tour.append(player_name)
        elif not from_active:
            from_queue.append(player_name)
        else:
            from_players_list.append(player_name)

    # Inform the host
    content = 'This is the result:\n'
    if from_players_list:
        content += f'- **From players list:** {", ".join(from_players_list)}\n'
    if from_queue:
        content += f'- **From queue:** {", ".join(from_queue)}\n'
    if not_in_tour:
        content += f'- **Not deleted** (they were not in tour?): {", ".join(not_in_tour)}\n'
    if not_found:
        content += f'- **Couldn\'t find player from name provided:** {", ".join(not_found)}'
    await interaction.followup.send(content=content, ephemeral=True)

    # Modify the player's message accordingly
    tour_players = tour.display_tour_players_and_queue()
    await tour.players_message.edit(content=tour_players)

    # Log the command usage
    args = [f'`players`: **{discord.utils.escape_markdown(players_str)}**']
    await _log_command(interaction, 'tour_players_remove', tour, args)


@error_handler_decorator()
async def tour_players_list(interaction: discord.Interaction):
    """Interaction to handle the `/tour_players_list` command. It send a message with the list of players that joined the tour sorted by their rank."""
    await interaction.response.defer(ephemeral=False)

    # Get the tour that is currently active
    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=False)
        return

    # Get the sorted player list (and queue)
    content = tour.display_tour_players_and_queue(sort=True)
    await interaction.followup.send(content=content, ephemeral=False)


@error_handler_decorator()
async def tour_players_ping(interaction: discord.Interaction):
    """Interaction to handle the `/tour_players_ping` command. It send a message with the discord mention of all the players (not queue) that joined the tour."""
    await interaction.response.defer(ephemeral=True)

    # Get the tour that is currently active
    tour = await  Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Get the str with the players's pings
    pings = tour.display_tour_players_mentions()
    if len(pings) == 0:
        content = 'There are no players to be pinged...'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Ping the players and inform the host
    await interaction.channel.send(content=pings)
    content = 'Players pinged successfully'
    await interaction.followup.send(content=content, ephemeral=True)

    # Log the command usage
    args = []
    await _log_command(interaction, 'tour_players_ping', tour, args)


@error_handler_decorator()
async def tour_end(interaction: discord.Interaction):
    """Interaction to handle the `/tour_end` command. It ends the tour that is currently active."""
    await interaction.response.defer(ephemeral=True)

    tour: Tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    class Tour_End_Confirmation_View(discord.ui.View):
        def __init__(self, tour: Tour, host_str: str):
            super().__init__(timeout=60)
            self.tour = tour
            self.host_str = host_str
            self.already_ended = False

        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, new_interaction: discord.Interaction, _ = discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            if self.already_ended:
                await new_interaction.followup.send(content=f'The tour ({self.host_str}) has already been ended', ephemeral=True)
                return

            # End the tour
            self.already_ended = True
            await Tours_Controller().end_current_tour(tour=self.tour, guild=new_interaction.guild)

            # Modify the "Looking for players" join embed's field to False
            embed = self.tour.generate_join_embed()
            await self.tour.join_message.edit(embed=embed)
            
            # Send confirmation message
            content = 'Tour ended successfully'
            await new_interaction.followup.send(content=content, ephemeral=True)

            # Log the command usage
            args = [f'**tour:** {self.tour.join_message.jump_url}']
            await _log_command(new_interaction, 'tour_end', self.tour, args)

    host_str = f'{tour.host.name}\'s Tour: "{tour.tour_info[:20]}"'
    content = f'You have selected the next tour:\n**{host_str}**.\nPlease click the button to confirm that you want to end it'
    view = Tour_End_Confirmation_View(tour=tour, host_str=host_str)
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def team_players_list(interaction: discord.Interaction):
    """Interaction to handle the `/team_players_list` command. It send a message with the list of players that are in a team sorted by their rank."""
    await interaction.response.defer(ephemeral=False)
    
    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=False)
        return

    # Display only those teams that have at least one player in their players list
    teams = [team.display_team() for team in tour.teams if len(team.players) > 0]
    
    content = '\n'.join(teams)
    content += '\n\n' + tour.get_players_not_in_team()
    await interaction.followup.send(content=content, ephemeral=False)


@error_handler_decorator()
async def team_players_add(interaction: discord.Interaction, team_index: int, players_str: str):
    """Interaction to handle the `/team_players_add` command. It adds tour players to a specific team."""
    await interaction.response.defer(ephemeral=True)

    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    not_found, not_added = ([] for _ in range(2))
    players_str = re.sub(' +', ' ', players_str)
    for player_name in players_str.split(' '):
        # Obtain the players from the input string of the host
        player = tour.get_tour_player(player_name)
        if player is None:
            player_name = discord.utils.escape_markdown(player_name)
            not_found.append(player_name)
            continue

        # Add the player
        added_ok = await tour.add_to_team(interaction.client, team_index, player)
        if not added_ok:
            player_name = discord.utils.escape_markdown(player.amq_name)
            not_added.append(player_name)

    # Inform the host
    teams = [team.display_team() for team in tour.teams if len(team.players) > 0]
    content = '\n'.join(teams) + '\n\n' if len(teams) > 0 else ''
    if not_added:
        content += f'- **Not added** (already in team?): {", ".join(not_added)}\n'
    if not_found:
        content += f'- **Couldn\'t find player from name provided in players\'s list:** {", ".join(not_found)}\n'
    
    content += tour.get_players_not_in_team()
    await interaction.followup.send(content=content, ephemeral=True)

    # Log the command usage
    args = [
        f'`team_index`: **{team_index}**',
        f'`players`: **{discord.utils.escape_markdown(players_str)}**'
    ]
    await _log_command(interaction, 'team_players_add', tour, args)


@error_handler_decorator()
async def team_players_remove(interaction: discord.Interaction, team_index: int, players_str: str):
    """Interaction to handle the `/team_players_remove` command. It removes tour players from a specific team."""
    await interaction.response.defer(ephemeral=True)

    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    not_found, not_removed = ([] for _ in range(2))
    players_str = re.sub(' +', ' ', players_str)
    for player_name in players_str.split(' '):
        # Obtain the players from the input string of the host
        player = tour.get_tour_player(player_name)
        if player is None:
            player_name = discord.utils.escape_markdown(player_name)
            not_found.append(player_name)
            continue

        # Remove the player
        removed_ok = await tour.remove_from_team(interaction.client, team_index, player)
        if not removed_ok:
            player_name = discord.utils.escape_markdown(player.amq_name)
            not_removed.append(player_name)

    # Inform the host
    teams = [team.display_team() for team in tour.teams if len(team.players) > 0]
    content = '\n'.join(teams) + '\n\n' if len(teams) > 0 else ''
    if not_removed:
        content += f'- **Not removed** (not in team?): {", ".join(not_removed)}\n'
    if not_found:
        content += f'- **Couldn\'t find player from name provided in players\'s list:** {", ".join(not_found)}\n'

    content += tour.get_players_not_in_team()
    await interaction.followup.send(content=content, ephemeral=True)

    # Log the command usage
    args = [
        f'`team_index`: **{team_index}**',
        f'`players`: **{discord.utils.escape_markdown(players_str)}**'
    ]
    await _log_command(interaction, 'team_players_remove', tour, args)


@error_handler_decorator()
async def team_randomize(interaction: discord.Interaction, number_of_teams: int, criteria: int):
    """Interaction to handle the `/team_randomize` command. It divides the players into groups and creates tour's teams based on the result."""

    class Team_Randomize_View(discord.ui.View):

        def __init__(self, tour: Tour, players: list[Player], type: Roll_Teams, number_of_teams: int, teams: list[list[Player]]):
            super().__init__(timeout=180)
            self.tour = tour
            self.players = players
            self.type = type
            self.number_of_teams = number_of_teams
            self.teams = teams
            self.rerolled = False

        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            
            if self.rerolled:
                content = 'The teams from these message have expired since you have rerolled them'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return

            content = 'Adding the roles...'
            await new_interaction.followup.send(content=content, ephemeral=True)

            # Make sure that teams are empty before adding the new players
            for team in self.tour.teams:
                for player in team.players:
                    await team.remove_player(client=new_interaction.client, player=player)

            # Creates the teams
            for i, team in enumerate(self.teams):
                for player in team:
                    await self.tour.add_to_team(client=new_interaction.client, team_index=i, player=player)

            # Inform about the result
            real_teams = [team.display_team() for team in self.tour.teams if len(team.players) > 0]
            real_teams = '\n'.join(real_teams)
            await new_interaction.channel.send(real_teams)
            await new_interaction.followup.send(content='Roles added successfully!', ephemeral=True)

            # Log the command usage
            args = [
                f'`number_of_teams`: **{number_of_teams}**',
                f'`criteria`: **{criteria}**'
            ]
            await _log_command(interaction, 'team_randomize', tour, args)


        @discord.ui.button(label='Reroll', style=discord.ButtonStyle.green)
        async def reroll(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)

            if self.rerolled:
                content = 'The teams from these message have expired since you have rerolled them'
                await new_interaction.followup.send(content=content, ephemeral=True)
                return
            
            self.rerolled = True
            rerolled_teams, results_str = Teams_Roll.roll_teams(type=self.type, player_list=self.players, num_teams=self.number_of_teams)
            view = Team_Randomize_View(tour=self.tour, players=self.players, type=self.type, number_of_teams=self.number_of_teams, teams=rerolled_teams)
            await interaction.followup.send(content=results_str, view=view, ephemeral=True)


    await interaction.response.defer(ephemeral=True)

    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Check that there are players in the tour
    if len(tour.players) == 0:
        content = 'There are not players to randomize!'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Split the players
    type = Roll_Teams(criteria)
    player_list = tour.players
    teams, results_str = Teams_Roll.roll_teams(type=type, player_list=player_list, num_teams=number_of_teams)

    # Inform the host
    content = f'These are the teams rolled based on the {type.name.replace("_", " ").capitalize()} criteria:\n\n{results_str}'
    view = Team_Randomize_View(tour=tour, players=player_list, type=type, number_of_teams=number_of_teams, teams=teams)
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def team_get_all_roles(interaction: discord.Interaction):
    """Interaction to handle the `/team_get_all_roles` command. It adds all team roles to the interaction's user."""
    await interaction.response.defer(ephemeral=True)
    await Roles().add_all_team_roles(interaction.guild, interaction.user.id)
    content = 'All roles added successfully!'
    await interaction.followup.send(content=content, ephemeral=True)


@error_handler_decorator()
async def roll_groups(interaction: discord.Interaction, number_of_groups: int, criteria: int):
    """Interaction to handle the `/roll_groups` command. It divides the players into groups."""

    class Roll_Groups_View(discord.ui.View):

        def __init__(self, players: list[Player], type: Roll_Teams, number_of_groups: int, groups: str):
            super().__init__(timeout=180)
            self.players = players
            self.type = type
            self.number_of_groups = number_of_groups
            self.groups = groups

        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            await new_interaction.channel.send(self.groups)
            await new_interaction.followup.send(content='Groups displayed suceessfully', ephemeral=True)

            # Log the command usage
            args = [
                f'`number_of_groups`: **{number_of_groups}**',
                f'`criteria`: **{criteria}**'
            ]
            await _log_command(interaction, 'roll_groups', tour, args)


        @discord.ui.button(label='Reroll', style=discord.ButtonStyle.green)
        async def reroll(self, new_interaction: discord.Interaction, _: discord.Button):
            await new_interaction.response.defer(ephemeral=True)
            _, groups = Teams_Roll.roll_teams(type=self.type, player_list=self.players, num_teams=self.number_of_groups)
            view = Roll_Groups_View(players=self.players, type=self.type, number_of_groups=self.number_of_groups, groups=groups)
            await interaction.followup.send(content=groups, view=view, ephemeral=True)


    await interaction.response.defer(ephemeral=True)

    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Check that there are players in the tour
    if len(tour.players) == 0:
        content = 'There are not players to randomize!'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Split the players
    type = Roll_Teams(criteria)
    player_list = tour.players
    _, groups = Teams_Roll.roll_teams(type=type, player_list=player_list, num_teams=number_of_groups)

    # Inform the host
    content = f'These are the teams rolled based on the {type.name.replace("_", " ").capitalize()} criteria:\n\n{groups}'
    view = Roll_Groups_View(players=player_list, type=type, number_of_groups=number_of_groups, groups=groups)
    await interaction.followup.send(content=content, view=view, ephemeral=True)


@error_handler_decorator()
async def roll_blind_crews(interaction: discord.Interaction, criteria: int, duels: bool):
    """Interaction to handle the `/roll_blind_crews` command. It rolls a blind crews round."""
    

    class Teams_Dropdown(discord.ui.Select):
        
        def __init__(self, criteria: int, duels: bool, active_teams: list[Team]):
            options = [discord.SelectOption(label=team.name, value=str(i)) for i, team in enumerate(active_teams)]
            super().__init__(placeholder='Choose 2 teams', options=options, min_values=2, max_values=2)
            self.teams = active_teams
            self.criteria = criteria
            self.duels = duels

        async def callback(self, new_interaction: discord.Interaction):
            await new_interaction.response.defer(ephemeral=True)
            team_1 = self.teams[int(self.values[0])]
            team_2 = self.teams[int(self.values[1])]
            await roll_bc(new_interaction, self.criteria, self.duels, team_1, team_2, add_team_names=True)
    

    class Teams_Dropdown_View(discord.ui.View):
        
        def __init__(self, criteria: int, duels: bool, active_teams: list[Team]):
            super().__init__(timeout=180)
            self.add_item(Teams_Dropdown(criteria, duels, active_teams))
            

    async def roll_bc(interaction: discord.Interaction, criteria: int, duels: bool, team_1: Team, team_2: Team, add_team_names: bool = False):
        """Roll a blind crews round for 2 teams."""
        # Create the BlindCrews
        type = Roll_Gamemode(criteria)
        blind_crews = Blind_Crews(type=type, team_1=team_1.players, team_2=team_2.players)

        # Roll the blindcrews round
        blind_crews.roll_blind_crews()
        round_info = blind_crews.get_round_information()
        additional_rolls = blind_crews.special_rolls_list
        results_template = blind_crews.get_results_template(duels)

        # Send the roll information
        if add_team_names:
            round_info = f'Blind Crews rolled for **{team_1.name}** vs **{team_2.name}**:\n\n' + round_info
        main_message = await interaction.channel.send(round_info)
        [await main_message.reply(additional_roll) for additional_roll in additional_rolls]
        content = f'Blind Crews with {type.name.replace("_", " ").capitalize()} rolled successfully!'
        await interaction.followup.send(content=content, ephemeral=True)

        try:
            await interaction.user.send(results_template)
        except discord.errors.Forbidden:
            # host has dms closed, we don't send them the template then
            pass

        # Log the command usage
        args = [f'`criteria`: **{criteria}**']
        await _log_command(interaction, 'roll_blind_crews', tour, args)

        
    await interaction.response.defer(ephemeral=True)

    tour = await Tours_Controller().get_current_tour(interaction)
    if tour is None:
        content = 'There is not a tour active at the moment'
        await interaction.followup.send(content=content, ephemeral=True)
        return
    
    # Check that the tour has two teams with players
    active_teams: list[Team] = []
    for team in tour.teams:
        if len(team.players) > 0:
            active_teams.append(team)
    
    if len(active_teams) < 2:
        content = 'Blind Crews requires players to be splitted into at least 2 teams!'
        await interaction.followup.send(content=content, ephemeral=True)
    
    elif len(active_teams) == 2:
        await roll_bc(interaction, criteria, duels, active_teams[0], active_teams[1])
    
    else:
        view = Teams_Dropdown_View(criteria, duels, active_teams)
        await interaction.followup.send(view=view, ephemeral=True)