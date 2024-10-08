import RPi.GPIO as GPIO
from ..constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
from .common import get_duty_cycle_values_from_speed

class Motor:
    NAME:str = "Motor"
    FORWARD:int = 0
    BACKWARD:int = 0

    def __init__(self,gpio_in_1:int,gpio_in_2:int,name:str="Motor"):
        self.gpio_in_1 = gpio_in_1
        self.gpio_in_2 = gpio_in_2
        GPIO.setmode(GPIO.BCM)
        nSLEEP = 25  # Connect nSLEEP to GPIO 25 or directly to 3.3V/5V

        self.NAME = name

        # Set up GPIO pins
        GPIO.setup(self.gpio_in_1, GPIO.OUT)
        GPIO.setup(self.gpio_in_2, GPIO.OUT)
        GPIO.setup(nSLEEP, GPIO.OUT)
        GPIO.output(nSLEEP, GPIO.HIGH)

        # Set up PWM on AIN1 and AIN2
        self.pwm_AIN1 = GPIO.PWM(self.gpio_in_1, 1000)  # 1 kHz frequency
        self.pwm_AIN2 = GPIO.PWM(self.gpio_in_2, 1000)  # 1 kHz frequency

        # Start PWM with 0% duty cycle (motor stopped)
        self.pwm_AIN1.start(0)
        self.pwm_AIN2.start(0)

        self._set_duty_cycle()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cleanup(self):
        """Cleans up the motor"""
        print(f"Cleaning up {self.NAME}")
        GPIO.cleanup()
        self.motor_stop()

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


    def _set_duty_cycle(self):
        """Sets the duty cycle for the motor"""
        self.pwm_AIN1.ChangeDutyCycle(self.FORWARD)
        self.pwm_AIN2.ChangeDutyCycle(self.BACKWARD)

    @property
    def current_speed(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD > 0):
            return self.FORWARD
        elif(self.BACKWARD > 0):
            return -self.BACKWARD
        return 0

    def __str__(self) -> str:
        return f"{self.NAME}: {self.current_speed}"