from . import Motors
import threading
import os
import asyncio
import datetime as dt
import math
from .. constants import MAX_POWERLEVEL as C_MAX_SPEED
from ..utils.common import clamp_speed
from ..sensors import RangeSensor
from ..enums import TurningLevel
import time

class CarRunner():
    FORWARD_MOTION:int
    TURNING_MOTION:int
    # This is the range that any forward motion will be set to 0
    STOP_RANGE:int = 40 # in cm
    STOP_FORWARD:bool = False
    MAX_SPEED:int

    SAMPLES_PER_SECOND:int = 10
    tsample:float = 1/SAMPLES_PER_SECOND
    # If we detected a "crash" we make sure that we keep the car stopped for a while

    last_stop_range_check = dt.datetime.now()
    stop_timer = dt.timedelta(milliseconds=500)


    def __init__(self,stop_range:int|None = None,max_speed:int = C_MAX_SPEED):
        self.motors = Motors(max_speed)
        self.MAX_SPEED = max_speed
        self.FORWARD_MOTION = 0
        self.TURNING_MOTION = 0
        if stop_range is not None:
            self.STOP_RANGE = stop_range
        self.range_sensor = RangeSensor() 
        # Create a stop event and ui event
        self._stop_event = threading.Event()
        self._update_thread = threading.Thread(target=self._listener)
        self._update_thread.start()

    def _listener(self):
        while not self._stop_event.is_set():
            time.sleep(self.tsample)
            self._range_stopper()

    def set_max_powerlevel(self,max_speed:int)->None:
        """Updates the speed ceiling"""
        self.MAX_SPEED = max(max_speed,10) # Min speed is still 10
        self.motors.set_max_powerlevel(max_speed)

    def set_turning_level(self,turning_level:TurningLevel):
        """Sets the turning level of the car"""
        self.motors.set_turning_level(turning_level)
        
    def motor_stop(self):
        """Stops the motors"""
        self.FORWARD_MOTION,self.TURNING_MOTION = 0,0
        self._update_speeds()

    def set_speed(self,forward_motion:int,turning_motion:int) -> int:
        """Sets the speeds of the car, returns the max RPM currently"""
        self.FORWARD_MOTION,self.TURNING_MOTION = forward_motion,turning_motion
        self._update_speeds()
        return self.motors.MAX_RPM

    def cleanup(self):
        """Cleans up the motors"""
        self.motor_stop()
        self.motors.cleanup()
        self._stop_event.set()

    @property
    def motor_powerlevels(self)->tuple[int,int]:
        """Returns the forward motion of both motors"""
        return self.motors.left_motor.current_power,self.motors.right_motor.current_power
    
    @property
    def motor_rpms(self)->tuple[int,int]:
        """Returns the forward motion of both motors"""
        return self.motors.left_motor.rpm,self.motors.right_motor.rpm
        
    def _range_stopper(self):
        """Returns boolean if we are within crash range"""
        crashing = self.range_sensor.get_cm_distance() < self.STOP_RANGE
        if(crashing):
            self.last_stop_range_check = dt.datetime.now()
            self.STOP_FORWARD = True
            return
        # If we are not crashing, we check if we should stop
        time_diff = dt.datetime.now() - self.last_stop_range_check
        if(time_diff < self.stop_timer):
            self.STOP_FORWARD = False

    def _update_speeds(self):
        """Updates the speeds of the car"""
        if self.STOP_FORWARD:
            self.FORWARD_MOTION = min(self.FORWARD_MOTION,0)
        self.motors.set_speed(self.FORWARD_MOTION,self.TURNING_MOTION)

    def __str__(self) -> str:
        ret_str = "Car Runner\n"
        ret_str += f"Forward Motion: {self.FORWARD_MOTION} Turning Motion: {self.TURNING_MOTION}\n"
        ret_str += str(self.motors)
        return ret_str

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()



