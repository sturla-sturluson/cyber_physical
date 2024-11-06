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

def _calibrate_loop(current_color:TapeColor,color_list:list,rgbsensor:RgbSensor,number_of_samples:int,time_interval:float):
    print("Hit enter to calibrate " + current_color.name)
    while True:
        color_list.append(rgbsensor.get_rgb())
        time.sleep(time_interval)
        if(len(color_list) == number_of_samples):
            break
def _save_to_csv(color_list:list,color:TapeColor):
    filename = f"{color.name}.csv"

    with open(filename, mode='w') as file:
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
    time_interval = 5/number_of_samples

    _calibrate_loop(TapeColor.BLACK,black_list,rgbsensor,number_of_samples,time_interval)
    _calibrate_loop(TapeColor.BLUE,blue_list,rgbsensor,number_of_samples,time_interval)
    _calibrate_loop(TapeColor.RED,red_list,rgbsensor,number_of_samples,time_interval)
    _calibrate_loop(TapeColor.TABLE,table_list,rgbsensor,number_of_samples,time_interval)
    _calibrate_loop(TapeColor.OTHER,other_list,rgbsensor,number_of_samples,time_interval)

    _save_to_csv(black_list,TapeColor.BLACK)
    _save_to_csv(blue_list,TapeColor.BLUE)
    _save_to_csv(red_list,TapeColor.RED)
    _save_to_csv(table_list,TapeColor.TABLE)
    _save_to_csv(other_list,TapeColor.OTHER)


if __name__ == '__main__':
    main()