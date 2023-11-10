from Code.Rolls.basic_rolls import Roll
from Code.Rolls.enums import Rolls_Enum
from Code.Players.player import Player
from Code.Gamemodes.Gamemodes.gamemode import Gamemode

class Match:
    """Class to represent a match. Formed by a gamemode and 2 list of players (team 1, team 2)."""
    def __init__(self, gamemode : Gamemode, team_1 : list[Player], team_2 : list[Player]) -> None:
        """Class constructor."""
        self.gamemode = gamemode
        self.team_1 = team_1
        self.team_2 = team_2

        # TODO Add new attributes (elo purposes)
        # - Match Status (PLAYING, FINISHED, etc.)
        # - Match Result (TEAM_1, TEAM_2, DRAW)
        # - The special roll (artist, tag, etc.) rolled?

    
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
            return content + Roll.roll(Rolls_Enum.ARTIST, as_str=True)
        
        # Special List
        elif 'special list' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.SPECIAL_LIST, as_str=True)
        
        # Global Player
        elif 'global player list' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.GLOBAL_PLAYER, as_str=True)

        # Random Genre
        elif 'random genre' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.GENRE, as_str=True)

        # Random Tag
        elif 'random tag' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.TAG, as_str=True)

        # Random Metronome
        elif 'metronome' in self.gamemode.name.lower():
            return content + Roll.roll(Rolls_Enum.METRONOME, as_str=True)


        # If the gamemode isn't special, we return None
        return None