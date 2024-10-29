import RPi.GPIO as GPIO
from ..constants import MAX_POWERLEVEL as C_MAX_POWERLEVEL
from ..utils import get_duty_cycle_values_from_speed,clamp_speed
from .encoder_reader import EncoderReader
import time
import threading

class Motor:
    NAME:str = "Motor"
    FORWARD:int = 0
    BACKWARD:int = 0
    MAX_POWERLEVEL:int
    UPDATES_PER_SECOND = 10
    UPDATE_INTERVAL = 1 / UPDATES_PER_SECOND

    target_rpm:int = 0
    # PID Parameters
    Kp:float = 0.05 # Proportional, used to correct the error
    Ki:float = 0.01 # Integral, used to correct the error over time
    Kd:float = 0.1  # Derivative, used to predict the error
    previous_error:float = 0


    def __init__(self,gpio_in_1:int,gpio_in_2:int,c_gpio_1:int,c_gpio_2:int,name:str="Motor",max_powerlevel:int = C_MAX_POWERLEVEL):
        self.gpio_in_1 = gpio_in_1
        self.gpio_in_2 = gpio_in_2
        GPIO.setmode(GPIO.BCM)

        self.NAME = name
        # Set up GPIO pins
        GPIO.setup(self.gpio_in_1, GPIO.OUT)
        GPIO.setup(self.gpio_in_2, GPIO.OUT)
        # Set up PWM on AIN1 and AIN2
        self.pwm_AIN1 = GPIO.PWM(self.gpio_in_1, 1000)  # 1 kHz frequency
        self.pwm_AIN2 = GPIO.PWM(self.gpio_in_2, 1000)  # 1 kHz frequency
        # Start PWM with 0% duty cycle (motor stopped)
        self.pwm_AIN1.start(0)
        self.pwm_AIN2.start(0)
        self._set_duty_cycle()

        self.MAX_POWERLEVEL = max_powerlevel
        self.pidreader = EncoderReader(c_gpio_1,c_gpio_2)
        self._stop_event = threading.Event()
        self._update_thread = threading.Thread(target=self._listener)
        self._update_thread.daemon = True # Allow the program to exit even if thread is running
        self._update_thread.start()

    def _listener(self):
        while not self._stop_event.is_set():
            time.sleep(self.UPDATE_INTERVAL)
            # Stop the motor if target RPM is zero
            if self.target_rpm == 0:
                self.motor_stop()
                continue
            # Lets get the current RPM and if the target speed is reversing or not
            current_rpm = self.pidreader.rpm_adjusted
            target_is_forward = self.target_rpm > 0
            # Getting the curr error
            error = self.target_rpm - current_rpm
            error_delta = error - self.previous_error
            self.previous_error = error
            # PID calculations
            proportional = self.Kp * error
            integral = self.Ki * error
            derivative = self.Kd * error_delta
            if(target_is_forward):
                self.BACKWARD = 0
                current_power = self.FORWARD
                current_power += proportional + integral + derivative
                self.FORWARD = int(current_power)
            else:
                self.FORWARD = 0
                current_power = self.BACKWARD
                current_power += -(proportional + integral + derivative)
                self.BACKWARD = int(current_power)
            self._set_duty_cycle()

    def set_max_powerlevel(self,max_speed:int)->None:
        """Updates the speed ceiling"""
        self.MAX_POWERLEVEL = clamp_speed(max_speed,10,100)

    def motor_stop(self):
        """Stops the motor"""
        self.FORWARD = 0
        self.BACKWARD = 0
        self._set_duty_cycle()

    def set_target_rpm(self,value:int):
        """Sets the target RPM (-200 to 200)"""
        self.target_rpm = clamp_speed(value,-200,200)

    def _set_duty_cycle(self):
        """Sets the duty cycle for the motor"""
        self.FORWARD = clamp_speed(self.FORWARD,0,self.MAX_POWERLEVEL)
        self.BACKWARD = clamp_speed(self.BACKWARD,0,self.MAX_POWERLEVEL)
        self.pwm_AIN1.ChangeDutyCycle(self.FORWARD)
        self.pwm_AIN2.ChangeDutyCycle(self.BACKWARD)

    @property
    def rpm(self):
        """Returns the current RPM"""
        return int(self.pidreader.rpm)

    @property
    def current_power(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD > 0):
            return self.FORWARD
        elif(self.BACKWARD > 0):
            return -self.BACKWARD
        return 0
    
    def __str__(self) -> str:
        error = self.target_rpm - int(self.pidreader.rpm)
        return f"""{self.NAME}: 
POWER: {self.current_power} 
FORWARD: {self.FORWARD}
BACKWARD: {self.BACKWARD}
TARGET RPM: {self.target_rpm}
RPM: {int(self.pidreader.rpm_adjusted)}
FORWARDS?: {self.pidreader.is_going_forward()}
ERROR: {error}
P: {self.Kp * error}
I: {self.Ki * error}
D: {self.Kd * (error - self.previous_error)}"""
    
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def stop(self):
        """Stop the RPM update thread"""
        self._stop_event.set()
        self._update_thread.join()
        
    def cleanup(self):
        """Cleans up the motor"""
        print(f"Cleaning up {self.NAME}")
        GPIO.cleanup()
        self.pidreader.cleanup()
        self.motor_stop()
        self.stop()