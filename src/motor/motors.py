from . import Motor
from ..utils import clamp_speed
from ..constants import SLEEP_PIN,AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN
import RPi.GPIO as GPIO

class Motors:
    ERROR_RATE = 0.005 # Change in speed to update the motors
    LAST_FORWARD_MOTION:int = 0
    LAST_TURNING_MOTION:int = 0
    def __init__(self):
        self._turn_motor_controller_on()
        left_pins = (BIN1_PIN,BIN2_PIN)
        right_pins = (AIN1_PIN,AIN2_PIN)
        self.left_motor = Motor(*left_pins,name="Left Motor")
        self.right_motor = Motor(*right_pins,name="Right Motor")

    def _turn_motor_controller_on(self):
        """Setting power to high to turn on the motor controller"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SLEEP_PIN, GPIO.OUT) 
        GPIO.output(SLEEP_PIN, GPIO.HIGH)

    def motor_stop(self):
        """Stops the motors"""
        self.left_motor.motor_stop()
        self.right_motor.motor_stop()      
        
    def cleanup(self):
        print("Cleaning up Motors")
        self.left_motor.cleanup()
        self.right_motor.cleanup()

    # Overload the set_speed method
    def set_speed(self,forward_motion:int,turning_motion:int = 0):
        """Sets the speed of the car
        Forward motion from -100 to 100
        Turning can go from -100 to 100
        """
        if not self._check_update(forward_motion,turning_motion):
            return
        self.LAST_FORWARD_MOTION,self.LAST_TURNING_MOTION = forward_motion,turning_motion
        left_engine_speed,right_engine_speed = forward_motion,forward_motion
        
        if(abs(turning_motion) > 1):
            left_engine_speed,right_engine_speed = self._calculate_turning_motion_values(forward_motion,turning_motion)
        self.left_motor.set_speed(left_engine_speed)
        self.right_motor.set_speed(right_engine_speed)

    def _check_update(self,forward_motion:int,turning_motion:int):
        """Checks if we need to update the motors"""
        return (
            abs(forward_motion - self.LAST_FORWARD_MOTION) > self.ERROR_RATE or 
            abs(turning_motion - self.LAST_TURNING_MOTION) > self.ERROR_RATE)

    def _calculate_turning_motion_values(self,forward_motion:int,turning_motion:int):
        """Calculates the turning motion values for the car"""
        if(forward_motion == 0): # If the car is not moving forward, then we don't turn
            return 0,0
        # If we are going forward, and turning motion is positive, we are turning right
        # If we are going backwards , turning motion is positive we are also turning right
        # This way we know if turning right, always lower the right motor speed and vice versa
        right_motor_speed,left_motor_speed = forward_motion,forward_motion
        if(abs(turning_motion) < 1): # If turning motion is very low, then we don't turn
            return right_motor_speed,left_motor_speed
        turning_adjusted = self._get_scaled_turning_speed(forward_motion,turning_motion) * 0.75
        right_motor_speed += turning_adjusted # If we are turning right, we need to lower the right motor speed
        left_motor_speed -= turning_adjusted  # Same for left motor
        return clamp_speed(right_motor_speed),clamp_speed(left_motor_speed)
           
    @classmethod
    def _get_scaled_turning_speed(cls,forward_motion:int,turning_motion:int):
        """Scales the turning motion based on the forward motion"""
        return int(forward_motion * (turning_motion/100))

    def __str__(self) -> str:
        return f"{self.left_motor}\n{self.right_motor}"
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()


