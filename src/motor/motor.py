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


    def _input_thread(self):
        while True:
            os.system('clear')
            print("Current Speed: ", self.current_speed)
            timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Current Time: ", timestamp)
            response = input("(W) Speed up, (S) Slow down, (<Space>) Stop, (Q) Quit: ").lower()
            if(len(response) == 0):
                continue
            if(response[0] == " "):
                self.motor_stop()
            elif(response[0] == "w"):
                self.speed_up()
            elif(response[0] == "s"):
                self.speed_down()
            elif(response[0] == "q"):
                break
            self._update_ui_event.set()
        self.stop_event.set()

    def _start_input_thread(self):
        """Starts the input thread."""
        threading.Thread(target=self._input_thread, daemon=True).start()

    async def motor_loop(self):
        """Calibrates the compass"""
        # Start the input thread to handle user input without blocking
        self._start_input_thread()

        # Start the calibration loop asynchronously
        await self._motor_loop()

    async def _motor_loop(self):
        while not self.stop_event.is_set():
            if(self.FORWARD > 0):
                self.pwm_AIN1.ChangeDutyCycle(self.FORWARD)
                self.pwm_AIN2.ChangeDutyCycle(0)
            elif(self.BACKWARD > 0):
                self.pwm_AIN1.ChangeDutyCycle(0)
                self.pwm_AIN2.ChangeDutyCycle(self.BACKWARD)
            # wait for 0.1 seconds
            await asyncio.sleep(0.1)
        self.motor_stop()


    def motor_stop(self):
        self.BACKWARD = 0
        self.FORWARD = 0
        self.pwm_AIN1.ChangeDutyCycle(0)
        self.pwm_AIN2.ChangeDutyCycle(0)


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cleaning up Motor")
        self.motor_stop()
        GPIO.cleanup()

    def motor_forward(self, speed:int):
        self.BACKWARD = 0
        self.FORWARD = speed

    def motor_backward(self, speed:int):
        self.BACKWARD = speed
        self.FORWARD = 0


    def speed_up(self):
        current_speed = self.current_speed
        if(current_speed > 0):
            self.FORWARD = self.get_clamped_speed(current_speed + self.SPEED_DELTA)
        elif(current_speed < 0):
            self.BACKWARD = self.get_clamped_speed(current_speed - self.SPEED_DELTA)
        # Update ui event

    def speed_down(self):
        current_speed = self.current_speed
        if(current_speed > 0):
            self.FORWARD = self.get_clamped_speed(current_speed - self.SPEED_DELTA)
        elif(current_speed < 0):
            self.BACKWARD = self.get_clamped_speed(current_speed + self.SPEED_DELTA)
        # Update ui event
    
    @property
    def current_speed(self):
        """Returns current speed from -100 to 100"""
        if(self.FORWARD > 0):
            return self.FORWARD
        elif(self.BACKWARD > 0):
            return -self.BACKWARD
        return 0


    @classmethod
    def get_clamped_speed(cls,speed:int):
        if(speed > cls.MAX_SPEED):
            return cls.MAX_SPEED
        elif(speed < 0):
            return 0
        return speed