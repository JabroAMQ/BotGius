from Code.Rolls.basic_rolls import Roll
from Code.Rolls.enums import Rolls_Enum
from Code.Players.player import Player
from Code.Gamemodes.Gamemodes.gamemode import Gamemode
from Code.Gamemodes.Artists.cq_artist import CQ_Artist
from Code.Gamemodes.SpecialLists.cq_specialList import CQ_SpecialList
from Code.Gamemodes.GlobalPlayers.global_players import GlobalPlayer

class Match:
    """Class to represent a match. Formed by a gamemode and 2 list of players (team 1, team 2)."""
    def __init__(self, gamemode: Gamemode, team_1: list[Player], team_2: list[Player]) -> None:
        """Class constructor."""
        self.gamemode = gamemode
        self.team_1 = team_1
        self.team_2 = team_2
        self.distribution = self._roll_distribution()
        self.special_roll = None

    
    def _roll_distribution(self) -> str | None:
        """
        Return a string with the gamemode distribution like: "(Distribution: {distribution})".\n
        If the gamemode's song selection is random, we return None instead.
        """
        if not self.gamemode.watched_song_selection:
            return None
        return self.gamemode.roll_distribution() 


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
            artist: CQ_Artist = Roll.roll(Rolls_Enum.ARTIST_CQ)
            self.special_roll = f'Artist: {artist.artist_name} (quiz ID: {artist.community_quiz_id})'
            return content + repr(artist)
        
        # Special List
        elif 'special list' in self.gamemode.name.lower():
            special_list: CQ_SpecialList = Roll.roll(Rolls_Enum.SPECIAL_LIST_CQ)
            self.special_roll = f'Special list: {special_list.special_list_name} (quiz ID: {special_list.community_quiz_id})'
            return content + repr(special_list)
        
        # Global Player
        elif 'global player' in self.gamemode.name.lower() and not 'picked' in self.gamemode.name.lower():
            global_player: GlobalPlayer = Roll.roll(Rolls_Enum.ACTIVE_GLOBAL_PLAYER)
            self.special_roll = f'Player: {global_player.player_name} (list: {global_player.list_name} ({global_player.list_from}))'
            return content + repr(global_player)

        # Random Genre
        elif 'genre' in self.gamemode.name.lower() and not 'picked' in self.gamemode.name.lower():
            genre: str = Roll.roll(Rolls_Enum.GENRE)
            self.special_roll = f'Genre: {genre}'
            return content + f'**Genre rolled:** {genre}'

        # Random Tag
        elif 'tag' in self.gamemode.name.lower() and not 'picked' in self.gamemode.name.lower():
            tag: str = Roll.roll(Rolls_Enum.TAG)
            self.special_roll = f'Tag: {tag}'
            return content + f'**Tag rolled:** {tag}'
        
        # Mastery Modes
        # NOTE we do not add roll for watched mastery modes
        elif 'mastery' in self.gamemode.name.lower() and not 'watched' in self.gamemode.name.lower():
            mastery_mode: str = Roll.roll(Rolls_Enum.MASTERY_MODE)
            self.special_roll = f'Mastery mode: {mastery_mode}'
            return content + f'**Mastery mode rolled:** {mastery_mode}'
        
        # Type 5 (OP/ED/IN/OPED/OPEDIN)
        elif 'countdown' in self.gamemode.name.lower() or 'ftf' in self.gamemode.name.lower():
            type_5: str = Roll.roll(Rolls_Enum.TYPE_5)
            self.special_roll = f'Type 5: {type_5}'
            return content + f'**Type 5 rolled:** {type_5}'

        # Random Metronome
        # NOTE not adding self.special_roll for metronomes on purpose
        # self.special_roll is basically extra info for the host that is particularly useful in crews_duel. For these cases, knowing the metronome beforehand makes no sense
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