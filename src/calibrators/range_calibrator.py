from ..sensors import RangeSensor
import time
import os
import asyncio
import threading
from ..constants import RANGE_CALIBRATION_FILE_PATH
import datetime as dt
import json
import numpy as np
from ..utils import get_robust_avg


class RangeSensorCalibrator:
    def __init__(self) -> None:
        self.distances = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
        self.measurements = list()
        self.range_sensor = RangeSensor()
        self.stop_event = threading.Event()
        self._update_ui_event = asyncio.Event()

    async def calibrate_loop(self):        
        """Calibration loop that runs until the stop event is set."""
        while not self.stop_event.is_set():
            os.system('clear')
            self.print_results()
            print(f"{self.range_sensor}")
            current_measurement = self.distances[len(self.measurements)%len(self.distances)]
            print(f"Press Enter when you are {current_measurement} cm away from the sensor.")
            await asyncio.sleep(0.10)

    def print_results(self):
        if(len(self.measurements) == 0):
            return
        print("Results")
        for i in range(len(self.measurements)):
            print(f"{i}: {self.measurements[i]}")

    def _get_measurement(self,distance:int):
        """The method that gets called when the user presses enter."""
        # We are gonna collect measurements for 1 second
        time_collecting = 1
        start_time = time.time()
        voltage_arr = np.array([])
        measurement_arr = np.array([])
        while time.time() - start_time < time_collecting:
            voltage = self.range_sensor.get_voltage()
            measurement = self.range_sensor.get_raw_value()
            voltage_arr = np.append(voltage_arr,voltage)
            measurement_arr = np.append(measurement_arr,measurement)
        avg_voltage = get_robust_avg(voltage_arr)
        avg_measurement = get_robust_avg(measurement_arr)
        self.measurements.append((distance,avg_measurement,avg_voltage))

    def _input_thread(self):
        """Handle user input in a separate thread."""
        while len(self.measurements) < len(self.distances):
            input()
            distance = self.distances[len(self.measurements)%len(self.distances)]
            self._get_measurement(distance)
        self.stop_event.set()

        current_date = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path =  RANGE_CALIBRATION_FILE_PATH
        time_stamp_file_path = file_path.parent / f"{current_date}_{file_path.name}"
        data = {}
        for i in range(len(self.measurements)):
            data[self.distances[i]] = self.measurements[i]
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        with open(time_stamp_file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Calibration data saved to {file_path}")

    async def calibrate(self):
        threading.Thread(target=self._input_thread).start()
        await self.calibrate_loop()