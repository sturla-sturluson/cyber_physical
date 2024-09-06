import board
from adafruit_lsm303dlh_mag import LSM303DLH_Mag
import busio
import math
import numpy as np
import time

class MagneticSensor:
    OFFSET = {
        "x": -41,
        "y": -11,
        "z": 0
    }
    def __init__(self) -> None:
        print("Initializing Magnetic Sensor")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)
        print("Magnetic Sensor Initialized")



    def _get_micro_teslas(self):
        x, y, z = self.mag.magnetic 
        x -= self.OFFSET["x"]
        y -= self.OFFSET["y"]   
        z -= self.OFFSET["z"]
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

    def get_orientation_in_degrees(self):
        """
        
        Returns:
            int: 0-360        
        """
        x_values = np.array([])
        y_values = np.array([])
        z_values = np.array([])
        for i in range(100):
            x , y, z = self._get_micro_teslas()
            x_values = np.append(x_values,x)
            y_values = np.append(y_values,y)
            z_values = np.append(z_values,z)
            time.sleep(0.001)
        avg_x = np.mean(x_values)
        avg_y = np.mean(y_values)
        return self._calculate_orientation(avg_x, avg_y)
    
    def get_full_data(self):
        x_values = np.array([])
        y_values = np.array([])
        x_max = 0
        x_min = 0
        y_max = 0
        y_min = 0
        for i in range(100):
            x , y, z = self._get_micro_teslas()
            x_values = np.append(x_values,x)
            y_values = np.append(y_values,y)
            time.sleep(0.001)
        x_max = np.max(x_values)
        x_min = np.min(x_values)
        y_max = np.max(y_values)
        y_min = np.min(y_values)
        x_avg = np.mean(x_values)
        y_avg = np.mean(y_values)
        return {
            "deg": self._calculate_orientation(x_avg, y_avg),
            "x_max": x_max, 
            "x_min": x_min,
            "y_max": y_max,
            "y_min": y_min,
            "x_avg": x_avg,
            "y_avg": y_avg,
        }

    @classmethod
    def get_orientation_string(cls,degrees:int):
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