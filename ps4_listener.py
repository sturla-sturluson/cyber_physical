from src.ps4_controller import PS4Listener
from src.motor import CarRunner
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
import pygame
import os
import asyncio
import argparse

MAX_SPEED_FLAG = "speed"
STOP_RANGE_FLAG = "range"


def main():
    parser = argparse.ArgumentParser(description="Run the car app")
    parser.add_argument(f"-{MAX_SPEED_FLAG}", type=int, metavar='<0-100>', help=f"Set the max speed of the car (0-100)")
    parser.add_argument(f"-{STOP_RANGE_FLAG}", type=int, metavar='<cm>', help=f"Set the stop range of the car in cm")
    args = parser.parse_args()
    # Defaults
    stop_range = 40 # in cm
    max_speed = 100
    if args.speed:
        max_speed =  args.speed
    if args.range:
        stop_range = args.range
    with CarRunner(
        stop_range=stop_range,
        max_speed=max_speed
        ) as car_runner:

        listener = PS4Listener(car_runner)

    


if __name__ == "__main__":
    main()