from enum import Enum

class List_From_Options(Enum):
    """Enum class that represent the possible sites where the player's anime list is stored in."""
    Anilist = 0
    Kitsu = 1
    MyAnimeList = 2


class List_Sections_Options(Enum):
    """
    Enumerate class that represent the possible section combinations from the player's anime list.\n
    Naming:
    - W = Watching
    - C = Completed
    - H = Hold / Paused
    - D = Dropped
    """
    W_C = 0
    W_C_H = 1
    W_C_D = 2
    W_C_H_D = 3
    C = 4
    C_H = 5
    C_D = 6
    C_H_D = 7


class Prefered_Gamemode_Options(Enum):
    """Enum class that represent the possible most favourited/hated gamemode types (by size) that the player can select."""
    
    # It is NEEDED that the enum names are the same names as the player's properties: fav/hated gamemodes (case not sensitive).
    # Do NOT modify names (values are OK), or modify tha player's properties names (and all their references) accordingly.
    # NOTE This is referenced from Players interaction "player_change_mode", modify its content accordingly if applying changes here.
    
    Fav_1v1_Gamemode = 1
    Hated_1v1_Gamemode = 2
    Fav_2v2_Gamemode = 3
    Hated_2v2_Gamemode = 4
    Fav_4v4_Gamemode = 5
    Hated_4v4_Gamemode = 6