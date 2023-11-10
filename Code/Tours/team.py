import discord

from Code.Utilities.escape_markdown import escape_markdown
from Code.Tours.enums import Teams
from Code.Players.player import Player
from Code.Others.roles import Roles

class Team:

    def __init__(self, guild_id : int, team_id : int) -> None:
        self._name = Teams(team_id).name.replace('_', ' ')
        self._role_index = team_id
        self._guild_id = guild_id
        self._players = []


    @property
    def players(self) -> list[Player]:
        return self._players


    async def add_player(self, client : discord.Client, player : Player) -> bool:
        """Add a player to the team. Return whether the player was added (False if they were already in the team)."""
        if player in self.players:
            return False
        
        await Roles().add_team_role(client, player.discord_id, self._guild_id, self._role_index)
        self.players.append(player)
        return True

    async def remove_player(self, client : discord.Client, player : Player) -> bool:
        """Remove a player from the team. Return whether the player was removed (False if they were not in the team)."""
        if player not in self.players:
            return False
        
        await Roles().remove_team_roles(client, player.discord_id, self._guild_id)
        self.players.remove(player)
        return True

    async def reset_roles(self, client : discord.Client) -> None:
        """Clear all the roles from the players without removing them from their team."""
        [await Roles().remove_team_roles(client, player.discord_id, self._guild_id) for player in self.players]

    def display_team(self, sort : bool = True) -> str:
        """Return a `str` with the information about the team's players list escaping markdown characters."""
        players_count = len(self.players)
        players = sorted(self.players) if sort else self.players
        players_list = [f'{player.amq_name} ({player.rank.name})' for player in players]
        players_data = escape_markdown(", ".join(players_list))
        summary = f'**{self._name} ({players_count}):** {players_data}'
        return summary