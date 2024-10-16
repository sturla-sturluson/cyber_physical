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

def is_off_course(current_heading:int,target_heading:int, dead_zone:int = 5):
    """Returns True if the car is off course"""
    delta = abs(current_heading - target_heading) % 360
    if delta > 180:
        delta = 360 - delta
    return delta > dead_zone



class PS4Listener:
    ps_4_axis_dead_zone = 0.10
    fps = 10

    target_speed = 100
    target_heading = 0
    is_auto_drive = False

    # Turn on auto drive button
    auto_drive_button:PS4Button = PS4Button("Button",id=2,name="Triangle",released=0)
    #Brake button (also stops auto drive)
    brake_button:PS4Button = PS4Button("Button",id=3,name="Square",released=0)
    # Accelerate and decelerate
    accelerate_button:PS4Button = PS4Button("Axis",id=5,name="R2",released=-1,min=-1,max=1)
    decelerate_button:PS4Button = PS4Button("Axis",id=2,name="L2",released=-1,min=-1,max=1)
    # Left and right motion
    turn_button:PS4Button = PS4Button("Axis",id=0,name="Left Stick X",released=0,min=-1,max=1)

    # Current motions
    forward_motion,turning_motion = 0,0
    
    last_print = dt.datetime.now()
    
    range_sensor:IRangeSensor

    def __init__(self,car_runner:CarRunner):
        self.car_runner = car_runner
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
        self.ps4_input = PS4ControllerInput(
            accelerate_btn=self.accelerate_button,
            reverse_btn= self.decelerate_button,
            steer_btn=self.turn_button,
            brake_btn=self.brake_button,
            dead_zone=self.ps_4_axis_dead_zone
        )
        self.mag_sensor = MagneticSensor()
        self.range_sensor = RangeSensor()
        self._event_loop()
    
    def _event_loop(self):
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self._toggle_auto_drive(event)    # If we press triangle, we start auto drive
            self._auto_drive_handler()
            self._manual_control_handler()
            self._set_speed()
            self._print_status()
        
    def _manual_control_handler(self):
        """Handles manual control of the car"""
        if(self.is_auto_drive):
            return
        self.forward_motion,self.turning_motion = self.ps4_input.get_values_from_game(self.joystick)

    def _toggle_auto_drive(self,event:pygame.event.Event):
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

    def _print_status(self):
        """Prints the status of the motors"""
        if (dt.datetime.now() - self.last_print).seconds < 0.5:   # only print once a second
            return
        self.last_print = dt.datetime.now()
        os.system('clear')
        # Auto drive on or off
        status_str = f"Auto Drive: {self.is_auto_drive}\n"
        if self.is_auto_drive:         # If its on we also add the target heading
            status_str += f"Target Heading: {self.target_heading}\n"
        angle,x_y,nesw_string = self.mag_sensor.get_data()         # Current heading,and nesw string
        status_str += f"Current Heading: {angle}\n"
        status_str += f"Direction: {nesw_string}\n"
        status_str += f"Range Sensor: {self.range_sensor.get_cm_distance()}\n"         # The range sensor
        left_speed,right_speed = self.car_runner.motor_speeds         # Current speed 
        status_str += f"Left Speed: {left_speed}\n"
        status_str += f"Right Speed: {right_speed}\n"
        status_str += f"Controller Values: {self.forward_motion},{self.turning_motion}\n"         # Add the controller values
        print(status_str)

    def _set_speed(self):
        """Sets the speed of the car"""
        self.car_runner.set_speed(self.forward_motion,self.turning_motion)





