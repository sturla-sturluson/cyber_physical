import board
import math
import numpy as np
import time
from typing import Protocol
import random
import os
import asyncio
import threading
import json
from pathlib import Path
import pprint
from adafruit_lsm303dlh_mag import LSM303DLH_Mag
import busio

pp = pprint.PrettyPrinter(indent=4)

CONFIG_DIR = "~/.config/cyber_physical_systems"
FILE_NAME = "compass_calibration.json"


class IMagneticSensor(Protocol):
    def get_x_y_z(self) -> tuple[float,float,float]:
        ...

class FakeMagneticSensor(IMagneticSensor):
    """Fake magnetic sensor for testing"""
    def get_x_y_z(self) -> tuple[float,float,float]:
        return random.uniform(-90,90),random.uniform(-90,90),random.uniform(-90,90)
    

class MagneticSensor(IMagneticSensor):
    """Magnetic sensor that uses the LSM303DLH_Mag sensor"""
    def __init__(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)

    def get_x_y_z(self) -> tuple[float,float,float]:
        x, y, z = self.mag.magnetic
        return x, y, z
    
class X_Y_Map:
    """ A 180x180 map that shows the cords
    from -90 to 90 degrees
    cord (52,32) would be added map[142,122]
    All of them will be 0, if a cord is added it will be 1
    """
    def __init__(self) -> None:
        # Scale is the number of degrees per grid
        # 1 would be 180x180 add 1 for the axis
        dimensions = 180 + 1

        self.map = np.zeros((dimensions,dimensions),dtype=int)
        # Create vertical Y axis and horizontal X axis

        for i in range(dimensions):
            self.map[dimensions//2,i] = -1
            self.map[i,dimensions//2] = -1

    def add_cord(self,x:int|float,y:int|float):
        """Adds a cord to the map"""
        # We add 90 to make it positive
        adj_x = int(x) + 90
        adj_y = int(y) + 90
        self.map[adj_x,adj_y] = 1

    def _get_row_list(self,width:int,value:str = "  ",center:str = "Y ")->list[str]:
        """Returns a list of strings for a row"""
        list_str = list()
        for i in range(width+1):
            if(i == width//2):
                list_str.append(center)
            else:
                list_str.append(value)
        return list_str
    
    def get_scaled_map(self,scale:int = 1)->str:
        """Returns a scaled map"""
        scaled_ratio = (180//scale) +1
        str_map = [[] for i in range(scaled_ratio)]
        for i in range(scaled_ratio):
            if(i == scaled_ratio//2):
                str_map[i] = self._get_row_list(scaled_ratio,"X ","+ ")
            else:
                str_map[i] = self._get_row_list(scaled_ratio)         
        for i in range(scaled_ratio-1):   
            for j in range(scaled_ratio-1):
                for x in range(scale):
                    for y in range(scale):
                        if(self.map[i*scale+x,j*scale+y] == 1):
                            str_map[i][j] = "1 "
                            break
            
        return "\n".join(["".join(row) for row in str_map])

    def __str__(self) -> str:
        return self.get_scaled_map(1)

class Cords:
    name:str = ""
    x:int|float|None = None
    y:int|float|None = None
    def __init__(self, name:str = "", x:int|float|None = None, y:int|float|None = None) -> None:
        self.name = name
        self.x = x
        self.y = y

    def __str__(self) -> str:
        x_str = "None" if self.x is None else str(f"{self.x:.2f}")
        y_str = "None" if self.y is None else str(f"{self.y:.2f}")
        name_str = self.name.rjust(10)
        x_str = x_str.rjust(5)
        y_str = y_str.rjust(5)
        return f"{name_str} | {x_str} | {y_str}"

    def set_max(self,x:int|float,y:int|float):
        """Just used for the the max cords"""
        self.x = x if self.x is None else max(self.x,x)
        self.y = y if self.y is None else max(self.y,y)

    def set_min(self,x:int|float,y:int|float):
        """Just used for the the min cords"""
        self.x = x if self.x is None else min(self.x,x)
        self.y = y if self.y is None else min(self.y,y)

    def set_cords(self,x:int|float,y:int|float):
        self.x = x
        self.y = y


class CompassCalibrator:
    def __init__(self, magnetic_sensor:IMagneticSensor) -> None:
        self.magnetic_sensor = magnetic_sensor
        self.current_cord = Cords(name="Current X/Y")
        self.max_cord = Cords(name="MAX X/Y")
        self.min_cord = Cords(name="MIN X/Y")

        # User saved positions NESW (Clockwise)
        self.user_positions = []
        self.states = ["NORTH","EAST","SOUTH","WEST"]

        self._update_ui_event = asyncio.Event()
        self._stop_event = threading.Event()

        self.x_y_map = X_Y_Map()



    @property
    def current_state_index(self):
        """Returns the current state index"""
        return len(self.user_positions)
    
    @property
    def current_state(self):
        """Returns the current state index"""
        if(self.current_state_index >= len(self.states)):
            return ""
        return self.states[self.current_state_index]

    def _print_screen(self):
        os.system('clear')
        print("Compass Calibrator")
        print(self.x_y_map.get_scaled_map(10))
        print(f"{self.current_cord}")
        print(f"{self.max_cord}")
        print(f"{self.min_cord}")
        for user_cord in self.user_positions:
            print(f"{user_cord}")
        if(self.current_state_index >= len(self.states)):
            print("Calibration Done")
        else:
            print(f"Calibrating for {self.current_state}")

    async def _calibrate_loop(self):
        """Calibration loop that runs until the stop event is set."""
        re_draw_interval = 1
        last_draw_time = time.time()
        while not self._stop_event.is_set():
            x,y,_ = self.magnetic_sensor.get_x_y_z()
            self.current_cord.set_cords(x,y)
            self.max_cord.set_max(x,y)
            self.min_cord.set_min(x,y)
            self.x_y_map.add_cord(x,y)
            if(time.time() - last_draw_time > re_draw_interval):
                last_draw_time = time.time()
                self._print_screen()
            await asyncio.sleep(0.05)


    def _input_thread(self):
        """Handle user input in a separate thread."""
        for state in self.states:
            input(f"Press enter to calibrate for {state}")
            self._save_user_state()
            self._update_ui_event.set()  # Signal to update the screen after user input
        input(f"Go back to North and press enter to finish calibration")
        self._stop_event.set()  # Signal to stop the loop once all inputs are done

    def start_input_thread(self):
        """Starts the input thread."""
        threading.Thread(target=self._input_thread, daemon=True).start()

    async def calibrate(self):
        """Calibrates the compass"""
        # Start the input thread to handle user input without blocking
        self.start_input_thread()

        # Start the calibration loop asynchronously
        await self._calibrate_loop()

        # Print the final screen after calibration is done
        self._print_screen()
        self._save_calibration()


    def _save_user_state(self):
        """Saves the direction the user is facing"""
        x,y,_ = self.magnetic_sensor.get_x_y_z()
        cord = Cords(name=self.current_state)
        cord.set_cords(x,y)
        self.user_positions.append(cord)

    def _save_calibration(self):
        """Saves the calibration data to a file"""
        data = {
            "max": [self.max_cord.x,self.max_cord.y],
            "min": [self.min_cord.x,self.min_cord.y],
            "north": [self.user_positions[0].x,self.user_positions[0].y],
            "east": [self.user_positions[1].x,self.user_positions[1].y],
            "south": [self.user_positions[2].x,self.user_positions[2].y],
            "west": [self.user_positions[3].x,self.user_positions[3].y],
        }
        # Create the config directory if it doesn't exist
        Path(CONFIG_DIR).expanduser().mkdir(parents=True, exist_ok=True)
        dir_path = Path(CONFIG_DIR).expanduser()

        file_path = dir_path / FILE_NAME
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        ## Save the 1:1 map
        print(f"Calibration data saved to {file_path}")
        current_file_location = Path(__file__).parent
        map_scales = [1,2,5]
        for scale in map_scales:
            file_path_map = current_file_location / f"graph_{scale}-1.txt"
            map_str = self.x_y_map.get_scaled_map(scale)
            with open(file_path_map, "w") as file:
                file.write(map_str)
            print(f"Grid map saved to {file_path_map}")




def main():
    compass_calibrator = CompassCalibrator(MagneticSensor())
    asyncio.run(compass_calibrator.calibrate())


if __name__ == '__main__':
    main()