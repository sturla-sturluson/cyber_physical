from src.ps4_controller.ps4_throttle import  PS4Listener
from src.motor import CarRunner
from src import OledDisplay
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
import pygame
import os
import asyncio
import threading
import argparse
import time

MAX_SPEED_FLAG = "speed"
STOP_RANGE_FLAG = "range"


def oled_display_str(listener:PS4Listener)->str:
    l_rpm,r_rpm = listener.car_runner.motor_rpms
    ret_str = f"T {listener.target_speed} L: {l_rpm} R: {r_rpm}\n"
    ret_str += f"Range: {round(listener.range_sensor.get_cm_distance())}\n"
    ret_str += f"F: {listener.forward_motion} T: {listener.turning_motion}\n"
    return ret_str

def display_text_thread(display:OledDisplay,listener:PS4Listener):
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
    stop_range = 40 # in cm
    max_speed = 100
    if args.speed:
        max_speed =  args.speed
    if args.range:
        stop_range = args.range

    Kp:float = 0.5 # Proportional, used to correct the error
    Ki:float = 0.01 # Integral, used to correct the error over time
    Kd:float = 0.1  # Derivative, used to predict the error


    with CarRunner(False,stop_range=stop_range) as car_runner:

        listener = PS4Listener(car_runner)
        # Launch the start thread
        threading.Thread(target=listener.start).start() 
        # Launch the display thread
        threading.Thread(target=display_text_thread,args=(display,listener)).start()
        # Wait for the listener to finish
        while True:
            print("================================")
            print(str(listener))
            time.sleep(0.5)
            

    


if __name__ == "__main__":
    main()