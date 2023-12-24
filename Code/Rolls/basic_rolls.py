import random

from Code.Rolls import enums
from Code.Gamemodes.controller import Main_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode
from Code.Gamemodes.Artists.artist import Artist
from Code.Gamemodes.SpecialLists.specialList import SpecialList
from Code.Gamemodes.GlobalPlayers.global_players import GlobalPlayer

class Roll:
    """Static class that contains methods to produce all basic rolls."""

    @staticmethod
    def roll(type: enums.Rolls_Enum, as_str: bool = False) -> str | Artist | SpecialList | GlobalPlayer:
        """
        Roll some stuff (no gamemodes) based on the `type` value\n.
        Returns the roll itself if `as_str` = False or an string representation of the roll with some additional information if `as_str` = True.

        Example:
        --------
        - `type == ARTIST` and `not as_str`:
            return the Artist object

        - `type == ARTIST` and `as_str`:
            return repr(Artist)

        - `type == GENRE` and `not as_str`:
            return the Genre rolled (as a string, this is, "Action")

        - `type == GENRE` and `as_str`:
            return "**Genre rolled:** Action"
        """
        match type:

            case enums.Rolls_Enum.ARTIST:
                roll = random.choice(Main_Controller().get_artists())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.SPECIAL_LIST:
                roll = random.choice(Main_Controller().get_special_lists())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.GLOBAL_PLAYER:
                roll = random.choice(Main_Controller().get_global_players())
                return repr(roll) if as_str else roll

            case enums.Rolls_Enum.GENRE:
                roll = random.choice(Main_Controller().get_genres())
                return f'**Genre rolled:** {roll}' if as_str else roll

            case enums.Rolls_Enum.TAG:
                roll = random.choice(Main_Controller().get_tags())
                return f'**Tag rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.METRONOME:
                roll = random.choice(Main_Controller().get_metronomes())
                return f'**Metronome rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.ITEM:
                roll = random.choice(Main_Controller().get_items())
                return f'**Item rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.DISTRIBUTION:
                distribution_names = [distribution.name for distribution in enums.Distributions]
                roll = random.choice(distribution_names)
                return f'**Distribution rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.TYPE_4:
                type_4_names = [type.name for type in enums.Type_4]
                roll = random.choice(type_4_names)
                return f'**Type 4 rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.TYPE_7:
                type_7_names = [type.name for type in enums.Type_7]
                roll = random.choice(type_7_names)
                return f'**Type 7 rolled:** {roll}' if as_str else roll
            
            case _:
                raise ValueError('Invalied "type" value')


    @staticmethod
    def roll_gamemode(type: enums.Roll_Gamemode = enums.Roll_Gamemode.ALL_GAMEMODES) -> Gamemode:
        """Roll a gamemode."""
        gamemodes = Main_Controller().get_gamemodes()

        match type:

            case enums.Roll_Gamemode.ALL_GAMEMODES:
                gamemodes = gamemodes

            case enums.Roll_Gamemode.ONLY_1V1:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 1]

            case enums.Roll_Gamemode.ONLY_2V2:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 2]

            case enums.Roll_Gamemode.ONLY_4V4:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 4]
                
            case enums.Roll_Gamemode.ONLY_WATCHED:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection]
            
            case enums.Roll_Gamemode.ONLY_WATCHED_1V1:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 1]

            case enums.Roll_Gamemode.ONLY_WATCHED_2V2:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 2]

            case enums.Roll_Gamemode.ONLY_WATCHED_4V4:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 4]

            case enums.Roll_Gamemode.ONLY_RANDOM:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection]

            case enums.Roll_Gamemode.ONLY_RANDOM_1V1:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size == 1]

            case enums.Roll_Gamemode.ONLY_RANDOM_2V2:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size == 2]

            case enums.Roll_Gamemode.ONLY_RANDOM_4V4:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size == 4]

            case enums.Roll_Gamemode.ONLY_TEAMS_MODES:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.size > 1]

            case enums.Roll_Gamemode.ONLY_WATCHED_TEAMS_MODES:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size > 1]

            case enums.Roll_Gamemode.ONLY_RANDOM_TEAMS_MODES:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size > 1]

            case _:
                raise ValueError('Invalied "type" value')
            
        return random.choice(gamemodes)