from . import Motors
import threading
import os
import asyncio
import datetime as dt
import math
from .. constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
from ..utils.common import clamp_speed
from ..sensors import RangeSensor
from ..display import OledDisplay

class CarRunner():
    FORWARD_MOTION:int
    TURNING_MOTION:int
    # This is the range that any forward motion will be set to 0
    STOP_RANGE:int = 40 # in cm
    STOP_FORWARD:bool = False
    RANGE_INTERVAL_CHECKER:dt.timedelta = dt.timedelta(milliseconds=500)
    last_stop_range_check = dt.datetime.now()
    display:OledDisplay|None = None
    last_display_time = dt.datetime.now()
    def __init__(self,stop_range:int|None = None,screen_on:bool = False,):
        self.motors = Motors()
        self.FORWARD_MOTION = 0
        self.TURNING_MOTION = 0
        if stop_range is not None:
            self.STOP_RANGE = stop_range
        self.range_sensor = RangeSensor()
        if screen_on:
            self.display = OledDisplay()    
        # Create a stop event and ui event
        self.stop_event = threading.Event()
        
    def motor_stop(self):
        """Stops the motors"""
        self.FORWARD_MOTION,self.TURNING_MOTION = 0,0
        self._update_speeds()

    def set_speed(self,forward_motion:int,turning_motion:int):
        """Sets the speeds of the car"""
        self.FORWARD_MOTION,self.TURNING_MOTION = forward_motion,turning_motion
        self._update_speeds()

    def cleanup(self):
        """Cleans up the motors"""
        self.motor_stop()
        self.motors.cleanup()
        self.stop_event.set()

    @property
    def motor_speeds(self)->tuple[int,int]:
        """Returns the forward motion of both motors"""
        return self.motors.left_motor.current_speed,self.motors.right_motor.current_speed
    
    def _update_display(self):
        """Updates the display"""
        if self.display is None:
            return
        if self.last_display_time > dt.datetime.now() - dt.timedelta(milliseconds=250):
            return
        self.display.clear()
        txt_str = f"Forward: {self.FORWARD_MOTION} Turning: {self.TURNING_MOTION}"
        m1_speed,m2_speed = self.motor_speeds
        txt_str += f"\nM1: {m1_speed} M2: {m2_speed}"
        self.display.display_text(txt_str)
        self.last_display_time = dt.datetime.now()

    def _range_stopper(self):
        """Returns boolean if we are within crash range"""
        crashing = self.range_sensor.get_cm_distance() < self.STOP_RANGE
        if(crashing):
            self.last_stop_range_check = dt.datetime.now()
            self.STOP_FORWARD = True
            return
        if(self.last_stop_range_check > dt.datetime.now() - self.RANGE_INTERVAL_CHECKER):
            self.STOP_FORWARD = False


    def _update_speeds(self):
        """Updates the speeds of the car"""
        self._range_stopper()
        if self.STOP_FORWARD:
            self.FORWARD_MOTION = min(self.FORWARD_MOTION,0)
        self.motors.set_speed(self.FORWARD_MOTION,self.TURNING_MOTION)
        self._update_display()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()



