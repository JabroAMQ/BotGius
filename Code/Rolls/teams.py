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
                teams_str = Teams_Roll._teams_as_str(teams, show_team_value=True)
            
            case Roll_Teams.BALANCED_SNAKE:
                teams = Teams_Roll._roll_teams_balanced_snake(player_list_copy, num_teams)
                teams_str = Teams_Roll._teams_as_str(teams, show_team_value=True)

            case Roll_Teams.BALANCED_GREEDY:
                teams = Teams_Roll._roll_teams_balanced_greedy(player_list_copy, num_teams)
                teams_str = Teams_Roll._teams_as_str(teams, show_team_value=True)
            
            case Roll_Teams.GROUPED_BY_STRENGTH:
                teams = Teams_Roll._roll_teams_grouped_by_strength(player_list_copy, num_teams)
                teams_str = Teams_Roll._teams_as_str(teams, show_team_value=False)

            case _:
                raise ValueError('Invalid "type" provided!')

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
    def _roll_teams_balanced_snake(player_list: list[Player], num_teams: int) -> list[list[Player]]:
        """
        Split the `player_list` into `num_teams` teams.\n
        All teams will have the same number of players.\n
        All teams will have as similar strength as possible.\n
        Balancing done via Snake / Zig-Zag pattern.
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
    def _roll_teams_balanced_greedy(player_list: list[Player], num_teams: int) -> list[list[Player]]:
        """
        Split the `player_list` into `num_teams` teams.\n
        All teams will have the same number of players.\n
        All teams will have as similar strength as possible.\n
        Balancing done via Greedy pattern, meaning that players are sorted by strength and then assigned one by one to the currently weakest team.
        """
        # Manually sort the players to not take into account the `amq_name` value
        # Sorted based on `rank` and, for those with the same rank, random (so different results can be provided given the same arguments)
        random.shuffle(player_list)
        player_list = sorted(player_list, key=lambda x: x.rank)

        teams = [[] for _ in range(num_teams)]
        team_strengths = [0] * num_teams
        max_players_per_team = len(player_list) // num_teams

        for player in player_list:
            # Filter for teams that aren't 'full' yet
            available_indices = [
                i for i, team in enumerate(teams) 
                if len(team) < max_players_per_team
            ]
            
            # From the available teams, pick the one with the lowest strength
            best_idx = min(available_indices, key=lambda i: team_strengths[i])
            
            # Assign and update
            teams[best_idx].append(player)
            team_strengths[best_idx] += player.rank.value

        return teams

    @staticmethod
    def _roll_teams_optimal(player_list: list[Player], num_teams: int) -> list[list[Player]]:
        """
        Split the `player_list` into `num_teams` teams.\n
        All teams will have the same number of players.\n
        All teams will have as similar strength as possible.\n
        Balancing done via Optimal pattern, meaning that all possible combinations are evaluated to find the one that minimizes the difference in strength teams.\n

        NOTE Very computationally expensive. Before using, improve it first / Limit it usage / Return early if a certain threshold is reached.
        """
        return NotImplementedError('Optimal team rolling is not implemented yet!')
        """
        # Manually sort the players to not take into account the `amq_name` value
        # Sorted based on `rank` and, for those with the same rank, random (so different results can be provided given the same arguments)
        random.shuffle(player_list)
        players = sorted(player_list, key=lambda x: x.rank)
        
        best_teams = None
        min_diff = float('inf')
        num_players = len(players)
        team_size = num_players // num_teams
        current_teams = [[] for _ in range(num_teams)]
        team_sums = [0] * num_teams

        def backtrack(idx: int) -> None:
            nonlocal min_diff, best_teams
            
            # If we reached the end, we compare
            if idx == num_players:
                diff = max(team_sums) - min(team_sums)
                if diff < min_diff:
                    min_diff = diff
                    best_teams = [team[:] for team in current_teams]
                return

            player = players[idx]
            val = player.rank.value

            # We try to put the player in each team
            for i in range(num_teams):
                if len(current_teams[i]) < team_size:
                    # Prunning: if the current sum of this team minus the current minimum already exceeds min_diff, it's unlikely to improve
                    # but to be 100% optimal, we only prune if the "gap" is unsolvable.
                    current_teams[i].append(player)
                    team_sums[i] += val
                    
                    # Prunning: if the team was empty, we don't try to put the player in the next empty teams (avoids redundant permutations)
                    is_empty = len(current_teams[i]) == 1
                    
                    backtrack(idx + 1)
                    
                    # Undo
                    team_sums[i] -= val
                    current_teams[i].pop()
                    
                    if is_empty: 
                        break

        backtrack(0)
        return best_teams
        """
    

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
    def _teams_as_str(teams: list[list[Player]], show_team_value: bool = False) -> str:
        """Return a string representation for the `teams` rolled."""
        teams_as_str = ''

        for i, team in enumerate(teams):
            team_players = [f'{player.amq_name} ({player.rank.name})' for player in team]
            teams_as_str += f'**Group {i+1} ({len(team)}):** '
            teams_as_str += ', '.join(team_players)
            teams_as_str += '\n'

        if show_team_value:
            teams_as_str += '\n'

            for i, team in enumerate(teams):
                team_players = []
                team_rank = 0

                for player in team:
                    team_players.append(f'{player.amq_name} ({player.rank.value})')
                    team_rank += player.rank.value

                teams_as_str += f'**Group {i+1} (Total Rank: {team_rank}):** '
                teams_as_str += ', '.join(team_players)
                teams_as_str += '\n'

        return teams_as_str