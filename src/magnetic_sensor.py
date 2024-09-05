import board
from adafruit_lsm303dlh_mag import LSM303DLH_Mag
import busio
import math

class MagneticSensor:
    def __init__(self) -> None:
        print("Initializing Magnetic Sensor")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)
        print("Magnetic Sensor Initialized")



    def _get_micro_teslas(self):
        x, y, z = self.mag.magnetic 
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
        x, y, z = self._get_micro_teslas()
        return self._calculate_orientation(x, y)