from enum import Enum,auto

class TurningLevel(Enum):
    SOFT = auto()
    MEDIUM = auto()
    HARD = auto()

class ButtonType(Enum):
    AXIS = auto()
    BUTTON = auto()
    HAT = auto()