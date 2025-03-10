from enum import Enum

class Distributions(Enum):
    """Enumerate class to represent the possible watched song distributions that an AMQ game can have."""
    Random = 0
    Weighted = 1
    Equal = 2


class Type_4(Enum):
    """Enumerate class to represent the 4 possible song type combinations possible that an AMQ game can have."""
    OPED = 0
    OPIN = 1
    EDIN = 2
    OPEDIN = 3


class Type_7(Enum):
    """Enumerate class to represent the 7 song type possibilities that an AMQ game can have."""
    OP = 0
    ED = 1
    IN = 2
    OPED = 3
    OPIN = 4
    EDIN = 5
    OPEDIN = 6


class Mastery_Modes(Enum):
    """Enumerate class to represent the 5 mastery modes options."""
    NOVICE = 0
    INTERMEDIATE = 1
    EXPERT = 2
    ALIEN = 3
    FULL = 4


class Rolls_Enum(Enum):
    """Enumerate class to represent the different rollable stuff possible."""
    ARTIST_OG = 0
    ARTIST_CQ = 1
    SPECIAL_LIST_OG = 2
    SPECIAL_LIST_CQ = 3
    GLOBAL_PLAYER = 4
    GENRE = 5
    TAG = 6
    METRONOME = 7
    ITEM = 8
    DISTRIBUTION = 9
    TYPE_4 = 10
    TYPE_7 = 11
    MASTERY_MODE = 12


class Roll_Gamemode(Enum):
    """Enumerate class to represent the different rollable gamemodes types possible."""
    ALL_GAMEMODES = 0
    ONLY_1V1 = 1
    ONLY_2V2 = 2
    ONLY_4V4 = 3
    ONLY_WATCHED = 4
    ONLY_RANDOM = 5
    ONLY_WATCHED_1V1 = 6
    ONLY_WATCHED_2V2 = 7
    ONLY_WATCHED_4V4 = 8
    ONLY_RANDOM_1V1 = 9
    ONLY_RANDOM_2V2 = 10
    ONLY_RANDOM_4V4 = 11
    ONLY_TEAMS_MODES = 12
    ONLY_WATCHED_TEAMS_MODES = 13
    ONLY_RANDOM_TEAMS_MODES = 14


class Roll_Teams(Enum):
    """Enumerate class to represent the different rollable teams/groups types possible."""
    FULL_RANDOM = 0
    BALANCED = 1
    GROUPED_BY_STRENGTH = 2