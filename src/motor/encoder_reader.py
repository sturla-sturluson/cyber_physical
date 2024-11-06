import time
from gpiozero import RotaryEncoder
import threading

class EncoderReader:
    PPR = 700  # Pulses Per Revolution of the encoder
    UPDATES_PER_SECOND = 100
    UPDATE_INTERVAL = 1 / UPDATES_PER_SECOND
    alpha = 0.2  # Smoothing factor for EMA
    OLD_STEP = 0
    CURR_STEP = 0

    def __init__(self, c1_pin: int, c2_pin: int):
        self.encoder = RotaryEncoder(c1_pin,c2_pin)
        self.curr_rpm = 0
        if(c1_pin == 0 or c2_pin == 0):
            print("Encoder not connected")
            self.curr_rpm = -1
            return
        self._pulse_count = 0
        # self._lock = threading.Lock()

        # # Start the background RPM update thread
        # self._stop_event = threading.Event()
        # self._update_thread = threading.Thread(target=self._update_rpm)
        # # self._update_thread.daemon = True # Allow the program to exit even if thread is running
        # self._update_thread.start()

        # # Attach a listener for encoder pulses
        # self.encoder.when_rotated = self._increment_pulse_count

    # def _increment_pulse_count(self):
    #     """Increment pulse count when encoder rotates"""
    #     with self._lock:
    #         self._pulse_count += 1

    # def _calculate_rpm(self, pulse_count: int) -> float:
    #     """Calculate RPM from pulse count over the specified time interval"""
    #     revolutions = pulse_count / self.PPR
    #     return (revolutions / self.UPDATE_INTERVAL) * 60  # convert to RPM

    # def _update_rpm(self):
    #     """Update the RPM at a fixed interval using exponential moving average."""
    #     pulse_count = 1
    #     while not self._stop_event.is_set():
    #         time.sleep(self.UPDATE_INTERVAL)
    #         # Updating to check if the encoder is going forward or backward
    #         self.OLD_STEP = self.CURR_STEP
    #         self.CURR_STEP = self.encoder.steps
    
    #         with self._lock:
    #             pulse_count = self._pulse_count
    #             self._pulse_count = 0  # reset pulse count after reading
    #         rpm = self._calculate_rpm(pulse_count)
    #         # Apply exponential moving average
    #         self.curr_rpm = self.alpha * rpm + (1 - self.alpha) * self.curr_rpm

    @property   
    def rpm(self):
        """Return the current RPM reading"""
        # with self._lock:
        #     return self.curr_rpm
        return self.curr_rpm
    @property   
    def rpm_adjusted(self):
        """Return the current RPM reading, but negative if the encoder is going backwards"""
        if(self.is_going_forward()):
            return self.curr_rpm
        return -self.curr_rpm

    def is_going_forward(self)->bool:
        """Returns True if the encoder is going forward"""
        return self.CURR_STEP <= self.OLD_STEP

    # def stop(self):
    #     """Stop the RPM update thread"""
    #     self._stop_event.set()
    #     self._update_thread.join()

    def cleanup(self):
        """Cleans up the PID Controller"""
        # self.stop()
        self.encoder.close()
        print("Exiting PID Controller")