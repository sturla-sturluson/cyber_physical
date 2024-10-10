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


def drive_straight_range(motors:Motors,mag_sensor:MagneticSensor,range_sensor:RangeSensor,target_speed:int,target_heading:int):
    current_heading = mag_sensor.get_angle()
    off_course = is_off_course(current_heading,target_heading)
    if off_course:
        if current_heading < target_heading:
            motors.set_speed(target_speed,target_heading//2)
        elif current_heading > target_heading:
            motors.set_speed(target_speed,-target_heading//2)
    else:
        motors.set_speed(target_speed,0)
    os.system('clear')
    print(f"Current target heading: {target_heading}")
    print(f"Current heading: {current_heading}")
    print(f"Left Speed: {motors.motor_1.current_speed}")
    print(f"Right Speed: {motors.motor_2.current_speed}")

    
def run_car(motors:Motors):
    # Init pygame
    pygame.init()
    running = True
    fps = 15
    clock = pygame.time.Clock()

    # Init joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick : {joystick.get_name()}")


    
    ps_4_axis_dead_zone = 0.10
    l2_button = PS4Button("Axis",id=2,name="L2",released=-1,min=-1,max=1)
    r2_button = PS4Button("Axis",id=5,name="R2",released=-1,min=-1,max=1)
    left_joystick_x_axis = PS4Button("Axis",id=0,name="Left Stick X",released=0,min=-1,max=1)
    square_button = PS4Button("Button",id=3,name="Square",released=0)

    ps4_controller = PS4ControllerInput(r2_button,l2_button,left_joystick_x_axis,square_button,ps_4_axis_dead_zone)

    forward_motion,turning_motion = 0,0
    # Game loop


    # Auto drive part
    mag_sensor = MagneticSensor()
    range_sensor = RangeSensor()
    target_speed = 100
    target_heading = 0
    is_auto_drive = False

    while running:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # If we press triangle, we start auto drive
            if event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                is_auto_drive = True
                target_heading = mag_sensor.get_angle()
            if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                is_auto_drive = False
    
        # Going to fetch the status of the controller
        if is_auto_drive:
            drive_straight_range(motors,mag_sensor,range_sensor,target_speed,target_heading)
            continue


        os.system('clear')
        forward_motion,turning_motion = ps4_controller.get_values_from_game(joystick)
        motors.set_speed(forward_motion,turning_motion)
        print(f"Forward: {forward_motion} Turning: {turning_motion}")
        print(f"Left Speed: {motors.motor_1.current_speed}")
        print(f"Right Speed: {motors.motor_2.current_speed}")


