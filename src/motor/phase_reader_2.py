import time
import numpy as np
from gpiozero import RotaryEncoder
import threading

class PhaseReader:
    PPR = 700  # Pulses Per Revolution of the encoder
    BOUNCE_TIME = None #0.1  # Time in seconds to debounce the encoder
    UPDATES_PER_SECOND = 10
    alpha = 0.2  # Smoothing factor for EMA

    OLD_STEP = 0
    CURR_STEP = 0

    def __init__(self, c1_pin: int, c2_pin: int):
        self.effective_ppr = self.PPR
        if self.BOUNCE_TIME is not None:
            self.effective_ppr = int(self.PPR * self.BOUNCE_TIME)

        # Initialize the rotary encoder
        self.encoder = RotaryEncoder(
            c1_pin,
            c2_pin,
            bounce_time=self.BOUNCE_TIME,
            max_steps=0,
            threshold_steps=(1, 1),
            wrap=False,
        )

        # rpm readings list
        self.number_of_readings = 80
        self.rpm_readings = []


        # RPM related variables
        self.curr_rpm = 0
        self._pulse_count = 0
        self._lock = threading.Lock()

        # Start the background RPM update thread
        self._stop_event = threading.Event()
        self._update_thread = threading.Thread(target=self._update_rpm)
        self._update_thread.daemon = True
        self._update_thread.start()

        # Attach a listener for encoder pulses
        self.encoder.when_rotated = self._increment_pulse_count

    def _increment_pulse_count(self):
        """Increment pulse count when encoder rotates."""
        with self._lock:
            self._pulse_count += 1

    def _calculate_rpm(self, pulse_count, time_interval):
        """Calculate RPM from pulse count over the specified time interval."""
        revolutions = pulse_count / self.effective_ppr
        rpm = (revolutions / time_interval) * 60  # convert to RPM
        return rpm

    def _update_rpm(self):
        """Update the RPM at a fixed interval using exponential moving average."""
        update_interval = 1 / self.UPDATES_PER_SECOND
        while not self._stop_event.is_set():
            time.sleep(update_interval)
            self.OLD_STEP = self.CURR_STEP
            self.CURR_STEP = self.encoder.steps
            with self._lock:
                pulse_count = self._pulse_count
                self._pulse_count = 0  # reset pulse count after reading

            rpm = self._calculate_rpm(pulse_count, update_interval)

            # Apply exponential moving average
            self.curr_rpm = self.alpha * rpm + (1 - self.alpha) * self.curr_rpm
    @property   
    def rpm(self):
        """Return the current RPM reading."""
        with self._lock:
            return self.curr_rpm
    @property   
    def rpm_adjusted(self):
        """Return the current RPM reading."""
        if(self.is_going_forward()):
            return self.curr_rpm
        else:
            return -self.curr_rpm

    def is_going_forward(self)->bool:
        """Returns True if the encoder is going forward"""
        return self.CURR_STEP < self.OLD_STEP

    def stop(self):
        """Stop the RPM update thread."""
        self._stop_event.set()
        self._update_thread.join()


    def cleanup(self):
        """Cleans up the PID Controller"""
        self.stop()
        self.encoder.close()
        print("Exiting PID Controller")