import difflib
import asyncio
from datetime import datetime

import discord

from Code.Players.player import Player
from Code.Tours.team import Team
from Code.Tours.enums import Teams
from Code.Utilities.escape_markdown import escape_markdown

class Tour:
    """Class that instanciates a Tour object."""

    def __init__(
        self,
        tour_id : int,
        host : discord.User,
        guild : discord.Guild,
        timer : float = None,
        max_players_size : int = None,
        counts_for_elo : bool = False,
        tour_info : str = ''
    ) -> None:
        """Constructor of the Tour class."""
        self._tour_id = tour_id
        self._guild_id = guild.id
        self._host = host
        self._is_tour_open = True
        self._is_tour_active = True

        self._timer = None
        self._task : asyncio.Task = None   # inform host that timer ended task
        self._set_timer(timer)

        self._max_players_size = max_players_size
        self._counts_for_elo = counts_for_elo
        self._tour_info = tour_info

        self._join_message = None
        self._players_message = None

        self._players = []
        self._queue = []
        self._teams = [Team(guild_id=self._guild_id, team_id=team_id) for team_id in range(len(Teams))]


    # No setter, final
    @property
    def tour_id(self) -> int:
        return self._tour_id
    
    # No setter, final
    @property
    def guild_id(self) -> int:
        return self._guild_id


    # No setter, final
    @property
    def host(self) -> discord.User:
        return self._host
    

    @property
    def is_tour_open(self) -> bool:
        return self._is_tour_open
    
    @is_tour_open.setter
    def is_tour_open(self, new_is_tour_open : bool) -> None:
        self._is_tour_open = new_is_tour_open

    @property
    def is_tour_active(self) -> bool:
        return self._is_tour_active
    
    @is_tour_active.setter
    def is_tour_active(self, new_is_tour_active : bool) -> None:
        self._is_tour_active = new_is_tour_active
    

    @property
    def timer(self) -> float | None:
        """Return POSIX timestamp as float if a timer was established before, else `None`"""
        return self._timer
    
    @timer.setter
    def timer(self, new_timer : float | None) -> None:
        self._set_timer(new_timer=new_timer)

    
    @property
    def max_players_size(self) -> int | None:
        return self._max_players_size
    
    @max_players_size.setter
    def max_players_size(self, new_max_players_size : int | None) -> None:
        self._max_players_size = new_max_players_size

    
    @property
    def counts_for_elo(self) -> bool:
        return self._counts_for_elo
    
    @counts_for_elo.setter
    def counts_for_elo(self, new_counts_for_elo : bool) -> None:
        self._counts_for_elo = new_counts_for_elo
    

    @property
    def tour_info(self) -> str:
        return self._tour_info
    
    @tour_info.setter
    def tour_info(self, new_tour_info : str) -> None:
        self._tour_info = new_tour_info


    @property
    def join_message(self) -> discord.Message | None:
        return self._join_message
    
    @join_message.setter
    def join_message(self, new_join_message : discord.Message) -> None:
        self._join_message = new_join_message
    

    @property
    def players_message(self) -> discord.Message | None:
        return self._players_message
    
    @players_message.setter
    def players_message(self, new_player_message : discord.Message) -> None:
        self._players_message = new_player_message
    

    # No setter, add players one by one using `self.add_player()` 
    @property
    def players(self) -> list[Player]:
        return self._players
    
    @property
    def queue(self) -> list[Player]:
        return self._queue
    
    @property
    def teams(self) -> list[Team]:
        return self._teams
    

    @property
    def max_size_restriction_ok(self) -> bool:
        return self.max_players_size is None or self.max_players_size > len(self.players)

    @property
    def timer_restriction_ok(self) -> bool:
        return self.timer is None or self.timer > datetime.now().timestamp()


    async def _inform_host_timer_ended(self, timer : float):
        """Inform the host that the timer has ended."""
        await asyncio.sleep(timer)
        try:
            await self.host.send(f'Timer ended!\n{self.join_message.jump_url}')
        except discord.errors.Forbidden:
            # Host has dm closed, we don't send the message then
            pass

    async def _inform_host_players_limit_reached(self):
        """Inform the host that the timer has ended."""
        try:
            await self.host.send(f'Max number of players reached!\n{self.join_message.jump_url}')
        except discord.errors.Forbidden:
            # Host has dm closed, we don't send the message then
            pass
    

    def _set_timer(self, new_timer : float | None) -> None:
        """Update the timer and create an asyncio task to send a message to the host's dms once the timer is finished."""
        self._timer = datetime.now().timestamp() + new_timer * 60 if new_timer is not None else None

        if self._timer is not None:
            # Cancel current timer task if exists and not yet finished
            if self._task is not None and not self._task.done():
                self._task.cancel()

            self._task = asyncio.create_task(self._inform_host_timer_ended(new_timer * 60))            


    def generate_join_embed(self) -> discord.Embed:
        """Return the join embed given the stored tour data."""
        title = f'{self.host.name}\'s Tour!'
        url = self.host.display_avatar.url

        timer = f'<t:{int(self.timer)}:R>' if self.timer is not None else 'Not yet established'
        size = f'{self.max_players_size} players' if self.max_players_size is not None else 'Not yet established'
        info = self.tour_info if len(self.tour_info) > 0 else 'Not yet established'
        sign_ups_open = 'Yes' if self.is_tour_open else 'No'

        embed = discord.Embed(title=title, color=discord.Color.green())
        embed.set_thumbnail(url=url)
        embed.add_field(name='Sign up closes', value=timer, inline=False)
        embed.add_field(name='Space for', value=size, inline=False)
        embed.add_field(name='Looking for players', value=sign_ups_open, inline=False)
        embed.add_field(name='Tour\'s info', value = info, inline=False)

        return embed
    

    def _display_tour_players(self, sort : bool) -> str:
        """Return a `str` with the information about the players's list escaping markdown characters."""
        players_count = len(self.players)
        players = sorted(self.players) if sort else self.players
        players_list = [f'{player.amq_name} ({player.rank.name})' for player in players]
        players_data = escape_markdown(", ".join(players_list))
        summary = f'**Players ({players_count}):** {players_data}'
        return summary
    
    def _display_tour_queue(self, sort : bool) -> str:
        """Return a `str` with the information about the players's queue escaping markdown characters."""
        queue_count = len(self.queue)
        queue = sorted(self.queue) if sort else self.queue
        queue_list = [f'{player.amq_name} ({player.rank.name})' for player in queue]
        queue_data = escape_markdown(", ".join(queue_list))
        summary = f'**Queue ({queue_count}):** {queue_data}'
        return summary
    
    def display_tour_players_and_queue(self, sort : bool = False) -> str:
        """Return a `str` with the information about the players's list and queue escaping markdown characters."""
        return f'{self._display_tour_players(sort)}\n{self._display_tour_queue(sort)}'

    def display_tour_players_mentions(self) -> str:
        """Return a `str` with the discord mentions from the players's list."""
        return ' '.join([player.discord_ping for player in self.players])
    

    def get_tour_player(self, player_name : str) -> Player | None:
        """Given the name of a player, return the closest match among all the tours players to `player.amq_name` (or `None` if a close enough match couldn't be found)."""
        players_by_names = {player.amq_name.lower() : player for player in self.players}
        possibilities = [player.amq_name.lower() for player in self.players]
        closest_matches = difflib.get_close_matches(player_name.lower(), possibilities)
        
        if not closest_matches:
            return None
        closest_match = players_by_names.get(closest_matches[0])
        return closest_match


    def add_player(self, player : Player, privileged : bool = False) -> tuple[bool, bool]:
        """
        Add a player to the tour's player list.\n
        `privileged` value can be set in order to ignore some restrictions (i.e. the timer).\n
        Returns a tuple consisting of 2 booleans:
        - Whether the player entered the tour.
        - Whether the player joined the tour's players list (instead of the queue).
        """
        # NOTE Splitting privileged and not privileged completely for easier understanding
        if not privileged:
            # CASE 1: Player don't join neither players's list nor queue:
            # TODO Add if player is banned from tours check as well... maybe?
            if not self.is_tour_open or player in self.players:
                return False, False

            # CASE 2: Player joins the queue instead of the players's list
            if not self.max_size_restriction_ok or not self.timer_restriction_ok:
                if player in self.queue:    # Make sure player is not already in the queue (prevent duplicates)
                    return False, False
                
                self.queue.append(player)
                return True, False
            
            # CASE 3: Player enter the player's list (If CASE 1 and CASE 2 were False)
            if player in self.queue:        # Check if the player was already in the queue, and remove them from the queue if so
                self.queue.remove(player)
            
            self.players.append(player)

            # Check if the max player limit has been reached
            if self.max_players_size is not None and self.max_players_size == len(self.players):
                # NOTE Inform the host that the size limit has been reached
                asyncio.create_task(self._inform_host_players_limit_reached())

            return True, True
        
        else:
            # CASE 1: we ignore the "tour not open" restriction
            if player in self.players:
                return False, False
            
            # CASE 2: we ignore the "timer" restriction
            if not self.max_size_restriction_ok:
                if player in self.queue:
                    return False, False
                
                self.queue.append(player)
                return True, False
            
            # CASE 3: Same as in not restricted
            if player in self.queue:
                self.queue.remove(player)
            
            self.players.append(player)
            return True, True
    

    async def remove_player(self, client : discord.Client, player : Player) -> tuple[bool, bool]:
        """
        Remove a player from the tour.\n
        Return a tuple consisting of 2 booleans:
        - First one: True if the player was successfully removed and False otherwise.
        - Second one: True if the removed player was in the player list and False if it was in the queue.
        """
        # CASE 1: Player not in tour
        if player not in self.players and player not in self.queue:
            return False, False
        
        # CASE 2: Player in queue
        elif player in self.queue:
            self.queue.remove(player)
            return True, False

        # CASE 3: Player in players's list
        # 1.- Remove player from teams and remove their team role (if proceed)
        [await team.remove_player(client, player) for team in self.teams if player in team.players]

        # 2.- Remove the player
        self.players.remove(player)

        # 3.- Add to the players list the player who has been waiting the most in queue
        if self.is_tour_open and len(self.queue) > 0 and self.timer_restriction_ok:
            player_in_queue = self.queue.pop(0)
            self.players.append(player_in_queue)

        return True, True
    

    async def add_to_team(self, client : discord.Client, team_index : int, player : Player) -> bool:
        """Add a player to a team. Return whether the player was added (False if they were already in the team)."""
        # Make sure the player doesn't end up in more than one team
        for index, team in enumerate(self.teams):
            if index == team_index:
                continue

            if player in team.players:
                await team.remove_player(client, player)
        
        return await self.teams[team_index].add_player(client, player)
    

    async def remove_from_team(self, client : discord.Client, team_index : int, player : Player) -> bool:
        """Remove a player from a team. Return whether the player was removed (False if they were not in the team)."""
        try:
            team = self.teams[team_index]
            return await team.remove_player(client, player)
        
        except IndexError:
            return False
        

    def get_players_not_in_team(self) -> str:
        """Return a string containing all the players that are in the tour players list but that haven't been added yet to any team."""
        players = []
        for player in self.players:
            in_team = False

            for team in self.teams:
                if player in team.players:
                    in_team = True
                    break

            if not in_team:
                players.append(player)
        
        players = sorted(players)
        players_data = [f'{escape_markdown(player.amq_name)} ({player.rank.name})' for player in players]
        players_str = ', '.join(players_data)
        answer = f'**Not in team ({len(players)})**: {players_str}'
        return answer