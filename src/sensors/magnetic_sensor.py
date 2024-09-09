import board
from adafruit_lsm303dlh_mag import LSM303DLH_Mag
import busio
import math
import numpy as np
import time
from ..interfaces import IMagneticSensor
import json
from ..models import Cords
from pathlib import Path

CONFIG_DIR = "~/.config/cyber_physical_systems"
FILE_NAME = "compass_calibration.json"

DEFAULT_CALIBRATION = {
    "max": [90.0,90.0],
    "min": [-90.0,-90.0],
    "north": [0.0,90.0],
    "east": [90.0,0.0],
    "south": [0.0,-90.0],
    "west": [-90.0,0.0],
}

def _is_valid_cords(cords:tuple[int|float,int|float]):
    x_cord, y_cord = cords
    x_cord = float(x_cord)
    y_cord = float(y_cord)
    if x_cord < -90 or x_cord > 90:
        raise ValueError("X cord must be between -90 and 90")
    if y_cord < -90 or y_cord > 90:
        raise ValueError("Y cord must be between -90 and 90")   


def _get_dot_product(cord1:Cords,cord2:Cords):
    x1 = cord1.x
    y1 = cord1.y
    x2 = cord2.x
    y2 = cord2.y
    return x1*x2 + y1*y2

def _get_angle(dot_product:int|float,cord1:Cords,cord2:Cords):
    magnitude1 = cord1.get_magnitude()
    magnitude2 = cord2.get_magnitude()
    theta = dot_product / (magnitude1 * magnitude2)
    degrees = math.degrees(math.acos(theta))
    return degrees

def _get_midpoints(max_cords:Cords,min_cords:Cords):
    """Returns the midpoints of the max and min cords"""
    x_midpoint = (max_cords.x + min_cords.x) / 2
    y_midpoint = (max_cords.y + min_cords.y) / 2
    return x_midpoint, y_midpoint

class MagneticSensor(IMagneticSensor):
    MAX_CORDS = Cords(*DEFAULT_CALIBRATION["max"])
    MIN_CORDS = Cords(*DEFAULT_CALIBRATION["min"])
    NORTH = Cords(*DEFAULT_CALIBRATION["north"])
    EAST = Cords(*DEFAULT_CALIBRATION["east"])
    SOUTH = Cords(*DEFAULT_CALIBRATION["south"])
    WEST = Cords(*DEFAULT_CALIBRATION["west"])

    OFFSET_ANGLE = 0 # Degrees we need to rotate from the sensor's output to match the user's perceived directions




    def __init__(self) -> None:
        print("Initializing Magnetic Sensor")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)
        self.calibration_data = self._get_configs()

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
        x_midpoint, y_midpoint = _get_midpoints(max_cords, min_cords)
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


    def _get_rotation(self, sensor_cord:Cords, user_cord:Cords):
        """To correct the sensor's output to match the perceived directions, we apply a rotation matrix"""
        # x_max = 71.63
        # y_max = 59.54
        # x_min = -52.72
        # y_min = -75.09
        # x_midpoint = 9.455
        # y_midpoint = -7.775
        # North is then (9.455, 59.54)
        # User north is (33.6,-9,91)
        # We use the rotation matrix to rotate the sensor's output to match the user's perceived directions

        dot_product = _get_dot_product(sensor_cord, user_cord)

        angle = _get_angle(dot_product, sensor_cord, user_cord)

        return angle

    def _get_micro_teslas(self):
        x, y, z = self.mag.magnetic 
        return x, y, z
    
    def get_x_y_z(self):
        """Returns the x,y,z values of the magnetic sensor"""
        x, y, z = self._get_micro_teslas()
        return x, y, z
    
    def get_raw_x_y_z(self):
        """Returns the x,y,z values of the magnetic sensor"""
        x, y, z = self._get_micro_teslas()
        return x, y, z

    def _calculate_orientation(self, x, y):
        if x == 0:
            return 90 if y > 0 else 270
        angle = int(math.degrees(math.atan(y / x)))
        if x < 0:
            angle += 180
        elif y < 0:
            angle += 360
        return angle

    def get_orientation(self):
        """
        Returns:
            int: 0-360        
        """
        x, y, z = self._get_micro_teslas()
        # Normalize the x and y to the range of -90 to 90, using the min and max values
        x = (x - self.MIN_CORDS.x) / (self.MAX_CORDS.x - self.MIN_CORDS.x) * 180 - 90
        y = (y - self.MIN_CORDS.y) / (self.MAX_CORDS.y - self.MIN_CORDS.y) * 180 - 90
        orientation = self._calculate_orientation(x, y)
        # Apply the offset angle
        orientation += self.OFFSET_ANGLE
        if orientation > 360:
            orientation -= 360
        if orientation < 0:
            orientation += 360
        return int(orientation)


    @classmethod
    def get_NSEW_string(cls,degrees:int):
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