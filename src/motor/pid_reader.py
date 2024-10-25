# Importing modules and classes
import time
import numpy as np
from gpiozero import RotaryEncoder
import asyncio
import threading


class PID_READER:
    ppr = 700  # Pulses Per Revolution of the encoder



    def __init__(self,c1_pin:int,c2_pin:int):
        self.encoder = RotaryEncoder(c1_pin, c2_pin, max_steps=0)
        self.tsample = 0.1  # Sampling period for code execution (s)
        # How many samples get stored per 10 seconds
        self.sample_time_range = 1
        self.angle_samples = int(self.sample_time_range / self.tsample)

        self.angle_arr_index = 0
        self.angle_arr:list[int] = [0 for _ in range(self.angle_samples)]

        self.angle_curr:int = 0
        self.tprev = 0
        self.tcurr = 0
        self.tstart = time.perf_counter()
        self.running = False
        # event
        self.listen_event = threading.Event()
        self.listen_thread = threading.Thread(target=self._listener)

    def start(self):
        """Starts the PID Controller"""
        self.running = True
        self.listen_thread.start()



    def _listener(self):
        while self.running:
            # Pausing for `tsample` to give CPU time to process encoder signal
            time.sleep(self.tsample)
            self.tprev = self.tcurr
            self.tcurr = time.perf_counter() - self.tstart
            self.angle_arr_index = (self.angle_arr_index + 1) % self.angle_samples
            self.angle_curr = -int(360 / self.ppr * self.encoder.steps)
            self.angle_arr[self.angle_arr_index] = self.angle_curr

    def _get_sample(self,index:int,up:bool)->float:
        """Returns a sample of the angle array, +- range/2"""
        slice_range = 2
        if(up):
            bottom = index
            top = index + slice_range
        else:
            bottom = index - slice_range
            top = index
        data_range = list()
        if bottom < 0 or top > self.angle_samples:
            data_range = self.angle_arr[bottom:] + self.angle_arr[:top]
        else:
            data_range = self.angle_arr[bottom:top]
        return sum(data_range) / len(data_range)

    @property
    def rpm(self)->float:
        """Returns the RPM of the encoder"""
        old_index = (self.angle_arr_index + 1 ) % self.angle_samples
        angle_prev = self._get_sample(old_index,True)
        angle_curr = self._get_sample(self.angle_arr_index,False)
        angle_diff = angle_curr - angle_prev
        # Normalize the angle diff to 0-360
        # One RPM is 360° in 60 seconds
        minute_angle = angle_diff / self.sample_time_range * 60
        return minute_angle // 360

    
    
    @property
    def angle(self)->float:
        """Returns the angle of the encoder"""
        return self.angle_curr
    
    def __str__(self) -> str:
        return f"Angle: {self.angle:.2f} RPM: {self.rpm:.2f}"

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        self.cleanup()

    def cleanup(self):
        """Cleans up the PID Controller"""
        self.encoder.close()
        print("Exiting PID Controller")