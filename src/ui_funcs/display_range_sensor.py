from ..sensors import RangeSensor
import time
import os
import asyncio
import threading


class RangeSensorCalibrator:
    def __init__(self) -> None:
        self.distances = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150] # Cm to benchmark
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

    def _input_thread(self):
        """Handle user input in a separate thread."""
        while len(self.measurements) < len(self.distances):
            input()
            distance = self.distances[len(self.measurements)%len(self.distances)]
            measurement = self.range_sensor.get_data()
            self.measurements.append((distance,*measurement))
            self._update_ui_event.set()
        self.stop_event.set()


    async def calibrate(self):
            threading.Thread(target=self._input_thread).start()
            await self.calibrate_loop()




def run_range_sensor():
    calibrator = RangeSensorCalibrator()
    asyncio.run(calibrator.calibrate())
    calibrator.print_results()
    print("Calibration complete.")
