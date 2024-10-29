from src.ps4_controller import PS4Listener
from src.motor import CarRunner,Motor
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN,A_C1_PIN,A_C2_PIN,B_C1_PIN,B_C2_PIN
import pygame
import os
import asyncio
import threading
import argparse
import time
import RPi.GPIO as GPIO
from src.constants import SLEEP_PIN

def _start_sleep():
    """Setting power to high to turn on the motor controller"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SLEEP_PIN, GPIO.OUT) 
    GPIO.output(SLEEP_PIN, GPIO.HIGH)

def main():

    speeds = [300]
    _start_sleep()

    with Motor(AIN1_PIN,AIN2_PIN,A_C1_PIN,A_C2_PIN) as motor:
        last_speed_update = time.time()
        # motor.start()
        motor.set_target_rpm(speeds.pop(0))
        while True:
            # os.system("clear")
            print(motor)
            time.sleep(0.5)
            if(time.time() - last_speed_update > 100):
                motor.set_target_rpm(speeds.pop(0))
                last_speed_update = time.time()


if __name__ == '__main__':
    main()