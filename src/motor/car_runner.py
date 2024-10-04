from . import Motor,Motors
import threading
import os
import asyncio
import datetime as dt
import math


class CurrentSpeed:
    X_SPEED:int
    Y_SPEED:int

    def __init__(self,x_speed:int,y_speed:int):
        self.X_SPEED = x_speed
        self.Y_SPEED = y_speed

    def set_x_speed(self,speed:int):
        """Sets the x speed"""
        self.X_SPEED = speed

    def set_y_speed(self,speed:int):
        """Sets the y speed"""
        self.Y_SPEED = speed

    @property
    def speeds(self):
        """Returns the speeds as a tuple"""
        return (self.X_SPEED,self.Y_SPEED)
    
    def __bool__(self):
        """Only return false if both speeds are 0"""
        return self.X_SPEED != 0 or self.Y_SPEED != 0

class CarRunner():
    MAX_SPEED = 100
    MIN_SPEED = -100
    MAX_TURN = 100
    MIN_TURN = -100
    # Time to go from 0 to max speed x-axis
    ZERO_TO_MAX:float = 4
    SLOW_DOWN_X_TIME:float = 3

    # Time to go from 0 to max speed y-axis
    ZERO_TO_MAX_Y:float = 4
    SLOW_DOWN_Y_TIME:float = 1


    current_speed:CurrentSpeed = CurrentSpeed(0,0)
    last_speed_update:dt.datetime = dt.datetime.now()

    left_pressed = False
    right_pressed = False
    forward_pressed = False
    back_pressed = False

    key_timeout = 0.15

    left_pressed_time = dt.datetime.now() - dt.timedelta(seconds=1)
    right_pressed_time = dt.datetime.now() - dt.timedelta(seconds=1)
    forward_pressed_time = dt.datetime.now() - dt.timedelta(seconds=1)
    back_pressed_time = dt.datetime.now() - dt.timedelta(seconds=1)

    def __init__(self,motor_1_pins:tuple[int,int],motor_2_pins:tuple[int,int]):
        self.motors = Motors(motor_1_pins,motor_2_pins)
        # Create a stop event and ui event
        self.stop_event = threading.Event()

    def shut_down(self):
        """Shuts down the car"""
        self.motor_stop()
        self.stop_event.set()
        self.cleanup()
    
    def speed_up(self):
        """Speeds up the motors"""
        x_speed = self.current_speed.X_SPEED + 10
        x_speed = min(x_speed,self.MAX_SPEED)
        self.current_speed.set_x_speed(x_speed)
        self.motors.set_speed(x_speed)

    def speed_down(self):
        """Slows down the motors"""
        x_speed = self.current_speed.X_SPEED - 10
        x_speed = max(x_speed,self.MIN_SPEED)
        self.current_speed.set_x_speed(x_speed)
        self.motors.set_speed(x_speed)

    def turn_right(self):
        """Turns the car right"""
        # If the current speed is 0 atm, we just turn on the spot
        self.motors.set_speed(self.current_speed.X_SPEED,int(self.current_speed.X_SPEED * 0.5))

    def turn_left(self):
        """Turns the car left"""
        # If the current speed is 0 atm, we just turn on the spot
        self.motors.set_speed(int(self.current_speed.X_SPEED * 0.5),self.current_speed.X_SPEED)


    def motor_stop(self):
        """Stops the motors"""
        self.motors.motor_stop()    
        self.set_wasd(False,False,False,False)


    def set_wasd(self,forward:bool,back:bool,left:bool,right:bool):
        """Sets the wasd keys"""
        # If the user is pressing both keys, we put both to false
        if(forward and back):
            self.forward_pressed = False
            self.back_pressed = False
        elif(forward):
            self.forward_pressed = True
            self.forward_pressed_time = dt.datetime.now()
        elif(back):
            self.back_pressed = True
            self.back_pressed_time = dt.datetime.now()
        if(left and right):
            self.left_pressed = False
            self.right_pressed = False
        elif(left):
            self.left_pressed = True
            self.left_pressed_time = dt.datetime.now()
        elif(right):
            self.right_pressed = True
            self.right_pressed_time = dt.datetime.now()



    def cleanup(self):
        """Cleans up the motors"""
        self.motors.cleanup()

    async def motor_loop(self):
        # start the display loop
        # Launch both motor loops in separate threads
        await self._display_thread()

    async def _display_thread(self):
        last_display_time = dt.datetime.now()
        # Only refresh terminal every 0.5 seconds
        while not self.stop_event.is_set():
            if (dt.datetime.now() - last_display_time).total_seconds() > 0.5:
                self._print_screen()
                last_display_time = dt.datetime.now()
            #self._update_speeds()
            await asyncio.sleep(0.1)   
            os.system('clear')
            self._update_key_pressed()
            print(f"W: {self.forward_pressed} S: {self.back_pressed} A: {self.left_pressed} D: {self.right_pressed}")
    
    def _update_key_pressed(self):
        """Gonna check if the keys have timed out"""
        curr_time = dt.datetime.now()
        if(self.forward_pressed and (curr_time - self.forward_pressed_time).total_seconds() > self.key_timeout):
            self.forward_pressed = False
        if(self.back_pressed and (curr_time - self.back_pressed_time).total_seconds() > self.key_timeout):
            self.back_pressed = False
        if(self.left_pressed and (curr_time - self.left_pressed_time).total_seconds() > self.key_timeout):
            self.left_pressed = False
        if(self.right_pressed and (curr_time - self.right_pressed_time).total_seconds() > self.key_timeout):
            self.right_pressed = False


    def _update_speeds(self):
        """This function updates all the values based on how fast it should accelerate etc"""
        self._update_key_pressed()
        previous_time = self.last_speed_update
        self.last_speed_update = dt.datetime.now()
        time_passed_in_milliseconds = int((self.last_speed_update - previous_time).total_seconds() * 1000)
        if(not self.current_speed and not self._is_y_delta and not self._is_x_delta):
            return
        ###################
        # X-Delta
        ###################
        # Now if the user is not doing x-delta but the car is moving, move it down
        if(not self._is_x_delta and self.current_speed.X_SPEED):
            # Since we are slowing down, the target speed is 0
            new_speed = self._get_time_adjusted_speed(
                original_speed=self.current_speed.X_SPEED,
                target_speed=0, # We are slowing down
                time_for_min_to_max=self.SLOW_DOWN_X_TIME,
                time_passed_milliseconds=time_passed_in_milliseconds
            )
            self.current_speed.set_x_speed(new_speed)

        elif(self.forward_pressed):
            new_speed = self._get_time_adjusted_speed(
                original_speed=self.current_speed.X_SPEED,
                target_speed=self.MAX_SPEED, # We are speeding up
                time_for_min_to_max=self.ZERO_TO_MAX,
                time_passed_milliseconds=time_passed_in_milliseconds
            )
            self.current_speed.set_y_speed(new_speed)
        elif(self.back_pressed):
            new_speed = self._get_time_adjusted_speed(
                original_speed=self.current_speed.X_SPEED,
                target_speed=self.MIN_SPEED, # We are speeding up
                time_for_min_to_max=self.ZERO_TO_MAX,
                time_passed_milliseconds=time_passed_in_milliseconds
            )
            self.current_speed.set_y_speed(new_speed)
        ###################
        # Y-Delta
        ###################
        # Now if the user is not turning the car, always move towards 0
        if(not self._is_y_delta and self.current_speed.Y_SPEED):
            # Since we are slowing down, the target speed is 0
            new_speed = self._get_time_adjusted_speed(
                original_speed=self.current_speed.Y_SPEED,
                target_speed=0, # We are slowing down
                time_for_min_to_max=self.SLOW_DOWN_Y_TIME,
                time_passed_milliseconds=time_passed_in_milliseconds
            )
            self.current_speed.set_y_speed(new_speed)
        elif(self.left_pressed):
            new_speed = self._get_time_adjusted_speed(
                original_speed=self.current_speed.Y_SPEED,
                target_speed=self.MAX_SPEED, # We are speeding up
                time_for_min_to_max=self.ZERO_TO_MAX_Y,
                time_passed_milliseconds=time_passed_in_milliseconds
            )
            self.current_speed.set_x_speed(new_speed)
        elif(self.right_pressed):
            new_speed = self._get_time_adjusted_speed(
                original_speed=self.current_speed.Y_SPEED,
                target_speed=self.MIN_SPEED, # We are speeding up
                time_for_min_to_max=self.ZERO_TO_MAX_Y,
                time_passed_milliseconds=time_passed_in_milliseconds
            )
            self.current_speed.set_x_speed(new_speed)

        # Set the speeds
        self._set_speeds()


    def _set_speeds(self):
        """Sets the speeds to the motors"""
        motor_1_speed = self.current_speed.X_SPEED
        motor_2_speed = self.current_speed.X_SPEED
        # Now lets adjust the speeds wether or not its turning 
        # Turning Right
        if(self.current_speed.Y_SPEED < 0):
            motor_1_speed = min(self.current_speed.X_SPEED + self.current_speed.Y_SPEED,self.MAX_SPEED)
            motor_2_speed = max(self.current_speed.X_SPEED - self.current_speed.Y_SPEED,self.MIN_SPEED)
        elif(self.current_speed.Y_SPEED > 0):
            motor_1_speed = max(self.current_speed.X_SPEED - self.current_speed.Y_SPEED,self.MIN_SPEED)
            motor_2_speed = min(self.current_speed.X_SPEED + self.current_speed.Y_SPEED,self.MAX_SPEED)

        self.motors.set_speed(motor_1_speed,motor_2_speed)



    @property
    def _is_x_delta(self):
        return self.forward_pressed or self.back_pressed
    
    @property
    def _is_y_delta(self):
        return self.left_pressed or self.right_pressed


    def _get_time_adjusted_speed(
            self,
            original_speed:int,
            target_speed:int,
            time_passed_milliseconds:int,
            time_for_min_to_max:float,
            )->int:
        """This function takes the current speed and calculates the new speed based on how long was passed"""
        max_speed = self.MAX_SPEED
        min_speed = self.MIN_SPEED


        new_speed = original_speed
        # If new_speed is already equal to max_speed or min_speed, we return it
        if(original_speed == max_speed or original_speed == min_speed or original_speed == target_speed):
            return new_speed
        # Calculate the range 
        speed_range = max_speed - min_speed
        # Calculate the speed per millisecond
        speed_per_millisecond = speed_range / time_for_min_to_max
        # Check if its a positive or negative delta
        if(original_speed < target_speed):
            new_speed = original_speed + (time_passed_milliseconds * speed_per_millisecond)
        else:
            new_speed = original_speed - (time_passed_milliseconds * speed_per_millisecond)
        # Clamp the speed in between 
        new_speed = min(max_speed,max(min_speed,new_speed))
        return int(new_speed)






    def _print_screen(self):
        """Prints the screen"""
        os.system('clear')
        # Print the current time
        print(dt.datetime.now().strftime("%H:%M:%S"))
        motors_string = str(self.motors).split("\n")
        print(motors_string[0])
        print(motors_string[1])

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()


