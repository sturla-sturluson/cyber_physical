import time
import board
import pwmio
from adafruit_motor.servo import Servo
import RPi.GPIO as GPIO
import threading
import asyncio
import os
import datetime as dt


class Motor:
    FORWARD = 0
    BACKWARD = 0

    MAX_SPEED = 100
    SPEED_DELTA = 10


    def __init__(self,gpio_in_1:int,gpio_in_2:int): 
        self.gpio_in_1 = gpio_in_1
        self.gpio_in_2 = gpio_in_2
        GPIO.setmode(GPIO.BCM)
        nSLEEP = 25  # Connect nSLEEP to GPIO 25 or directly to 3.3V/5V

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

        self.stop_event = threading.Event()
        self._update_ui_event = asyncio.Event()



    async def _motor_loop(self):
        while not self.stop_event.is_set():
            os.system('clear')
            # Print the current time
            print(dt.datetime.now().strftime("%H:%M:%S"))
            print("Current Speed: ", self.current_speed)
            self.pwm_AIN1.ChangeDutyCycle(min(self.FORWARD,100))
            self.pwm_AIN2.ChangeDutyCycle(min(self.BACKWARD,100))
            time.sleep(0.1)



    async def motor_loop(self):
        self.IS_ON = True
        await self._motor_loop()

    def stop_loop(self):
        self.IS_ON = False
        self.stop_event.set()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cleaning up Motor")
        GPIO.cleanup()
        self.motor_stop()

    def motor_stop(self):
        self.BACKWARD = 0
        self.FORWARD = 0
        self._update_ui_event.set()
        print("Motor Stopped")

        

    def speed_up(self):
        self.FORWARD,self.BACKWARD = self._get_speeds_from_current_speed(self.SPEED_DELTA)
        # Update ui event
        self._update_ui_event.set()

    def speed_down(self):
        self.FORWARD,self.BACKWARD = self._get_speeds_from_current_speed(-self.SPEED_DELTA)
        # Update ui event
        self._update_ui_event.set()
    
    @property
    def current_speed(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD > 0):
            return self.FORWARD
        elif(self.BACKWARD > 0):
            return -self.BACKWARD
        return 0

    def _get_speeds_from_current_speed(self,delta:int):
        """Returns the forward and backward speeds from the current speed"""
        new_speed = self.current_speed + delta
        if(new_speed >= 0):
            return min(new_speed,self.MAX_SPEED),0
        return 0,min(-new_speed,self.MAX_SPEED)