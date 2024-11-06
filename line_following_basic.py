from src.motor import CarRunner, Motors
from src.sensors import RgbSensor
from src.utils import get_tape_color,get_closest_color,get_current_time_string
from src.enums import TapeColor,TurningLevel
from src import OledDisplay
from src.constants import AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
import pygame
import os
import asyncio
import threading
import argparse
import time
from queue import Queue

# def oled_display_str(motors:Motors,rgb_sensor:RgbSensor)->str:
#     ret_str = ""
#     # ret_str += f"Range: {round(listener.range_sensor.get_cm_distance())}\n"
#     rgb = rgb_sensor.get_rgb()
#     ret_str += f"RGB: {rgb}\n"
#     tape_color = get_tape_color(rgb)
#     closest_color = get_closest_color(rgb)
#     ret_str += f"Tape: {tape_color.name}\n"
#     ret_str += f"Closest: {closest_color.name}\n"
#     left_power = motors.left_motor.current_power
#     right_power = motors.right_motor.current_power
#     ret_str += f"L: {left_power} R: {right_power}\n"

#     return ret_str

# def display_text_thread(display:OledDisplay,motors:Motors,rgb_sensor:RgbSensor):
#     while True:
#         display.display_text(oled_display_str(motors,rgb_sensor))
#         time.sleep(0.5)

def get_most_common_tape_color(color_map:dict)->TapeColor:
    curr_max = 0
    max_tape_color = TapeColor.OTHER
    blue_color = color_map[TapeColor.BLUE]
    red_color = color_map[TapeColor.RED]
    black_color = color_map[TapeColor.BLACK]
    other_color = color_map[TapeColor.OTHER]
    table_color = color_map[TapeColor.TABLE]
    if(blue_color > curr_max):
        curr_max = blue_color
        max_color = TapeColor.BLUE
    if(red_color > curr_max):
        curr_max = red_color
        max_color = TapeColor.RED
    if(black_color > curr_max):
        curr_max = black_color
        max_color = TapeColor.BLACK
    if(table_color > curr_max):
        curr_max = table_color
        max_color = TapeColor.TABLE
    if(other_color > curr_max):
        curr_max = other_color
        max_color = TapeColor.OTHER

    return max_color


def main():
    display = OledDisplay()
    rgb_sensor = RgbSensor()  
    display_thread:threading.Thread 

    MAX_SPEED = 40

    SAFE_SPEED = 15

    SPEED_STEP = 0.999

    UPDATES_PER_SEC = 60
    TIME_INTERVAL = 1/UPDATES_PER_SEC

    try:
        with Motors(False) as motors: 
            # display_thread = threading.Thread(target=display_text_thread,args=(display,motors,rgb_sensor))
            
            motors.set_turning_level(TurningLevel.MEDIUM)



            ahead_speed = MAX_SPEED/2
            turning = 0

            base_turn = 5


            input("Press enter to start")
            old_curr_tape_color = TapeColor.OTHER
            curr_tape_color = TapeColor.OTHER
            # display_thread.start()

            last_print = time.time()
            print_timer = 0.1

            while True:
                time.sleep(TIME_INTERVAL)
                rgb = rgb_sensor.get_rgb()
                _curr_tape_color = get_tape_color(rgb)
                # _curr_tape_color = get_closest_color(rgb)
                old_curr_tape_color = curr_tape_color
                curr_tape_color = _curr_tape_color

                # If its other, lets just keep the same heading
                if(curr_tape_color == TapeColor.OTHER or curr_tape_color == TapeColor.TABLE):
                    # turning = 0
                    # ahead_speed *= SPEED_STEP
                    if old_curr_tape_color == TapeColor.RED:
                        curr_tape_color = TapeColor.RED
                        turning = base_turn
                    else:
                        curr_tape_color = TapeColor.BLACK
                        turning = 0
                    ahead_speed *= SPEED_STEP
                # If its black, stay on course
                elif(curr_tape_color == TapeColor.BLACK):
                    turning = 0
                    ahead_speed /= SPEED_STEP
                # If its red, turn right
                elif(curr_tape_color == TapeColor.RED):
                    if(old_curr_tape_color == TapeColor.RED):
                        turning = min(100,turning+1)
                    else:
                        turning = base_turn
                    ahead_speed /= SPEED_STEP
                # If its blue, turn left
                elif(curr_tape_color == TapeColor.BLUE):
                    if(old_curr_tape_color == TapeColor.RED):
                        turning = min(100,turning-1)
                    else:
                        turning = -base_turn
                    # ahead_speed /= SPEED_STEP
                    
                    


                ahead_speed = max(min(ahead_speed,MAX_SPEED),SAFE_SPEED)
                motors.set_speed(int(ahead_speed),turning)
                if(time.time() - last_print > print_timer):
                    last_print = time.time()
                    # os.system('clear')
                    print(f"Time: {get_current_time_string()}")
                    print(f"RGB: {rgb}")
                    print(f"Tape: {curr_tape_color.name}")
                    print(f"L: {motors.left_motor.current_power} R: {motors.right_motor.current_power}")
                    print(f"Speed: {ahead_speed} Turning: {turning}")
    except KeyboardInterrupt:
        print("Exiting")
        # display_thread.join()
        display.clear()
        

    


if __name__ == "__main__":
    main()