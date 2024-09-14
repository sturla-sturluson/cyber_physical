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
from .. import utils as UTILS


class MagneticSensor(IMagneticSensor):
    def __init__(self) -> None:
        print("Initializing Magnetic Sensor")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)
        self.translation_function = UTILS.get_translation_function()

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

        angle = UTILS.get_angle(sensor_cord, user_cord)

        return angle

    def get_x_y_z(self):
        """Returns the x,y,z values of the magnetic sensor"""
        x, y, z = self.mag.magnetic
        return x, y, z
    
    def get_orientation(self)->int:
        """
        Returns:
            int: 0-360        
        """
        x, y, _ = self.get_x_y_z()
        # Use the translation function to normalize the x and y values
        x, y = self.translation_function(x, y)
        # Get the orientation of the sensor
        return UTILS.calculate_orientation(x, y)
    
    def get_data(self)->tuple[int,tuple[int,int],str]:
        """Returns a tuple of (Angle,(X,Y),"NESW string")"""
        x, y, _ = self.get_x_y_z()
        # Use the translation function to normalize the x and y values
        x, y = self.translation_function(x, y)
        # Get the orientation of the sensor
        orientation = UTILS.calculate_orientation(x, y)
        return orientation, (x, y), self.get_NSEW_string(orientation)

    @classmethod
    def get_NSEW_string(cls,degrees:int)->str:
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
        return UTILS.get_NSEW_string(degrees)