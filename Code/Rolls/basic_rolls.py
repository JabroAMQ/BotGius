import random
import datetime

from Code.Rolls import enums
from Code.Gamemodes.controller import Main_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode
from Code.Gamemodes.Artists.og_artist import OG_Artist
from Code.Gamemodes.Artists.cq_artist import CQ_Artist
from Code.Gamemodes.SpecialLists.og_specialList import OG_SpecialList
from Code.Gamemodes.SpecialLists.cq_specialList import CQ_SpecialList
from Code.Gamemodes.GlobalPlayers.global_players import GlobalPlayer

class Roll:
    """Static class that contains methods to produce all basic rolls."""

    @staticmethod
    def roll(type: enums.Rolls_Enum, as_str: bool = False) -> str | OG_Artist | CQ_Artist | OG_SpecialList | CQ_SpecialList | GlobalPlayer:
        """
        Roll some stuff (no gamemodes) based on the `type` value\n.
        Returns the roll itself if `as_str` = False or an string representation of the roll with some additional information if `as_str` = True.

        Example:
        --------
        - `type == ARTIST_OG` and `not as_str`:
            return the Artist object

        - `type == ARTIST_OG` and `as_str`:
            return repr(Artist)

        - `type == GENRE` and `not as_str`:
            return the Genre rolled (as a string, this is, "Action")

        - `type == GENRE` and `as_str`:
            return "**Genre rolled:** Action"
        """
        match type:

            case enums.Rolls_Enum.ARTIST_OG:
                roll = random.choice(Main_Controller().get_artists_OG())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.ARTIST_CQ:
                roll = random.choice(Main_Controller().get_artists_CQ())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.SPECIAL_LIST_OG:
                roll = random.choice(Main_Controller().get_special_lists_OG())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.SPECIAL_LIST_CQ:
                roll = random.choice(Main_Controller().get_special_lists_CQ())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.ALL_GLOBAL_PLAYER:
                roll = random.choice(Main_Controller().get_all_global_players())
                return repr(roll) if as_str else roll
            
            case enums.Rolls_Enum.ACTIVE_GLOBAL_PLAYER:
                roll = random.choice(Main_Controller().get_active_global_players())
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
            
            case enums.Rolls_Enum.SONG_SELECTION:
                selection_names = [selection.name for selection in enums.SongSelections]
                roll = random.choice(selection_names)
                if not as_str:
                    return roll
                # We additionally roll distribution if watched or mixed
                if roll in {enums.SongSelections.MIXED.name, enums.SongSelections.WATCHED.name}:
                    distribution_names = [distribution.name for distribution in enums.Distributions]
                    distribution_roll = random.choice(distribution_names)
                    return f'**Song selection rolled:** {roll.capitalize()} ({distribution_roll.capitalize()} distribution)'
                else:
                    return f'**Song selection rolled:** {roll.capitalize()}'

            
            case enums.Rolls_Enum.DISTRIBUTION:
                distribution_names = [distribution.name for distribution in enums.Distributions]
                roll = random.choice(distribution_names)
                return f'**Distribution rolled:** {roll.capitalize()}' if as_str else roll.capitalize()
            
            case enums.Rolls_Enum.TYPE_4:
                type_4_names = [type.name for type in enums.Type_4]
                roll = random.choice(type_4_names)
                return f'**Type 4 rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.TYPE_5:
                type_5_names = [type.name for type in enums.Type_5]
                roll = random.choice(type_5_names)
                return f'**Type 5 rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.TYPE_7:
                type_7_names = [type.name for type in enums.Type_7]
                roll = random.choice(type_7_names)
                return f'**Type 7 rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.MASTERY_MODE:
                mastery_mode_names = [mastery_mode.name.capitalize() for mastery_mode in enums.Mastery_Modes]
                roll = random.choice(mastery_mode_names)
                return f'**Mastery mode rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.DECADE:
                decades_names = [
                    decade.name.lstrip('_').replace('_', ' ').capitalize()
                    for decade in enums.Decades
                ]
                roll = random.choice(decades_names)
                return f'**Decade rolled:** {roll}' if as_str else roll
            
            case enums.Rolls_Enum.YEAR:
                first_year = 1968       # Previous years do not have enough songs to be rolled (20+); modify if needed
                last_year = datetime.datetime.now().year
                roll = random.randint(first_year, last_year)
                return f'**Year rolled:** {roll}' if as_str else roll

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

            case enums.Roll_Gamemode.ONLY_3V3:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 3]

            case enums.Roll_Gamemode.ONLY_4V4:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.size == 4]
                
            case enums.Roll_Gamemode.ONLY_WATCHED:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection]
            
            case enums.Roll_Gamemode.ONLY_WATCHED_1V1:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 1]

            case enums.Roll_Gamemode.ONLY_WATCHED_2V2:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 2]

            case enums.Roll_Gamemode.ONLY_WATCHED_3V3:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 3]

            case enums.Roll_Gamemode.ONLY_WATCHED_4V4:
                gamemodes = [gamemode for gamemode in gamemodes if gamemode.watched_song_selection and gamemode.size == 4]

            case enums.Roll_Gamemode.ONLY_RANDOM:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection]

            case enums.Roll_Gamemode.ONLY_RANDOM_1V1:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size == 1]

            case enums.Roll_Gamemode.ONLY_RANDOM_2V2:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size == 2]

            case enums.Roll_Gamemode.ONLY_RANDOM_3V3:
                gamemodes = [gamemode for gamemode in gamemodes if not gamemode.watched_song_selection and gamemode.size == 3]

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