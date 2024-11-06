import RPi.GPIO as GPIO
from ..constants import MAX_POWERLEVEL,MAX_RPM
from ..utils import get_duty_cycle_values_from_speed,clamp_speed
from .encoder_reader import EncoderReader
import time
import threading



POWER_TO_RPM = {
    0:0,
    10:10,
    20:20,
    30:30,
    40:40,
    50:50,
    60:60,
    70:70,
    80:80,
    90:90,
    100:100
}


class Motor:
    NAME:str = "Motor"
    FORWARD_POWER:int = 0
    BACKWARD_POWER:int = 0
    UPDATES_PER_SECOND = 50
    UPDATE_INTERVAL = 1 / UPDATES_PER_SECOND

    PID_SELF_CORRECT:bool 
    target_rpm:int = 0
    # PID Parameters
    Kp:float = 0.1 # Proportional, used to correct the error
    Ki:float = 0.01 # Integral, used to correct the error over time
    Kd:float = 0.1  # Derivative, used to predict the error
    previous_error:float = 0


    def __init__(self,
                 gpio_in_1:int,gpio_in_2:int,
                 c_gpio_1:int = 0, c_gpio_2:int = 0,
                 pid_self_correction:bool = False,
                 name:str="Motor"):
        self.gpio_in_1 = gpio_in_1
        self.gpio_in_2 = gpio_in_2
        GPIO.setmode(GPIO.BCM)
        self.PID_SELF_CORRECT = pid_self_correction

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
        self.pidreader = EncoderReader(c_gpio_1,c_gpio_2)
        if(self.PID_SELF_CORRECT):
            self._stop_event = threading.Event()
            self._update_thread = threading.Thread(target=self._listener)
            # self._update_thread.daemon = True # Allow the program to exit even if thread is running
            self._update_thread.start()

    def  set_pid_params(self,Kp:float,Ki:float,Kd:float):
        """Sets the PID parameters"""
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

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
            # OPTIONALLY LETS SET TARGET ALWAYS TO BE A LITTLE BIT LOWER
            # error =  current_rpm - self.target_rpm
            error =  (self.target_rpm * 0.95) - current_rpm
            error_delta = error - self.previous_error
            self.previous_error = error
            # PID calculations
            proportional = self.Kp * error
            integral = self.Ki * error
            derivative = self.Kd * error_delta

            controller_output = proportional + integral + derivative

            current_power = self.current_power
            if(controller_output>current_power):
                controller_output = current_power + 1
            elif(controller_output < current_power):
                controller_output = current_power - 1
            # Setting the power output
            self._set_power(int(controller_output))


    def motor_stop(self):
        """Stops the motor"""
        self.FORWARD_POWER = 0
        self.BACKWARD_POWER = 0
        self._set_duty_cycle()

    def set_target_rpm(self,value:int):
        """Sets the target RPM"""
        self.target_rpm = clamp_speed(value,-MAX_RPM,MAX_RPM)

    def set_target_power(self,value:int):
        """Sets the target power from -100 to 100"""
        self._set_power(value)

    def _set_power(self,power_output:int):
        """Setting power from -100 to 100"""
        if(power_output > 0):
            self.FORWARD_POWER = power_output
            self.BACKWARD_POWER = 0
        else:
            self.FORWARD_POWER = 0
            self.BACKWARD_POWER = -power_output
        self._set_duty_cycle()

    def _set_duty_cycle(self):
        """Sets the duty cycle for the motor"""
        self.FORWARD_POWER = clamp_speed(self.FORWARD_POWER,0,MAX_POWERLEVEL)
        self.BACKWARD_POWER = clamp_speed(self.BACKWARD_POWER,0,MAX_POWERLEVEL)
        self.pwm_AIN1.ChangeDutyCycle(self.FORWARD_POWER)
        self.pwm_AIN2.ChangeDutyCycle(self.BACKWARD_POWER)

    @property
    def rpm(self):
        """Returns the current RPM"""
        return int(self.pidreader.rpm)

    @property
    def current_power(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD_POWER > 0):
            return self.FORWARD_POWER
        elif(self.BACKWARD_POWER > 0):
            return -self.BACKWARD_POWER
        return 0
    
    def __str__(self) -> str:
        error = self.target_rpm - int(self.pidreader.rpm)
        return f"""{self.NAME}: 
POWER: {self.current_power} 
FORWARD: {self.FORWARD_POWER}
BACKWARD: {self.BACKWARD_POWER}
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
        if(self.PID_SELF_CORRECT):
            self.stop()
        GPIO.cleanup()
        self.pidreader.cleanup()
        self.motor_stop()

