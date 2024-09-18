import board
import time
import random
import os
import asyncio
import threading
import json
from pathlib import Path
from adafruit_lsm303dlh_mag import LSM303DLH_Mag
import busio
from .utils import X_Y_Map, degrees_to_coordinates, get_NSEW_string





class FakeMagneticSensor():
    LAST_ANGLE = 0
    """Fake magnetic sensor for testing"""
    def get_x_y_z(self) -> tuple[float,float,float]:
        self.LAST_ANGLE += random.uniform(-1,2)
        self.LAST_ANGLE = self.LAST_ANGLE % 360
        x,y = degrees_to_coordinates(int(self.LAST_ANGLE))
        x = random.uniform(x-2,x+2)
        y = random.uniform(y-2,y+2)
        return x,y,random.uniform(-90,90)
    
    def get_orientation(self) -> int:
        return int(self.LAST_ANGLE)
    def get_data(self) -> tuple[int, tuple[int, int], str]:
        x,y,_ = self.get_x_y_z()
        nesw = get_NSEW_string(int(self.LAST_ANGLE))
        return int(self.LAST_ANGLE),(int(x),int(y)),nesw
        
    

class MagneticSensor():
    """Magnetic sensor that uses the LSM303DLH_Mag sensor"""
    def __init__(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mag = LSM303DLH_Mag(i2c)

    def get_x_y_z(self) -> tuple[float,float,float]:
        x, y, z = self.mag.magnetic
        return x, y, z


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
    def __init__(self) -> None:
        self.magnetic_sensor = MagneticSensor()
        self.current_cord = Cords(name="Current X/Y")
        self.max_cord = Cords(name="MAX X/Y")
        self.min_cord = Cords(name="MIN X/Y")

        # User saved positions NESW (Clockwise)
        self.user_positions = []
        self.states = ["CIRCLE","NORTH"]

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
        print(self.x_y_map.get_scaled_map(5))
        print(f"{self.current_cord}")
        print(f"{self.max_cord}")
        print(f"{self.min_cord}")
        if(self.current_state == "CIRCLE"):
            print("Rotate in a circle\nPress Enter when done")
        if(self.current_state == "NORTH"):
            print("Rotate to where you Want North to be\nPress Enter when done")

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
            await asyncio.sleep(0.10)


    def _input_thread(self):
        """Handle user input in a separate thread."""
        for state in self.states:
            input()
            self._save_user_state()
            self._update_ui_event.set()  # Signal to update the screen after user input
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
            "north": [self.user_positions[1].x,self.user_positions[1].y],
        }
        # Create the config directory if it doesn't exist
        Path(CONFIG_DIR).expanduser().mkdir(parents=True, exist_ok=True)
        dir_path = Path(CONFIG_DIR).expanduser()

        file_path = dir_path / CALIBRATION_FILE_PATH
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




