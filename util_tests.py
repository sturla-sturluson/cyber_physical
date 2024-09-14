from src.utils import get_translation_function,get_NSEW_string,calculate_orientation,degrees_to_coordinates
from src.utils.x_y_map import X_Y_Map
import numpy as np
import math
import os

    
def main():
    translate_function = get_translation_function()
    angle = 0
    x_y_map = X_Y_Map()
    #x_y_map.add_cord(0,90)
    while True:
        #x_cord, y_cord = input("Enter x and y cordinates: ").split()
        os.system('clear')
        x_cord, y_cord = degrees_to_coordinates(angle)
        print(f"Angle: {angle}")
        print(f"Original {x_cord:.1f}x {y_cord:.1f}y")
        x_cord = int(x_cord)
        y_cord = int(y_cord)
        cords = translate_function(x_cord, y_cord)
        x_y_map.add_cord(cords[0], cords[1])
        print(x_y_map.get_scaled_map(10))
        
        print(f"Angle: {angle}, {calculate_orientation(x_cord, y_cord)}")  
        # print(f"NESW: {get_NSEW_string(angle)}")
        # print(f"Translated cords: {cords[0]} {cords[1]}")
        # orientation = _calculate_orientation(cords[0], cords[1])
        # print(f"Orientation: {orientation}")
        # print(f"NESW Translated: {get_NSEW_string(orientation)}")


        input("")
        angle += 5
        angle %= 360


if __name__ == "__main__":
    main()