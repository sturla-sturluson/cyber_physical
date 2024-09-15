from ..constants import CALIBRATION_FILE_PATH
from .. import utils as UTILS
from ..models import Cords
import json
import numpy as np
from typing import Callable

DEFAULT_CALIBRATION = {
    "max": [90.0,90.0],
    "min": [-90.0,-90.0],
    "north": [0.0,90.0],
}

MAX_CORDS = Cords(*DEFAULT_CALIBRATION["max"])
MIN_CORDS = Cords(*DEFAULT_CALIBRATION["min"])
NORTH = Cords(*DEFAULT_CALIBRATION["north"])
_DEFAULT_CALIBRATION = (MAX_CORDS,MIN_CORDS,NORTH)

def _get_cords(data:list[float])->Cords:
    x_cord = float(data[0])
    y_cord = float(data[1])
    if(x_cord < -90.0 or x_cord > 90.0 or y_cord < -90.0 or y_cord > 90.0):
        raise ValueError("Invalid Cords")
    return Cords(x_cord,y_cord)


def _load_configs():
    try:
        # Check if the calibration file exists            
        with open(CALIBRATION_FILE_PATH, "r") as f:
            data = json.load(f)
            # Format json to a dictionary
            data = dict(data)
            max_cords = _get_cords(data["max"])
            min_cords = _get_cords(data["min"])
            north_cords = _get_cords(data["north"])
            return max_cords,min_cords,north_cords


    except FileNotFoundError:
        print("Calibration file not found, using default values")
        return _DEFAULT_CALIBRATION

    except ValueError as e:
        print(e)
        print("Using default calibration values")
        return _DEFAULT_CALIBRATION
            
def _generate_translation_matrix(min_cords:Cords,max_cords:Cords)->np.ndarray:
    """Generates a matrix that normalizes the cordinates from the calibration data
    Max = (71,50) # X,Y
    Min = (-35,-45) 
    Midpoint = (18,2.5)
    (71,50) -> (90,90)
    (-35,50) -> (-90,90)
    (18,2.5) -> (0,0)
    """
    x_midpoint, y_midpoint = UTILS.get_midpoints(max_cords, min_cords)
    translation_matrix = np.array([
        [1, 0, -x_midpoint],
        [0, 1, -y_midpoint],
        [0, 0, 1]
    ])
    scale_x = 180 / (max_cords.x - min_cords.x)
    scale_y = 180 / (max_cords.y - min_cords.y)
    scale_matrix = np.array([
        [scale_x, 0, 0],
        [0, scale_y, 0],
        [0, 0, 1]
    ])
    # @ is the matrix multiplication operator
    return scale_matrix @ translation_matrix


def _generate_rotation_matrix(angle:int)->np.ndarray:
    cos_a = np.cos(np.radians(angle))
    sin_a = np.sin(np.radians(angle))
    return np.array([[cos_a,-sin_a],[sin_a,cos_a]])


def get_translation_function()->Callable[[int|float,int|float],tuple[int,int]]:
    """Returns a function that translates the cordinates from the calibration data
    You then plug in the x,y from the magnetometer and it will return the translated cordinates   
    
    """
    max_cords,min_cords,north_cords = _load_configs()
    translation_matrix = _generate_translation_matrix(min_cords,max_cords)
    x_midpoint, _ = UTILS.get_midpoints(max_cords, min_cords)
    # Getting the angle from sensor north cords, and where the user wants north to be
    sensor_north = Cords(x_midpoint, max_cords.y)
    angle = UTILS.get_angle(north_cords,sensor_north)
    rotation_matrix = _generate_rotation_matrix((int(angle)))

    def translate(x:int|float,y:int|float)->tuple[int,int]:
        """Translates the cordinates from the calibration data"""
        # Clamping the cords to the max and min cords, to ensure no fuckery happens
        x = max(min(x, int(max_cords.x)), int(min_cords.x))
        y = max(min(y, int(max_cords.y)), int(min_cords.y))
        cords = np.array([x,y,1])
        translated_cords = translation_matrix @ cords
        rotated_cords = rotation_matrix @ translated_cords[:2]
        return (int(rotated_cords[0]),int(rotated_cords[1]) )
    
    return translate


def get_NSEW_string(degrees:int):
    """Takes in the degrees and returns the lettering for what direction it is
    338°-22° -> N
    23°-67° -> NE
    68°-112° -> E
    113°-157° -> SE
    158°-202° -> S
    203°-247° -> SW
    248°-292° -> W
    293°-337° -> NW
    """      

    if degrees >= 338 or degrees <= 22:
        return "N"
    elif degrees >= 23 and degrees <= 67:
        return "NE"
    elif degrees >= 68 and degrees <= 112:
        return "E"
    elif degrees >= 113 and degrees <= 157:
        return "SE"
    elif degrees >= 158 and degrees <= 202:
        return "S"
    elif degrees >= 203 and degrees <= 247:
        return "SW"
    elif degrees >= 248 and degrees <= 292:
        return "W"
    elif degrees >= 293 and degrees <= 337:
        return "NW"
    else:
        return "N/A"