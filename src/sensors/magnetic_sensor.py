import board
from adafruit_lsm303dlh_mag import LSM303DLH_Mag
import busio
from ..interfaces import IMagneticSensor
from .. import utils as UTILS


class MagneticSensor(IMagneticSensor):
    def __init__(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)
        self.translation_function = UTILS.get_translation_function()

    def get_x_y_z(self):
        """Returns the x,y,z values of the magnetic sensor"""
        x, y, z = self.mag.magnetic
        return x, y, z
    
    def get_angle(self)->int:
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
        # Get the orientation in compass degrees
        orientation = UTILS.calculate_orientation(x, y)
        return orientation, (x, y), self.get_NSEW_string(orientation)
    
    def get_non_translate_data(self)->tuple[int,tuple[int,int],str]:
        """Returns a tuple of (Angle,(X,Y),"NESW string", unmodified x,y)"""
        x, y, _ = self.get_x_y_z()
        # Get the orientation in compass degrees
        orientation = UTILS.calculate_orientation(x, y)
        return orientation, (round(x), round(y)), self.get_NSEW_string(orientation)

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