import RPi.GPIO as GPIO
from ..constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
from ..utils import get_duty_cycle_values_from_speed,clamp_speed
from .phase_reader_2 import PhaseReader
import time
import threading

class Motor:
    NAME:str = "Motor"
    FORWARD:int = 0
    BACKWARD:int = 0
    MAX_POWERLEVEL:int
    SAMPLES_PER_SECOND:int = 10
    tsample:float = 1/SAMPLES_PER_SECOND

    target_rpm:int = 0

    _curr_duty_cycle:int = 0
    # PID Parameters
    # Proportional, used to correct the error
    Kp:float = 0.05
    # Integral, used to correct the error over time
    Ki:float = 0.01
    # Derivative, used to predict the error
    Kd:float = 0.1

    previous_error:float = 0



    def __init__(self,
                 gpio_in_1:int,gpio_in_2:int,
                 c_gpio_1:int,c_gpio_2:int,
                 name:str="Motor",
                 max_powerlevel:int = MAX_POWERLEVEL):
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

        self.MAX_POWERLEVEL = max_powerlevel

        self._set_duty_cycle()

        self.pidreader = PhaseReader(c_gpio_1,c_gpio_2)
        self.listen_event = threading.Event()
        self.listen_thread = threading.Thread(target=self._listener)

        # start
        self.start()

    def start(self):
        """Starts the motor"""
        self.listen_event.set()
        self.listen_thread.start()


    def _listener(self):
        while self.listen_event.is_set():
            time.sleep(self.tsample)

            # Stop the motor if target RPM is zero
            if self.target_rpm == 0:
                self.motor_stop()
                continue

            current_rpm = self.pidreader.rpm_adjusted
            target_is_forward = self.target_rpm > 0

            # # Invert current RPM if the direction doesn't match the target
            # if target_is_forward:
            #     current_rpm = -current_rpm

            # Calculate the error
            error = self.target_rpm - current_rpm

            # PID calculations
            proportional = self.Kp * error
            integral = self.Ki * error
            derivative = self.Kd * (error - self.previous_error)
            
            # Update the previous error for the derivative term
            self.previous_error = error

            if(target_is_forward):
                self.BACKWARD = 0
                current_power = self.FORWARD
                current_power += proportional + integral + derivative
                self.FORWARD = current_power
            else:
                self.FORWARD = 0
                current_power = self.BACKWARD
                current_power += -(proportional + integral + derivative)
                self.BACKWARD = current_power



            self._set_duty_cycle()

                



    def set_max_speed(self,max_speed:int)->None:
        """Updates the speed ceiling"""
        # Hard low is 10, hard max is 100
        self.MAX_POWERLEVEL = clamp_speed(max_speed,10,100)

    def motor_stop(self):
        """Stops the motor"""
        self.BACKWARD = 0
        self.FORWARD = 0
        self._set_duty_cycle()

    def set_target_speed(self,value:int):
        """Sets the speed from -100 to 100"""
        # Max rpm is 130
        self.target_rpm = clamp_speed(value,-200,200)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cleanup(self):
        """Cleans up the motor"""
        print(f"Cleaning up {self.NAME}")
        GPIO.cleanup()
        self.pidreader.cleanup()
        self.motor_stop()



    def _set_duty_cycle(self):
        """Sets the duty cycle for the motor"""
        forward = clamp_speed(self.FORWARD,0,self.MAX_POWERLEVEL)
        backward = clamp_speed(self.BACKWARD,0,self.MAX_POWERLEVEL)
        # print(f"FORWARD: {forward} BACKWARD: {backward}")
        self.pwm_AIN1.ChangeDutyCycle(forward)
        self.pwm_AIN2.ChangeDutyCycle(backward)


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
    

# proportional = self.Kp * error
# integral = self.Ki * error
# derivative = self.Kd * (error - self.previous_error)
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