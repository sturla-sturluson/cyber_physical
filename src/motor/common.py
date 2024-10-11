# Common functions for all motors functions

from ..constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE


def clamp_speed(speed:int|float,lower:int=MIN_SPEED,upper:int=MAX_SPEED)->int:
    """Clamps the speed value between the MAX_SPEED and MIN_SPEED"""
    speed = int(speed)
    return max(min(speed,upper),lower)

def get_duty_cycle_values_from_speed(target_speed:int)->tuple[int,int]:
    """Returns the duty cycle values for the motor based on the target speed
    Speed is from -100 to 100
    Duty cycle is from 0 to 100
    """
    target_speed = clamp_speed(target_speed)
    if(target_speed == 0):
        return (0,0)
    if(target_speed > 0):
        return (target_speed,0)
    return (0,-target_speed)

def get_clamped_dead_zone(value:float,dead_zone:float,released:int=0)-> float:
    """Returns the value if its outside the dead zone"""
    if abs(value) < dead_zone:
        return released
    return clamp_speed(value,-1,1)