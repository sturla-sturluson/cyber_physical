from ..constants import CALIBRATION_FILE_PATH
from .. import utils as UTILS
from ..models import Cords
import json
import numpy as np

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
            
def _generate_translation_matrix(angle:float)->np.ndarray:
    cos_a = np.cos(np.radians(angle))
    sin_a = np.sin(np.radians(angle))
    return np.array([[cos_a,-sin_a],[sin_a,cos_a]])


def get_translation_matrix()->np.ndarray:
    max_cords,min_cords,north_cords = _load_configs()
    # Get the midpoints
    x_midpoint, y_midpoint = UTILS.get_midpoints(max_cords, min_cords)
    # Now we get the north cord requested by the user
    sensor_north = Cords(x_midpoint, max_cords.y)
    # Get the angle between the sensor north and the north cords
    angle = UTILS.get_angle(sensor_north,north_cords)
    # Get the translation matrix
    

def _get_configs(self):
        """Loads the calibration file"""
        data = {}
        try:
            # Check if the calibration file exists
            Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True) 
            # Check if the file exists
            file_path = Path(CONFIG_DIR).expanduser() / FILE_NAME
            
            with open(file_path, "r") as f:
                data = json.load(f)
                # Format json to a dictionary

                data = dict(data)

                # Check if the calibration file is valid
                print(data)
                # for key in DEFAULT_CALIBRATION.keys():
                #     data = data.get(key)
                #     _is_valid_cords(data)
                self._set_configs(data)

        except FileNotFoundError:
            print("Calibration file not found, using default values")
            file_path = Path(CONFIG_DIR).expanduser() / FILE_NAME
            print(f"FilePath: {file_path}")
            print(f"File Exists: {file_path.exists()}")
            # LS of the directory
            print(f"Directory Contents: {list(Path(CONFIG_DIR).iterdir())}")
            data = DEFAULT_CALIBRATION
            self._set_configs(data)
        except ValueError as e:
            print(e)
            print("Using default calibration values")
            data = DEFAULT_CALIBRATION
            self._set_configs(data)

    def _get_converted_data(self,data:list):
        """Converts the list of strings to a list of floats"""
        return [float(x) for x in data]

    def _set_configs(self,data:dict[str,list[int|float]]):
        """Saves the calibration data"""

        max_cords = Cords(*data["max"])
        min_cords = Cords(*data["min"])
        x_midpoint, y_midpoint = UTILS.get_midpoints(max_cords, min_cords)
        sensor_north = Cords(x_midpoint, max_cords.y)
        sensor_east = Cords(max_cords.x, y_midpoint)
        sensor_south = Cords(x_midpoint, min_cords.y)
        sensor_west = Cords(min_cords.x, y_midpoint)
        # Check if all the angles are close enough to 90 degrees
        north_angle = self._get_rotation(sensor_north,Cords(*data["north"]))
        east_angle = self._get_rotation(sensor_east,Cords(*data["east"]))
        south_angle = self._get_rotation(sensor_south,Cords(*data["south"]))
        west_angle = self._get_rotation(sensor_west,Cords(*data["west"]))
        print(f"North angle: {north_angle}")
        print(f"East angle: {east_angle}")
        print(f"South angle: {south_angle}")
        print(f"West angle: {west_angle}")

        # Setting all the data
        self.MAX_CORDS = max_cords
        self.MIN_CORDS = min_cords
        self.NORTH = Cords(*data["north"])
        self.EAST = Cords(*data["east"])
        self.SOUTH = Cords(*data["south"])
        self.WEST = Cords(*data["west"])
        self.OFFSET_ANGLE = north_angle