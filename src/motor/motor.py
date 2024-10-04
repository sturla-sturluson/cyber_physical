import RPi.GPIO as GPIO


class Motor:
    FORWARD = 0
    BACKWARD = 0

    MAX_SPEED = 100
    SPEED_DELTA = 10
    NAME:str = "Motor"

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

        self._set_speed()

    async def motor_loop(self):
        """Motor loop that runs until stop_loop is called"""
        self._print_message("Motor Loop Started")
        self.IS_ON = True

    def stop_loop(self):
        """Stops the motor loop"""
        self.IS_ON = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def cleanup(self):
        """Cleans up the motor"""
        self._print_message("Cleaning up Motor")
        GPIO.cleanup()
        self.motor_stop()

    def motor_stop(self):
        """Stops the motor"""
        self.BACKWARD = 0
        self.FORWARD = 0
        self._print_message("Motor Stopped")
        self._set_speed()      

    def speed_up(self):
        """Speeds up the motor"""
        self._print_message("Speeding Up")
        self.FORWARD,self.BACKWARD = self._get_speeds_from_current_speed(self.SPEED_DELTA)
        # Update ui event
        self._set_speed()
    
    def set_speed(self,value:int):
        """Sets the speed from -100 to 100"""
        if(value > 0):
            self.FORWARD = min(value,self.MAX_SPEED)
            self.BACKWARD = 0
        elif(value < 0):
            self.FORWARD = 0
            self.BACKWARD = min(-value,self.MAX_SPEED)
        else:
            self.FORWARD = 0
            self.BACKWARD = 0
        self._set_speed()
        self._print_message(f"Speed set to {value}")

    def speed_down(self):
        """Speeds down the motor"""
        self._print_message("Speeding Down")
        self.FORWARD,self.BACKWARD = self._get_speeds_from_current_speed(-self.SPEED_DELTA)
        # Update ui event
        self._set_speed()   

    def _set_speed(self):
        self.pwm_AIN1.ChangeDutyCycle(min(self.FORWARD,100))
        self.pwm_AIN2.ChangeDutyCycle(min(self.BACKWARD,100))

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
    
    def _print_message(self,message:str):
        """Prints a message to the console, clearing the screen first"""
        # Flush the buffer
        print("\033c", end="")
        print(f"{self.NAME}: {message}")


    def __str__(self) -> str:
        return f"{self.NAME}: {self.current_speed}"