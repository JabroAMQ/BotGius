import random
from copy import copy

from Code.Rolls.enums import Roll_Teams
from Code.Players.player import Player

class Teams_Roll:
    """Static class that contains the methods to split a list of players into different teams."""

    @staticmethod
    def roll_teams(type: Roll_Teams, player_list: list[Player], num_teams: int = 2) -> tuple[list[list[Player]], str]:
        """
        Split the `player_list` into `num_teams` teams following a different criteria based on the `type` provided.\n
        Return a tuple consisting of 2 elements:
        - `list[list[Player]]`: The list of the teams (as `list[Player]`) rolled.
        - `str`: A string representation of the teams rolled.
        """
        player_list_copy = copy(player_list)

        match type:

            case Roll_Teams.FULL_RANDOM:
                teams = Teams_Roll._roll_teams_random(player_list_copy, num_teams)
            
            case Roll_Teams.BALANCED:
                teams = Teams_Roll._roll_teams_balanced(player_list_copy, num_teams)
            
            case Roll_Teams.GROUPED_BY_STRENGTH:
                teams = Teams_Roll._roll_teams_grouped_by_strength(player_list_copy, num_teams)

            case _:
                raise ValueError('Invalid "type" provided!')

        teams_str = Teams_Roll._teams_as_str(teams)
        return teams, teams_str


    @staticmethod
    def _roll_teams_random(player_list: list[Player], num_teams: int) -> list[list[Player]]:
        """
        Split the `player_list` into `num_teams` teams.\n
        All teams will have the same number of players.\n
        Players are "drafted" to one team randomly.
        """
        teams = [[] for _ in range(num_teams)]
        num_players = len(player_list)

        for i in range(num_players):
            player = random.choice(player_list)
            teams[i%num_teams].append(player)
            player_list.remove(player)

        return teams


    @staticmethod
    def _roll_teams_balanced(player_list: list[Player], num_teams: int) -> list[list[Player]]:
        """
        Split the `player_list` into `num_teams` teams.\n
        All teams will have the same number of players.\n
        All teams will have as similar strength as possible.
        """
        # Manually sort the players to not take into account the `amq_name` value
        # Sorted based on `rank` and, for those with the same rank, random (so different results can be provided given the same arguments)
        random.shuffle(player_list)
        player_list = sorted(player_list, key=lambda x: x.rank)
    
        teams = [[] for _ in range(num_teams)]
        
        for i, player in enumerate(player_list):
            # Zig-Zag / Snake pattern:
            # First runner assigned like: team_1, team_2, ..., team_n
            # Second one like: team_n, team_n-1, ..., team_1
            if i % (2 * num_teams) < num_teams:
                team_idx = i % num_teams
            else:
                team_idx = num_teams - 1 - (i % num_teams)

            teams[team_idx].append(player)

        return teams
    

    @staticmethod
    def _roll_teams_grouped_by_strength(player_list: list[Player], num_teams: int) -> list[list[Player]]:
        """
        Split the `player_list` into `num_teams` teams.\n
        All teams will have the same number of players.\n
        Players will be grouped in a team with other players with similar strength.
        """
        # Manually sort the players to not take into account the `amq_name` value
        # Sorted based on `rank` and, for those with the same rank, random (so different results can be provided given the same arguments)
        random.shuffle(player_list)
        player_list = sorted(player_list, key=lambda x: x.rank)
    
        teams = [[] for _ in range(num_teams)]
        players_per_team = len(player_list) // num_teams

        for i in range(num_teams):
            teams[i] = player_list[i*players_per_team:(i+1)*players_per_team]

        return teams
    

    @staticmethod
    def _teams_as_str(teams: list[list[Player]]) -> str:
        """Return a string representation for the `teams` rolled."""
        teams_as_str = ''
        for i, team in enumerate(teams):
            team_players = [f'{player.amq_name} ({player.rank.name})' for player in team]
            teams_as_str += f'**Group {i+1} ({len(team)}):** '
            teams_as_str += ', '.join(team_players)
            teams_as_str += '\n'
        return teams_as_str