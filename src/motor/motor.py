import RPi.GPIO as GPIO
from ..constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
from ..utils import get_duty_cycle_values_from_speed,clamp_speed
from .pid_reader import PID_READER

class Motor:
    NAME:str = "Motor"
    FORWARD:int = 0
    BACKWARD:int = 0

    MAX_SPEED:int

    def __init__(self,
                 gpio_in_1:int,gpio_in_2:int,
                 c_gpio_1:int,c_gpio_2:int,
                 name:str="Motor",
                 max_speed:int = MAX_SPEED):
        self.gpio_in_1 = gpio_in_1
        self.gpio_in_2 = gpio_in_2
        GPIO.setmode(GPIO.BCM)

        self.pidreader = PID_READER(c_gpio_1,c_gpio_2)

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

        self.pidreader.start()
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


    def _set_duty_cycle(self):
        """Sets the duty cycle for the motor"""
        self.pwm_AIN1.ChangeDutyCycle(clamp_speed(self.FORWARD,0,self.MAX_SPEED))
        self.pwm_AIN2.ChangeDutyCycle(clamp_speed(self.BACKWARD,0,self.MAX_SPEED))

    @property
    def current_speed(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD > 0):
            return self.FORWARD
        elif(self.BACKWARD > 0):
            return -self.BACKWARD
        return 0

    def __str__(self) -> str:
        return f"{self.NAME}: {self.current_speed} Angle: {int(self.pidreader.angle)} RPM: {int(self.pidreader.rpm)}"