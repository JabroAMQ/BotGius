from enum import Enum

class InfoType(Enum):
    """Enumerate class to represent the posible value types."""
    GAMEMODES = 0
    METRONOMES = 1
    ITEMS = 2
    ARTISTS_OG = 3
    ARTISTS_CQ = 4
    SPECIAL_LISTS_OG = 5
    SPECIAL_LISTS_CQ = 6
    TAGS = 7
    GLOBAL_PLAYERS = 8


class Genres(Enum):
    """
    Enumerate class to represent the possible genres that an anime can have.\n
    Hentai genre is not included.
    """
    Action = 0
    Adventure = 1
    Comedy = 2
    Drama = 3
    Ecchi = 4
    Fantasy = 5
    Horror = 6
    Mahou_Shoujo = 7
    Mecha = 8
    Music = 9
    Mystery = 10
    Psychological = 11
    Romance = 12
    Sci_Fi = 13
    Slice_of_Life = 14
    Sports = 15
    Supernatural = 16
    Thriller = 17