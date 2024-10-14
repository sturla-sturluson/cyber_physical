from typing import Protocol

class IMagneticSensor(Protocol):
    def get_x_y_z(self) -> tuple[float,float,float]:
        ...
    def get_angle(self) -> int:
        ...
    @classmethod
    def get_NSEW_string(cls,degrees:int) -> str:
        ...
    def get_data(self)->tuple[int,tuple[int,int],str]:
        """Returns a tuple of (Angle,(X,Y),"NESW string")"""
        ...

class IRangeSensor(Protocol):
    def get_voltage(self) -> float:
        """Returns the voltage of the sensor"""
        return 1
    
    def get_raw_value(self) -> int:
        """Returns the raw value of the sensor
            Which is a int from 0 to 65535
        """
        return 1
    
    def get_cm_distance(self)->float:
        """Returns the distance in cm"""
        return 150
                        
    def get_data(self) -> tuple[int,float,float]:
        """Returns the raw value and the voltage, and estimated distance in cm.
        Returns:
            tuple[int,float]: (raw value, voltage, distance in cm)
        """
        return 1,1,1
