from enum import Enum

FONT = "Arial"


class KeyTypes(Enum):
    """
    Enum for the different types of keys in Redis and their corresponding names
    """
    ALL = "All"
    STRING = "String"
    LIST = "List"
    SET = "Set"
    SORTED_SET = "Sorted Set"
    HASH = "Hash"


class Colors(Enum):
    """
    Enum for the different colors used in the GUI
    """
    BACKGROUND = "#18122B"
    FOREGROUND = "#393053"
    PRIMARY = "#443C68"
    LIGHT = "#635985"
    TEXT = "#F1F5F9"
    TEXT_SECONDARY = "#E1D7B7"


class FontSizes(Enum):
    """
    Enum for the different font sizes used in the GUI
    """
    SMALL = 10
    MEDIUM = 12
    LARGE = 14
    EXTRA_LARGE = 16
    TITLE = 30
    SUBTITLE = 22
