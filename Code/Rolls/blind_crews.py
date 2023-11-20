import random
from copy import copy

from Code.Rolls import enums
from Code.Rolls.basic_rolls import Roll
from Code.Matches.match import Match
from Code.Players.player import Player

class Blind_Crews:
    """Class that contains the methods to roll a blind crews round given two teams."""
    def __init__(self, type : enums.Roll_Gamemode, team_1 : list[Player], team_2 : list[Player]) -> None:
        """Class constructor"""
        self.type = type
        self.team_1 = team_1
        self.team_2 = team_2
        
        self.matches : list[Match] = []             # List of rolled matches
        self.special_rolls_list : list[str] = []    # All the additional rolls for special modes (artistmania, random tag, etc.)


    def roll_blind_crews(self) -> None:
        """Roll a blind crews round given the parameter values stablished in the object constructor."""
        # Create a copy of the teams so that we can roll another round later
        team_1, team_2 = copy(self.team_1), copy(self.team_2)

        # Reset the matches
        # TODO Store the matches anywhere else before deleting the info?
        self.matches.clear()
        self.special_rolls_list.clear()

        # Roll a new set of matches
        while len(team_1) and len(team_2):
            self._roll_match(team_1, team_2)


    def _roll_match(self, team_1 : list[Player], team_2 : list[Player]) -> Match:
        """
        Creates a Match:
        - 1. Roll a gamemode with the constraints `self.type` stablished in the class constructor.
        - 2. Roll players from both teams (`team_1` and `team_2`) to play the gamemode selected.
        - 3. Creates and return the `match` given the gamemode and players rolled.

        NOTE: `team_1` and `team_2` are the list of players NOT YET SELECTED to play a gamemode.\n
        NOTE: `team_1` and `team_2` lists are modified inside this method (players selected are removed from the lists).
        """
        # 1. Roll the Gamemode
        gamemode = Roll.roll_gamemode(self.type)

        # Make sure that there are at least enough players in team_1 and team_2
        # NOTE In case not, roll any 1v1 gamemode
        # TODO Is it possible to improve this?
        if gamemode.size > len(team_1) or gamemode.size > len(team_2):
            gamemode = Roll.roll_gamemode(enums.Roll_Gamemode.ONLY_1V1)

        # 2. Roll the Players from both teams
        selected_team_1, selected_team_2 = [[] for _ in range(2)]
        for _ in range(gamemode.size):
            
            # Team 1
            player_team_1 = random.choice(team_1)
            selected_team_1.append(player_team_1)
            team_1.remove(player_team_1)            # Remove the player from the list to prevent them from being rolled again

            # Team 2
            player_team_2 = random.choice(team_2)
            selected_team_2.append(player_team_2)
            team_2.remove(player_team_2)            # Remove the player from the list to prevent them from being rolled again

        # 3. Create the match
        new_match = Match(gamemode, selected_team_1, selected_team_2)

        # 4. Additional roll if a special gamemode was rolled
        additional_roll = new_match.special_gamemode_additional_roll()
        if additional_roll is not None:
            self.special_rolls_list.append(additional_roll)

        # 5. Add the match to the matches list
        self.matches.append(new_match)

    
    def get_round_information(self) -> str:
        """Given the stored set of matches, return a string with the public information about the round rolled."""
        content = ''

        for match in self.matches:
            # 1. Add the gamemode
            content += f'**Gamemode selected:** {match.gamemode.name}\n'
            
            # 2. Roll a valid gamemode distribution
            content += f'{match.gamemode.roll_distribution()}\n'
            
            # 3. Add team_1 players
            team_1_names = [player.amq_name for player in match.team_1]
            team_1_names = ' '.join(team_1_names)
            content += f'**Team 1:** {team_1_names}\n'
            
            # 4. Add team_2 players 
            team_2_names = [player.amq_name for player in match.team_2]
            team_2_names = ' '.join(team_2_names)
            content += f'**Team 2:** {team_2_names}\n\n'

        return content
    

    def get_results_template(self) -> str:
        """Given the stored set of matches, return a string with the results template to send to the host's dms."""
        content = ''

        for i, match in enumerate(self.matches):
            # 1. Get gamemode name
            gamemode_name = match.gamemode.name

            # 2. Get team 1 players names
            team_1_names = [player.amq_name for player in match.team_1]
            team_1_names = ' '.join(team_1_names)

            # 3. Get team 2 players names
            team_2_names = [player.amq_name for player in match.team_2]
            team_2_names = ' '.join(team_2_names)

            # 4. Add the data to content
            content += f'**{i+1}) {gamemode_name}:** {team_1_names} VS {team_2_names} --> \n'

        content = f'```{content}```'
        return content