from . import Motor
from .common import clamp_speed
class Motors:
    ERROR_RATE = 0.005 # Change in speed to update the motors
    LAST_FORWARD_MOTION:int = 0
    LAST_TURNING_MOTION:int = 0
    def __init__(self,motor_1_pins:tuple[int,int],motor_2_pins:tuple[int,int]):
        self.motor_1 = Motor(*motor_1_pins,name="Left Motor")
        self.motor_2 = Motor(*motor_2_pins,name="Right Motor")

    def __enter__(self):
        return self
    
    def motor_stop(self):
        self.motor_1.motor_stop()
        self.motor_2.motor_stop()      
        
    def cleanup(self):
        print("Cleaning up Motors")
        self.motor_1.cleanup()
        self.motor_2.cleanup()

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
        
        if(turning_motion > 1 or turning_motion < -1):
            left_engine_speed,right_engine_speed = self._calculate_turning_motion_values(forward_motion,turning_motion)
        self.motor_1.set_speed(left_engine_speed)
        self.motor_2.set_speed(right_engine_speed)

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
        if(abs(turning_motion) < 1):
            return right_motor_speed,left_motor_speed
        turning_adjusted = get_scaled_turning_speed(forward_motion,turning_motion)
        turning_adjusted *= 0.50
        right_motor_speed += turning_adjusted
        left_motor_speed -= turning_adjusted
        right_motor_speed = clamp_speed(right_motor_speed)
        left_motor_speed = clamp_speed(left_motor_speed)
        return right_motor_speed,left_motor_speed
        


    

    def __str__(self) -> str:
        return f"{self.motor_1}\n{self.motor_2}"
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()



def get_scaled_turning_speed(forward_motion:int,turning_motion:int):
    return int(forward_motion * (turning_motion/100))