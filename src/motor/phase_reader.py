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
        self.rpm_queue_size = 20
        self.rpm_queue = list()


        self.last_pulse_time = time.perf_counter()

        # Set up callback for each pulse detected by encoder
        self.encoder.when_rotated = self._pulse_detected


    def start(self):
        """Starts the encoder reading in a separate thread"""
        self.listen_event = threading.Event()
        self.listen_thread = threading.Thread(target=self._listener)

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
            # print(self)

    def _pulse_detected(self):
        """Callback for each encoder pulse to calculate frequency-based RPM"""
        current_time = time.perf_counter()
        # Calculate time difference (interval) between pulses
        time_interval = current_time - self.last_pulse_time
        self.last_pulse_time = current_time  # Update last pulse time
        # since its 700 pulses per revolution, we divide by 700
        # print(time_interval)
        self._curr_rpm = 60/(time_interval) / self.PPR

    def _set_rpm_buffer_smoothing(self):
        """Returns the RPM with buffer smoothing
        Buffer smoothing uses a queue to store the last n RPM readings,
        then calculates the average of the last n readings.
        """
        curr_time = time.perf_counter()
        # if its been more than 250ms since the last pulse, we set the rpm to 0
        if(self._curr_rpm == 0):
            self.curr_rpm = 0
            return
        if self.last_pulse_time + 0.50 < curr_time:
            self.rpm_queue = list()
            if(self._curr_rpm < 5):
                self._curr_rpm = 0
                self.curr_rpm = 0
            else:
                self.curr_rpm = self.curr_rpm * 0.9
                # self.last_pulse_time = curr_time
            return
        curr_rpm = self._curr_rpm
        self.rpm_queue.append(curr_rpm)
        if(len(self.rpm_queue) > self.rpm_queue_size):
            self.rpm_queue.pop(0)
        self.curr_rpm = np.mean(self.rpm_queue)

    @property
    def rpm(self)->int:
        """Returns the RPM of the encoder"""
        return int(self.curr_rpm)

    
    def __str__(self) -> str:
        return f"RPM: {self.rpm}"

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type,exc_value,traceback):
        self.cleanup()

    def cleanup(self):
        """Cleans up the PID Controller"""
        self.stop()
        self.encoder.close()
        print("Exiting PID Controller")