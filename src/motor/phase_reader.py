# Importing modules and classes
import time
import numpy as np
from gpiozero import RotaryEncoder
import asyncio
import threading
import queue


class PhaseReader:
    PPR = 700  # Pulses Per Revolution of the encoder
    BOUNCE_TIME = 0.01  # Time in seconds to debounce the encoder
    UPDATES_PER_SECOND = 10
    _curr_rpm:int = 0
    curr_rpm:int = 0
    # Alpha value for the exponential moving average
    alpha:float = 0.2 # (0.1 -> 0.3)

    def __init__(self,c1_pin:int,c2_pin:int):
        self.effective_ppr = self.PPR
        if(self.BOUNCE_TIME is not None):
            self.effective_ppr = int(self.PPR * self.BOUNCE_TIME)

        self.encoder = RotaryEncoder(
            c1_pin,
            c2_pin,
            bounce_time=self.BOUNCE_TIME,
            max_steps=0,
            threshold_steps=(1, 1),
            wrap=False,
            )

        self.tsample =  1/self.UPDATES_PER_SECOND
        # How many samples get stored per 10 seconds
        # self.sample_time_range = 1
        # self.angle_samples = int(self.sample_time_range / self.tsample)

        # self.angle_arr_index = 0
        # self.angle_arr:list[int] = [0 for _ in range(self.angle_samples)]

        # self.angle_curr:int = 0
        # self.tprev = 0
        # self.tcurr = 0
        # self.tstart = time.perf_counter()

        self.rpm_queue_size = 20
        self.rpm_queue = queue.Queue()

        self.listen_event = threading.Event()
        self.listen_thread = threading.Thread(target=self._listener)

        self.last_pulse_time = time.perf_counter()

        # Set up callback for each pulse detected by encoder
        self.encoder.when_rotated = self._pulse_detected


    def start(self):
        """Starts the encoder reading in a separate thread"""
        self.listen_event.set()
        if not self.listen_thread.is_alive():
            self.listen_thread.start()

    def stop(self):
        """Stops the encoder reading thread"""
        self.listen_event.clear()
        self.listen_thread.join()

    def _listener(self):
        """Threaded listener to maintain encoder updates"""
        while self.listen_event.is_set():
            time.sleep(self.tsample)
            self._set_rpm_buffer_smoothing()

    def _pulse_detected(self):
        """Callback for each encoder pulse to calculate frequency-based RPM"""
        current_time = time.perf_counter()
        
        # Calculate time difference (interval) between pulses
        time_interval = current_time - self.last_pulse_time
        self.last_pulse_time = current_time  # Update last pulse time

        # Calculate RPM from time interval
        if time_interval > 0:  # Avoid division by zero
            self._curr_rpm = 60 / time_interval


    # def _listener(self):
    #     """Threaded listener to periodically sample the encoder position"""
    #     while self.listen_event.is_set():
    #         self.reading()
    #         time.sleep(self.tsample)  # Sleep between samples

    # def reading(self):
    #     """Performs the reading of the encoder"""
    #     self.tprev = self.tcurr
    #     self.tcurr = time.perf_counter() - self.tstart
    #     self.angle_arr_index = (self.angle_arr_index + 1) % self.angle_samples
    #     self.angle_curr = -int(360 / self.ppr * self.encoder.steps)
    #     self.angle_arr[self.angle_arr_index] = self.angle_curr
    #     # Calculate the RPM
    #     self._set_rpm_buffer_smoothing()
    #     # self._set_rpm_ema_smoothing()

    def _set_rpm_buffer_smoothing(self):
        """Returns the RPM with buffer smoothing
        Buffer smoothing uses a queue to store the last n RPM readings,
        then calculates the average of the last n readings.
        """
        curr_rpm = self._curr_rpm
        self.rpm_queue.put(curr_rpm)
        if self.rpm_queue.qsize() > self.rpm_queue_size:
            self.rpm_queue.get()
        self.curr_rpm = np.mean(list(self.rpm_queue.queue))


    # def _set_rpm_ema_smoothing(self):
    #     """Returns the RPM with exponential moving average smoothing
    #     Exponential Moving Average (EMA), which provides a weighted average of past RPM readings. 
    #     EMA gives more weight to recent values, so it adapts more quickly to changes compared to a simple moving average.
    #     """
    #     curr_rpm = self._get_curr_rpm()
    #     self.curr_rpm = self.alpha * curr_rpm + (1 - self.alpha) * self.curr_rpm

    # def _get_curr_rpm(self):
    #     """Returns the RPM of the encoder"""
    #     old_index = (self.angle_arr_index + 1 ) % self.angle_samples
    #     angle_diff = self.angle_arr[self.angle_arr_index] - self.angle_arr[old_index]
    #     minute_angle = angle_diff / self.sample_time_range * 60 # Angles per minute
    #     curr_rpm = minute_angle // 360
    #     return curr_rpm



    @property
    def rpm(self)->float:
        """Returns the RPM of the encoder"""
        return self.curr_rpm
    
    # @property
    # def angle(self)->float:
    #     """Returns the angle of the encoder"""
    #     return self.angle_curr
    
    def __str__(self) -> str:
        # return f"Angle: {self.angle:.2f} RPM: {self.rpm:.2f}"
        return f"RPM: {self.rpm:.2f}"

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        self.cleanup()

    def cleanup(self):
        """Cleans up the PID Controller"""
        self.stop()
        self.encoder.close()
        print("Exiting PID Controller")