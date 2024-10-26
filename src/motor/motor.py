import RPi.GPIO as GPIO
from ..constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
from ..utils import get_duty_cycle_values_from_speed,clamp_speed
from .phase_reader import PhaseReader
import time
import threading

class Motor:
    NAME:str = "Motor"
    FORWARD:int = 0
    BACKWARD:int = 0
    MAX_SPEED:int
    SAMPLES_PER_SECOND:int = 5
    tsample:float = 1/SAMPLES_PER_SECOND

    target_rpm:int = 0
    # PID Parameters
    # Proportional, used to correct the error
    Kp:float = 1.0 
    # Integral, used to correct the error over time
    Ki:float = 0.5 
    # Derivative, used to predict the error
    Kd:float = 0.05  

    previous_error:float = 0

    def __init__(self,
                 gpio_in_1:int,gpio_in_2:int,
                 c_gpio_1:int,c_gpio_2:int,
                 name:str="Motor",
                 max_speed:int = MAX_SPEED):
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

        self.MAX_SPEED = max_speed

        self._set_duty_cycle()

        self.pidreader = PhaseReader(c_gpio_1,c_gpio_2)
        self.listen_event = threading.Event()
        self.listen_thread = threading.Thread(target=self._listener)

    def start(self):
        """Starts the motor"""
        self.listen_event.set()
        self.listen_thread.start()

    def _listener(self):
        """Listens for the encoder"""
        while self.listen_event.is_set():
            time.sleep(self.tsample)
            curr_speed = self.pidreader.rpm
            error = self.target_rpm - curr_speed
            # PID
            proportional = self.Kp * error
            integral = self.Ki * error
            derivative = self.Kd * (error - self.previous_error)

            control_signal = proportional + integral + derivative

            self.set_speed(int(control_signal))

            self.previous_error = error

    def set_max_speed(self,max_speed:int)->None:
        """Updates the speed ceiling"""
        # Hard low is 10, hard max is 100
        self.MAX_SPEED = clamp_speed(max_speed,10,100)

    def motor_stop(self):
        """Stops the motor"""
        self.BACKWARD = 0
        self.FORWARD = 0
        self._set_duty_cycle()

    def set_speed(self,value:int):
        """Sets the speed from -100 to 100"""
        ain_1,ain_2 = get_duty_cycle_values_from_speed(value)
        self.FORWARD = ain_1
        self.BACKWARD = ain_2
        self._set_duty_cycle() 

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
        self.pwm_AIN1.ChangeDutyCycle(clamp_speed(self.FORWARD,0,self.MAX_SPEED))
        self.pwm_AIN2.ChangeDutyCycle(clamp_speed(self.BACKWARD,0,self.MAX_SPEED))

    @property
    def current_power(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD > 0):
            return self.FORWARD
        elif(self.BACKWARD > 0):
            return -self.BACKWARD
        return 0

    def __str__(self) -> str:
        return f"{self.NAME}: {self.current_power} Angle: {int(self.pidreader.angle)} RPM: {int(self.pidreader.rpm)}"