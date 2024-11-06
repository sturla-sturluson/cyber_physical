from enum import Enum,auto

class TurningLevel(Enum):
    SOFT = auto()
    MEDIUM = auto()
    HARD = auto()

class ButtonType(Enum):
    AXIS = auto()
    BUTTON = auto()
    HAT = auto()

class TapeColor(Enum):
    RED = auto()
    BLACK = auto()
    BLUE = auto()
    TABLE = auto()
    OTHER = auto()