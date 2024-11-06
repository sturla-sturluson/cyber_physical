from src.ps4_controller.ps4_basic import  BasePS4Listener
from src.motor import CarRunner
from src import OledDisplay
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
from src.utils import get_tape_color
import pygame
import os
import asyncio
import threading
import argparse
import time

MAX_SPEED_FLAG = "speed"
STOP_RANGE_FLAG = "range"




def oled_display_str(listener:BasePS4Listener)->str:
    l_rpm,r_rpm = listener.car_runner.motor_rpms
    ret_str = f"T {listener.target_speed} L: {l_rpm} R: {r_rpm}\n"
    # ret_str += f"Range: {round(listener.range_sensor.get_cm_distance())}\n"
    # ret_str += f"RGB: {listener.rgb_sensor._get_rgb()}\n"
    # tape_color = listener.rgb_sensor.tape_color
    # ret_str += f"Tape: {tape_color.name}\n"
    left_power = listener.car_runner.motor_powerlevels[0]
    right_power = listener.car_runner.motor_powerlevels[1]
    ret_str += f"L: {left_power} R: {right_power}\n"

    return ret_str

def display_text_thread(display:OledDisplay,listener:BasePS4Listener):
    while True:
        display.display_text(oled_display_str(listener))
        time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="Run the car app")
    parser.add_argument(f"-{MAX_SPEED_FLAG}", type=int, metavar='<0-100>', help=f"Set the max speed of the car (0-100)")
    parser.add_argument(f"-{STOP_RANGE_FLAG}", type=int, metavar='<cm>', help=f"Set the stop range of the car in cm")

    display = OledDisplay()

    args = parser.parse_args()
    # Defaults
    stop_range = -1 # in cm
    max_speed = 100
    if args.speed:
        max_speed =  args.speed
    if args.range:
        stop_range = args.range

    with CarRunner(False,stop_range=stop_range) as car_runner:
        
        listener = BasePS4Listener(car_runner)
        # Launch the start thread
        threading.Thread(target=listener.start).start() 
        # Launch the display thread
        threading.Thread(target=display_text_thread,args=(display,listener)).start()
        # Wait for the listener to finish
        while True:
            # os.system('clear')
            print(str(listener))
            time.sleep(0.25)
            

    


if __name__ == "__main__":
    main()