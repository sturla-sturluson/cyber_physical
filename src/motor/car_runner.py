from . import Motor,Motors
import threading
import os
import asyncio
import datetime as dt
import math
from . import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
from .common import clamp_speed


class CarRunner():
    FORWARD_MOTION:int
    TURNING_MOTION:int

    def __init__(self,motor_1_pins:tuple[int,int],motor_2_pins:tuple[int,int]):
        self.motors = Motors(motor_1_pins,motor_2_pins)
        self.FORWARD_MOTION = 0
        self.TURNING_MOTION = 0
        # Create a stop event and ui event
        self.stop_event = threading.Event()
        

    def shut_down(self):
        """Shuts down the car"""
        self.motor_stop()
        self.stop_event.set()
        self.cleanup()
    
    def motor_stop(self):
        """Stops the motors"""
        self.motors.motor_stop()    

    def set_speeds(self,forward_motion:int,turning_motion:int):
        """Sets the speeds of the car"""
        self.FORWARD_MOTION = clamp_speed(forward_motion)
        self.TURNING_MOTION = clamp_speed(turning_motion)


    def cleanup(self):
        """Cleans up the motors"""
        self.motors.cleanup()

    async def motor_loop(self):
        # start the display loop
        # Launch both motor loops in separate threads
        await self._display_thread()

    async def _display_thread(self):
        last_display_time = dt.datetime.now()
        # Only refresh terminal every 0.5 seconds
        while not self.stop_event.is_set():
            if (dt.datetime.now() - last_display_time).total_seconds() > 0.5:
                self._print_screen()
                last_display_time = dt.datetime.now()
            self._update_speeds()
            await asyncio.sleep(0.1)   
            

    def _update_speeds(self):
        """Updates the speeds of the car by updating the Motors"""
        self.motors.set_speed(self.FORWARD_MOTION,self.TURNING_MOTION)


    def _print_screen(self):
        """Prints the screen"""
        os.system('clear')
        # Print the current time
        print(dt.datetime.now().strftime("%H:%M:%S"))
        motors_string = str(self.motors).split("\n")
        print(motors_string[0])
        print(motors_string[1])

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()


