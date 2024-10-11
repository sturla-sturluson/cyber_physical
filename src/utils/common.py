# Common functions for all motors functions
try:
    from ..constants import MAX_SPEED, MIN_SPEED, MAX_DUTY_CYCLE, MIN_DUTY_CYCLE
except ImportError:
    MAX_SPEED = 100
    MIN_SPEED = -100
    MAX_DUTY_CYCLE = 100
    MIN_DUTY_CYCLE = 0


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

def get_clamped_dead_zone(value:float,dead_zone:float,released:int=0,min:int=-1,max:int=1)->float:
    """Returns the value if its outside the dead zone"""
    if abs(value) < dead_zone:
        return released
    return clamp_speed(value,min,max)



def get_heading_difference(current_heading:int,target_heading:int):
    delta = abs(current_heading - target_heading) % 360
    if delta > 180:
        delta = 360 - delta
    return delta

def is_off_course(current_heading:int,target_heading:int, dead_zone:int = 10):
    """Returns True if the car is off course"""
    delta = get_heading_difference(current_heading,target_heading)
    return delta > dead_zone


def get_scaled_number(value:int|float,min:int|float,max:int|float,new_min:int,new_max:int)->int:
    """Scales the value from min to max to new_min to new_max"""
    curr_range_value = max - min
    normalize_range_value = new_max - new_min
    normalized_value = (value - min) / curr_range_value
    return int(new_min + (normalized_value * normalize_range_value))

def heading_test():
    target_heading = 0
    test_headings = [0,10,8,9,68,345,350,355,359,360]
    # header
    first_split = 7
    second_split = 9
    third_split = 13
    fourth_split = 20
    header_str = "Current".ljust(first_split) + " | Target".ljust(second_split) + " | Off Course".ljust(third_split) + " | Difference".ljust(fourth_split)
    print(header_str)
    for i in range(10):
        current_heading =  test_headings[i]
        printstr = f"{current_heading}°".ljust(first_split)
        diff = get_heading_difference(current_heading,target_heading)
        printstr += f" | {target_heading}°".ljust(second_split)
        off_course = is_off_course(current_heading,target_heading)
        printstr += f" | {off_course}".ljust(third_split)
        printstr += f" | {diff}°".ljust(fourth_split)
        print(printstr)
        
def main():
    # scale test
    curr_min = -1
    curr_max = 1
    curr_value = 1
    scale_min,scale_max = 0,100
    print(get_scaled_number(curr_value,curr_min,curr_max,scale_min,scale_max))


if __name__ == '__main__':
    main()