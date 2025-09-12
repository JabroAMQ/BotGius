from enum import Enum

class SongSelections(Enum):
    """Enumerate class to represent the possible song selections that an AMQ game can have."""
    RANDOM = 0
    MIXED = 1
    WATCHED = 2


class Distributions(Enum):
    """Enumerate class to represent the possible watched song distributions that an AMQ game can have."""
    RANDOM = 0
    WEIGHTED = 1
    EQUAL = 2


class Type_4(Enum):
    """Enumerate class to represent the 4 possible song type combinations possible that an AMQ game can have."""
    OPED = 0
    OPIN = 1
    EDIN = 2
    OPEDIN = 3


class Type_5(Enum):
    """Enumerate class to represent 5 song types that an AMQ game can have (OP/ED/IN/OPED/OPEDIN)."""
    OP = 0
    ED = 1
    IN = 2
    OPED = 3
    OPEDIN = 4


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


class One_Life_Challenge(Enum):
    """Enumerate class to represent the different one life challenge modes."""
    _5S = 0
    _5S_START_SAMPLE = 1
    _6S_END_SAMPLE = 2
    _6S_2X = 3
    _6S_4X = 4


class Uma_Musume(Enum):
    """Enumerate class to represent the different Uma Musume types?"""
    SPRINT = 0
    MILE = 1
    MEDIUM = 2
    LONG = 3


class Rolls_Enum(Enum):
    """Enumerate class to represent the different rollable stuff possible."""
    ARTIST_OG = 0
    ARTIST_CQ = 1
    SPECIAL_LIST_OG = 2
    SPECIAL_LIST_CQ = 3
    ALL_GLOBAL_PLAYER = 4
    ACTIVE_GLOBAL_PLAYER = 5
    GENRE = 6
    TAG = 7
    METRONOME = 8
    ITEM = 9
    SONG_SELECTION = 10
    DISTRIBUTION = 11
    TYPE_4 = 12
    TYPE_5 = 13
    TYPE_7 = 14
    MASTERY_MODE = 15
    YEAR = 16
    ONE_LIFE_CHALLENGE = 17
    UMA_MUSUME = 18


class Roll_Gamemode(Enum):
    """Enumerate class to represent the different rollable gamemodes types possible."""
    ALL_GAMEMODES = 0
    ONLY_1V1 = 1
    ONLY_2V2 = 2
    ONLY_3V3 = 3
    ONLY_4V4 = 4
    ONLY_WATCHED = 5
    ONLY_RANDOM = 6
    ONLY_WATCHED_1V1 = 7
    ONLY_WATCHED_2V2 = 8
    ONLY_WATCHED_3V3 = 9
    ONLY_WATCHED_4V4 = 10
    ONLY_RANDOM_1V1 = 11
    ONLY_RANDOM_2V2 = 12
    ONLY_RANDOM_3V3 = 13
    ONLY_RANDOM_4V4 = 14
    ONLY_TEAMS_MODES = 15
    ONLY_WATCHED_TEAMS_MODES = 16
    ONLY_RANDOM_TEAMS_MODES = 17


class Roll_Teams(Enum):
    """Enumerate class to represent the different rollable teams/groups types possible."""
    FULL_RANDOM = 0
    BALANCED = 1
    GROUPED_BY_STRENGTH = 2