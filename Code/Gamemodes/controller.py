from copy import copy

from Code.Gamemodes.enums import InfoType, Genres
from Code.Gamemodes.Sheet.controller import Sheet_Controller
from Code.Gamemodes.Gamemodes.controller import Gamemodes_Controller
from Code.Gamemodes.Gamemodes.gamemode import Gamemode
from Code.Gamemodes.Artists.controller import Artist_Controller
from Code.Gamemodes.Artists.og_artist import OG_Artist
from Code.Gamemodes.Artists.cq_artist import CQ_Artist
from Code.Gamemodes.SpecialLists.controller import SpecialList_Controller
from Code.Gamemodes.SpecialLists.og_specialList import OG_SpecialList
from Code.Gamemodes.SpecialLists.cq_specialList import CQ_SpecialList
from Code.Gamemodes.GlobalPlayers.controller import GlobalPlayer_Controller
from Code.Gamemodes.GlobalPlayers.global_players import GlobalPlayer

class Main_Controller:
    """Controller to encapsule the Players Logic from the rest of the application."""
    _instance = None
    def __new__(cls):
        """Override the __new__ method to return the existing instance of the class if it exists or create a new instance if it doesn't exist yet.\n"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._set_data()
        return cls._instance

    def _set_data(self) -> None:
        """
        Method that retrieves the Gamemodes from the database, sheets and yaml files the next info:\n
        - Gamemodes Descriptions
        - Metronomes
        - Items
        - Tags
        - OG_Artists
        - CQ_Artists
        - Special Lists
        - Global Players
        - Genres
        """
        gamemodes_descriptions, self.metronomes, self.items, self.tags, og_artists, cq_artists, og_special_lists, cq_special_lists = Sheet_Controller().get_sheet_data()
        
        self.gamemodes = Gamemodes_Controller(gamemodes_descriptions)

        self.artists = Artist_Controller(og_artists, cq_artists)
        self.special_lists = SpecialList_Controller(og_special_lists, cq_special_lists)

        all_global_players, active_global_players = Sheet_Controller().get_global_players()
        self.global_players = GlobalPlayer_Controller(all_global_players, active_global_players)

        self.genres = [genre.name.replace('_', ' ') for genre in Genres]


    def info(self, type: int) -> list[str]:
        """
        Return a list of strings with the information asked according to the type value.

        Raise:
        -----------
        - ValueError: If the type provided is not valid.
        """
        match type:
            case InfoType.GAMEMODES.value:
                return self.gamemodes.list_all_gamemodes()
            
            case InfoType.METRONOMES.value:
                return sorted(self.metronomes, key=str.lower)
            
            case InfoType.ITEMS.value:
                return sorted(self.items, key=str.lower)
            
            case InfoType.ARTISTS_OG.value:
                return self.artists.info_artists_OG()
            
            case InfoType.ARTISTS_CQ.value:
                return self.artists.info_artists_CQ()
            
            case InfoType.SPECIAL_LISTS_OG.value:
                return self.special_lists.info_special_lists_OG()
            
            case InfoType.SPECIAL_LISTS_CQ.value:
                return self.special_lists.info_special_lists_CQ()
            
            case InfoType.TAGS.value:
                return sorted(self.tags, key=str.lower)
            
            case InfoType.ALL_GLOBAL_PLAYERS.value:
                return self.global_players.info_all_global_players()
            
            case InfoType.ACTIVE_GLOBAL_PLAYERS.value:
                return self.global_players.info_active_global_players()
            
            case _:
                raise ValueError('Invalid type value!')


    def get_gamemode(self, gamemode_id_or_name: str) -> Gamemode | None:
        """
        Give a name or id of a Gamemode, return the `Gamemode` which has that id or name.\n
        In the name case, the closest match to the value provided is searched for.\n
        `None` can be returned if the id or a similar enough name couldn't be found in the Gamemodes's Catalogs.
        """
        return self.gamemodes.get_gamemode(gamemode_id_or_name)   

    def get_gamemodes(self) -> list[Gamemode]:
        """Return a list containing all the gamemodes."""
        return self.gamemodes.get_all_gamemodes()
    
    def get_artists_OG(self) -> list[OG_Artist]:
        """Return a list with all the artists stored (original version)."""
        return self.artists.get_artists_OG()
    
    def get_artists_CQ(self) -> list[CQ_Artist]:
        """Return a list with all the artists stored (community quiz version)."""
        return self.artists.get_artists_CQ()
    
    def get_special_lists_OG(self) -> list[OG_SpecialList]:
        """Return a list with all the special lists stored (original version)."""
        return self.special_lists.get_special_lists_OG()
    
    def get_special_lists_CQ(self) -> list[CQ_SpecialList]:
        """Return a list with all the special lists stored (community quiz version)."""
        return self.special_lists.get_special_lists_CQ()
    
    def get_all_global_players(self) -> list[GlobalPlayer]:
        """Return a list with all the global players stored."""
        return self.global_players.get_all_global_players()
    
    def get_active_global_players(self) -> list[GlobalPlayer]:
        """Return a list with all the active global players stored."""
        return self.global_players.get_active_global_players()
    
    def get_genres(self) -> list[str]:
        """Return a list with all the anime genres stored."""
        return copy(self.genres)
    
    def get_tags(self) -> list[str]:
        """Return a list with all the anime tags stored."""
        return copy(self.tags)
    
    def get_metronomes(self) -> list[str]:
        """Return a list with all the metronome powers stored."""
        return copy(self.metronomes)
    
    def get_items(self) -> list[str]:
        """Return a list with all the items stored."""
        return copy(self.items)


    def add_gamemode(
        self,
        gamemode_name: str,
        gamemode_size: int,
        gamemode_code: str,
        is_gamemode_watched: bool,
        is_random_dist_rollable: bool,
        is_weighted_dist_rollable: bool,
        is_equal_dist_rollable: bool
    ) -> tuple[bool, str]:
        """
        Create a gamemode with the provided data, storing it into the database and memory (through the gamemodes's catalogs).\n
        Return a tuple consisting of 2 values:
        - A boolean which is `True` if the gamemode could be stored, `False` otherwise, this is, a gamemode with that name already existed in memory.
        - A log str providing the gamemode's data.
        """
        return self.gamemodes.add_gamemode(
            gamemode_name=gamemode_name,
            gamemode_size=gamemode_size,
            gamemode_code=gamemode_code,
            is_watched=is_gamemode_watched,
            is_random_dist_rollable=is_random_dist_rollable,
            is_weighted_dist_rollable=is_weighted_dist_rollable,
            is_equal_dist_rollable=is_equal_dist_rollable
        )

    def delete_gamemode(self, gamemode: Gamemode) -> bool:
        """Delete the gamemode provided as argument. Return `True` if the gamemode was deleted successfully, `False` otherwise."""
        return self.gamemodes.delete_gamemode(gamemode)
    
    
    def get_gamemode_old_values(
        self,
        gamemode: Gamemode,
        new_name: str | None,
        new_code: str | None,
        new_random: bool | None,
        new_weighted: bool | None,
        new_equal: bool | None
    ) -> tuple[bool, str | None, str | None, bool | None, bool | None, bool | None]:
        """
        For each of the gamemode fields editable (those that has a parameter in this function), return `None` if a new value wasn't provided or if the new
        value is the same that the field currently contains. It return the old value of the field otherwise (this is, a change was made).\n
        It also return as the first tuple value a boolean that indicate whether there is an invalid combination of field values.
        """
        return self.gamemodes.get_gamemode_old_values(
            gamemode=gamemode,
            new_name=new_name,
            new_code=new_code,
            new_random=new_random,
            new_weighted=new_weighted,
            new_equal=new_equal
        )

    def edit_gamemode(
        self,
        gamemode_name: str,
        new_name: str | None,
        new_code: str | None,
        new_random_dist_rollable: bool | None,
        new_weighted_dist_rollable: bool | None,
        new_equal_dist_rollable: bool | None
    ) -> bool:
        """
        Edit the gamemode with name `gamemode_name`.
        If a `new_...` field is `None` it will be ignored, this is, it won't be modified.
        Return `True` if changes could be applied and `False` if an error was raised when applying the changes in the database.
        """
        return self.gamemodes.edit_gamemode(
            gamemode_name=gamemode_name,
            new_name=new_name,
            new_code=new_code,
            new_random=new_random_dist_rollable,
            new_weighted=new_weighted_dist_rollable,
            new_equal=new_equal_dist_rollable
        )