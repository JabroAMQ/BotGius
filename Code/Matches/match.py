from Code.Rolls.basic_rolls import Roll
from Code.Rolls.enums import Rolls_Enum
from Code.Players.player import Player
from Code.Gamemodes.Gamemodes.gamemode import Gamemode

class Match:
    """Class to represent a match. Formed by a gamemode and 2 list of players (team 1, team 2)."""
    def __init__(self, gamemode: Gamemode, team_1: list[Player], team_2: list[Player]) -> None:
        """Class constructor."""
        self.gamemode = gamemode
        self.team_1 = team_1
        self.team_2 = team_2
        self.special_roll = None    # TODO

    
    def special_gamemode_additional_roll(self) -> str | None:
        """
        For those special gamemodes that requires an additional roll (Artistmania, random tag, etc.), apply that roll.\n
        Return a string representation of the additional roll, or `None` if no additional roll is required for the gamemode.
        """
        team_1_playes = ', '.join([player.amq_name for player in self.team_1])
        team_2_players = ', '.join([player.amq_name for player in self.team_2])

        content = f'**Match for gamemode {self.gamemode.name}** between:\n'
        content += f'**Team 1:** {team_1_playes}\n'
        content += f'**Team 2:** {team_2_players}\n\n'

        # NOTE obtaining which gamemodes are the special ones by their names
        # Not using their ids for flexibility (for instance, a new Artistmania mode is added or a database with different gamemodes ids is used)
        #
        # NOTE hardcoding the mode names, might be interesing to create an enum class instead.

        # Artistmania
        if 'artistmania' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.ARTIST_OG, as_str=True)
        
        # Special List
        elif 'special list' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.SPECIAL_LIST_OG, as_str=True)
        
        # Global Player
        elif 'global player list' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.ACTIVE_GLOBAL_PLAYER, as_str=True)

        # Random Genre
        elif 'random genre' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.GENRE, as_str=True)

        # Random Tag
        elif 'random tag' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.TAG, as_str=True)
        
        # Mastery Modes
        # NOTE we do not add roll for watched mastery modes
        elif 'mastery' in self.gamemode.name.lower() and not 'watched' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.MASTERY_MODE, as_str=True)
        
        # Type 5 (OP/ED/IN/OPED/OPEDIN)
        elif 'countdown' in self.gamemode.name.lower() or 'ftf' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.TYPE_5, as_str=True)

        # Random Metronome
        elif 'metronome' in self.gamemode.name.lower():
            # Rolling 1 different metronome per player
            metronomes = ''
            # Team 1
            for player in self.team_1:
                metronomes += f'**Metronome for {player.amq_name} ->** {Roll.roll(Rolls_Enum.METRONOME, as_str=False)}\n'
            # Team 2
            for player in self.team_2:
                metronomes += f'**Metronome for {player.amq_name} ->** {Roll.roll(Rolls_Enum.METRONOME, as_str=False)}\n'
            return content + metronomes


        # If the gamemode isn't special, we return None
        return None