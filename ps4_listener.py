from src.ps4_controller import PS4Listener
from src.motor import CarRunner
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
import pygame
import os
import asyncio





def main():
    stop_range = 40 # in cm
    with CarRunner(
        stop_range=stop_range
        ) as car_runner:
        # asyncio.run(car_runner.run_car())
        listener = PS4Listener(car_runner)

    


if __name__ == "__main__":
    main()