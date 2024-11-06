from src.motor import CarRunner, Motors
from src.sensors import RgbSensor
from src.utils import get_tape_color
from src.enums import TapeColor,TurningLevel
from src import OledDisplay
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
import pygame
import os
import asyncio
import threading
import argparse
import time
import csv

def _calibrate_loop(current_color:TapeColor,color_list:list,rgbsensor:RgbSensor,number_of_samples:int):
    input("Hit enter to calibrate " + current_color.name)
    old_color = (-1,-1,-1)
    while True:
        new_color = rgbsensor.get_rgb()
        if(new_color != old_color):
            color_list.append(new_color)
            old_color = new_color
            print(f"{len(color_list)}/{number_of_samples}")
        time.sleep(0.10)
        if(len(color_list) == number_of_samples):
            break
        
def _save_to_csv(color_list:list,color:TapeColor):
    filename = f"{color.name}.csv"

    with open("data/color_cal/" + filename, mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for c in color_list:
            writer.writerow(c)
    print(f"Saved {filename}")

def main():
    black_list = []
    blue_list = []
    red_list = []
    table_list = []
    other_list = []
    rgbsensor = RgbSensor()
    # Take samples for 5 seconds or 100 samples
    number_of_samples = 100

    _calibrate_loop(TapeColor.BLACK,black_list,rgbsensor,number_of_samples)
    _calibrate_loop(TapeColor.BLUE,blue_list,rgbsensor,number_of_samples)
    _calibrate_loop(TapeColor.RED,red_list,rgbsensor,number_of_samples)

    _save_to_csv(black_list,TapeColor.BLACK)
    _save_to_csv(blue_list,TapeColor.BLUE)
    _save_to_csv(red_list,TapeColor.RED)


if __name__ == '__main__':
    main()