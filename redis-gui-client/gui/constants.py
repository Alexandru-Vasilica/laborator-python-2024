from enum import Enum

FONT = "Arial"

class KeyTypes(Enum):
    ALL = "All"
    STRING = "String"
    LIST = "List"
    SET = "Set"
    SORTED_SET = "Sorted Set"
    HASH = "Hash"

class Colors(Enum):
    BACKGROUND = "#18122B"
    FOREGROUND = "#393053"
    PRIMARY = "#443C68"
    LIGHT = "#635985"
    TEXT = "#F1F5F9"


class FontSizes(Enum):
    SMALL = 10
    MEDIUM = 12
    LARGE = 14
    EXTRA_LARGE = 16
