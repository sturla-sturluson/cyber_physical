import pygame
import os
from ..motor import Motors
from ..utils import clamp_speed,get_clamped_dead_zone
from .ps4_button import PS4Button
from .ps4_controller import PS4ControllerInput
from ..sensors import MagneticSensor,RangeSensor


def is_off_course(current_heading:int,target_heading:int, dead_zone:int = 5):
    """Returns True if the car is off course"""
    delta = abs(current_heading - target_heading) % 360
    if delta > 180:
        delta = 360 - delta
    return delta > dead_zone

def get_heading_difference(current_heading:int,target_heading:int):
    delta = abs(current_heading - target_heading) % 360
    if delta > 180:
        delta = 360 - delta
    return delta


class PS4Listener:
    ps_4_axis_dead_zone = 0.10
    fps = 15


    target_speed = 100
    target_heading = 0
    is_auto_drive = False

    # Turn on auto drive button
    auto_drive_button:PS4Button = PS4Button("Button",id=3,name="Triangle",released=0)
    #Brake button (also stops auto drive)
    brake_button:PS4Button = PS4Button("Button",id=1,name="Cross",released=0)
    # Accelerate and decelerate
    accelerate_button:PS4Button = PS4Button("Axis",id=5,name="R2",released=-1,min=-1,max=1)
    decelerate_button:PS4Button = PS4Button("Axis",id=2,name="L2",released=-1,min=-1,max=1)
    # Left and right motion
    left_motion:PS4Button = PS4Button("Axis",id=0,name="Left Stick X",released=0,min=-1,max=1)

    # Current motions
    forward_motion,turning_motion = 0,0
     

    def __init__(self,motors:Motors):
        self.motors = motors
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
            self.accelerate_button,
            self.decelerate_button,
            self.left_motion,
            self.brake_button,
            self.ps_4_axis_dead_zone
        )

        self.mag_sensor = MagneticSensor()
        self.range_sensor = RangeSensor()
    

    def _event_loop(self):
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # If we press triangle, we start auto drive
                self._toggle_auto_drive(event)

            self._auto_drive_handler()
            self._manual_control_handler()

            self._print_status()
        
    def _manual_control_handler(self):
        """Handles manual control of the car"""
        if(self.is_auto_drive):
            return
        # Get the controller values
        self.forward_motion,self.turning_motion = self.ps4_input.get_values_from_game(self.joystick)
        # Setting the speed of the motors
        self.motors.set_speed(self.forward_motion,self.turning_motion)


    def _toggle_auto_drive(self,event:pygame.event.Event):
        if(self.is_auto_drive):
            if event.type == pygame.JOYBUTTONDOWN and event.button in [self.auto_drive_button.id,self.brake_button.id]:
                self.is_auto_drive = False
        else:
            if event.type == pygame.JOYBUTTONDOWN and event.button == self.auto_drive_button:
                self.is_auto_drive = True
                self.target_heading = self.mag_sensor.get_angle()


    def _auto_drive_handler(self):
        """"""
        current_heading = self.mag_sensor.get_angle()
        # calculate how much off course we are 
        delta = get_heading_difference(current_heading,self.target_heading)
        # if its less than 2 degrees, we are on course
        off_course = delta > 2
        if off_course:
            # if we are off course, we adjust turning motion
            # Turning motion is a range from -100 to 100, max we ever turn is 15 
            turning_motion = self.target_heading - current_heading
            turning_motion = clamp_speed(turning_motion,-15,15)
            self.motors.set_speed(self.target_speed,turning_motion)


    def _print_status(self):
        """Prints the status of the motors"""
        os.system('clear')
        status_str = ""
        # Auto drive on or off
        status_str += f"Auto Drive: {self.is_auto_drive}\n"
        # If its on we also add the target heading
        if self.is_auto_drive:
            status_str += f"Target Heading: {self.target_heading}\n"
        # Current heading
        status_str += f"Current Heading: {self.mag_sensor.get_angle()}\n"
        # The range sensor
        status_str += f"Range Sensor: {self.range_sensor.get_cm_distance()}\n"
        # Current speed 
        status_str += f"Left Speed: {self.motors.motor_1.current_speed}\n"
        status_str += f"Right Speed: {self.motors.motor_2.current_speed}\n"
        # Add the controller values
        status_str += f"Controller Values: {self.forward_motion},{self.turning_motion}\n"
        print(status_str)





