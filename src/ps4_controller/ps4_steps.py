import pygame
import os
from ..motor import CarRunner
from ..utils import clamp_speed,get_clamped_dead_zone,get_heading_difference
from .ps4_button import PS4Button
from .ps4_controller import PS4ControllerInput
from ..sensors import MagneticSensor,RangeSensor
import datetime as dt
import time
from ..interfaces import IRangeSensor
from ..enums import TurningLevel,ButtonType

def is_off_course(current_heading:int,target_heading:int, dead_zone:int = 5):
    """Returns True if the car is off course"""
    delta = abs(current_heading - target_heading) % 360
    if delta > 180:
        delta = 360 - delta
    return delta > dead_zone



class PS4Listener:
    ps_4_axis_dead_zone = 0.10
    fps = 10

    target_speed:int
    target_heading = 0
    is_auto_drive = False
    is_drive = False
    is_stopped = False

    # Turn on auto drive button
    auto_drive_button:PS4Button = PS4Button(ButtonType.BUTTON,id=2,name="Triangle",released=0)
    #Brake button (also stops auto drive)
    brake_button:PS4Button = PS4Button(ButtonType.BUTTON,id=3,name="Square",released=0)
    # Accelerate and decelerate
    accelerate_button:PS4Button = PS4Button(ButtonType.BUTTON,id=5,name="R1",released=0)
    decelerate_button:PS4Button = PS4Button(ButtonType.BUTTON,id=4,name="L1",released=0)
    # Left and right motion
    turn_button:PS4Button = PS4Button(ButtonType.AXIS,id=0,name="Left Stick X",released=0,min=-1,max=1)

    toggle_drive_button:PS4Button = PS4Button(ButtonType.BUTTON,id=0,name="Cross",released=0)

    turning_level_button:PS4Button = PS4Button(ButtonType.BUTTON,id=1,name="Circle",released=0)
    # Current motions
    forward_motion,turning_motion = 0,0
    range_sensor:IRangeSensor

    TURNING_LEVELS = [TurningLevel.SOFT,TurningLevel.MEDIUM,TurningLevel.HARD]
    turning_level_index = 1

    def __init__(self,car_runner:CarRunner):
        self.car_runner = car_runner
        self.target_speed = 0

        # Init pygame
        pygame.init()
        self.running = True

        self.clock = pygame.time.Clock()

        # Init joystick
        self.joystick = pygame.joystick.Joystick(0)
        # If no joystick is found, we exit
        if self.joystick is None:
            print("No joystick found")
            raise ValueError("No joystick found")
        self.joystick.init()
        print(f"Joystick : {self.joystick.get_name()}")
        # All the buttons for manual control
        self.ps4_input = PS4ControllerInput(self.joystick,dead_zone=self.ps_4_axis_dead_zone)
        self.mag_sensor = MagneticSensor()
        self.range_sensor = RangeSensor()

    def start(self):
        """Starts the event loop"""
        self._event_loop()
    
    def _event_loop(self):
        while self.running:
            self.clock.tick(self.fps)
            self.is_stopped = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # If we press triangle, we start auto drive
                self._listen_stop(event)
                if(self.is_stopped):
                    break
                self._listen_toggle_auto_drive(event)    
                # If we press circle, we change the turning level
                self._listen_change_turning_level(event)

                self._listen_toggle_drive(event)

                self._listen_speed_change(event)

            if not self.is_stopped:
                self._auto_drive_handler()
                self._turning_values_fetcher()
            self._set_speed()

    def _listen_speed_change(self,event:pygame.event.Event):
        """Listens for speed changes"""
        if(event.type == pygame.JOYBUTTONDOWN and event.button == self.accelerate_button.id):
            self.target_speed += 10
        elif(event.type == pygame.JOYBUTTONDOWN and event.button == self.decelerate_button.id):
            self.target_speed -= 10

    def _listen_stop(self,event:pygame.event.Event):
        """Stops the car"""
        if(event.type == pygame.JOYBUTTONDOWN and event.button == self.brake_button.id):
            self.is_auto_drive = False
            self.forward_motion = 0
            self.turning_motion = 0
            self.is_stopped = True        

    def _listen_toggle_drive(self,event:pygame.event.Event):
        """Toggles the drive on and off"""
        if(event.type == pygame.JOYBUTTONDOWN and event.button == self.toggle_drive_button.id):
            self.is_drive = not self.is_drive
      
    def _turning_values_fetcher(self):
        """Handles manual control of the car"""
        if(self.is_auto_drive):
            return
        self.ps4_input.set_value(self.turn_button)
        self.turning_motion = self.turn_button.get_normalized_value(-100,100)

    def _listen_change_turning_level(self,event:pygame.event.Event):
        if(event.type == pygame.JOYBUTTONDOWN and event.button == self.turning_level_button.id):
            self.turning_level_index = (self.turning_level_index + 1) % len(self.TURNING_LEVELS)
            self.car_runner.set_turning_level(self.TURNING_LEVELS[self.turning_level_index])

    def _listen_toggle_auto_drive(self,event:pygame.event.Event):
        """Toggles auto drive on and off"""
        if(self.is_auto_drive 
           and  event.type == pygame.JOYBUTTONDOWN 
           and event.button in [self.auto_drive_button.id,self.brake_button.id]):
                self.is_auto_drive = False
        elif event.type == pygame.JOYBUTTONDOWN and event.button == self.auto_drive_button.id:
                self.is_auto_drive = True
                self.target_heading = self.mag_sensor.get_angle()

    def _auto_drive_handler(self):
        """Handles the auto drive"""
        current_heading = self.mag_sensor.get_angle()         # calculate how much off course we are 
        delta = get_heading_difference(current_heading,self.target_heading)         
        turning_motion = 0 
        if delta > 1:   # if we are off course, we adjust turning motion
            # Turning motion is a range from -100 to 100, max we ever turn is 15 
            turning_motion = clamp_speed(self.target_heading - current_heading,-15,15)
        self.forward_motion,self.turning_motion = self.target_speed,turning_motion

    def _get_turn_level_to_string(self):
        """Returns the turning level as a string"""
        return str(self.TURNING_LEVELS[self.turning_level_index])

    def _set_speed(self):
        """Sets the speed of the car"""
        max_rpm = self.car_runner.set_speed(self.forward_motion,self.turning_motion)
        self.target_speed = clamp_speed(self.target_speed,-max_rpm,max_rpm)

    def __str__(self):
        status_str = f"Auto Drive: {self.is_auto_drive}\n"
        status_str += f"Turning Level: {self._get_turn_level_to_string()}\n"
        status_str += f"Max Speed: {self.target_speed}\n"
        if self.is_auto_drive:         # If its on we also add the target heading
            status_str += f"Target Heading: {self.target_heading}\n"
        angle,x_y,nesw_string = self.mag_sensor.get_data()         # Current heading,and nesw string
        status_str += f"Current Heading: {angle}\n"
        status_str += f"Direction: {nesw_string}\n"
        status_str += f"Range Sensor: {self.range_sensor.get_cm_distance()}\n"         # The range sensor
        status_str += f"Controller Values: {self.forward_motion},{self.turning_motion}\n"         # Add the controller values
        status_str += str(self.car_runner)
        return status_str





