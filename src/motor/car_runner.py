from . import Motor,Motors
import threading
import os
import asyncio
import datetime as dt


class CurrentSpeed:
    X_SPEED:int
    Y_SPEED:int

    def __init__(self,x_speed:int,y_speed:int):
        self.X_SPEED = x_speed
        self.Y_SPEED = y_speed

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


    current_speed:CurrentSpeed = CurrentSpeed(0,0)
    left_pressed = False
    right_pressed = False
    forward_pressed = False
    back_pressed = False

    left_pressed_time:float = 0
    right_pressed_time:float = 0
    forward_pressed_time:float = 0
    back_pressed_time:float = 0


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
        self.motors.speed_up()

    def speed_down(self):
        """Slows down the motors"""
        self.motors.speed_down()

    def motor_stop(self):
        """Stops the motors"""
        self.motors.motor_stop()    

    def turn_left(self):
        """Turns the car left"""
        # If the current speed is 0 atm, we just turn on the spot
        self.motors.set_speed(0,100)


    def cleanup(self):
        """Cleans up the motors"""
        self.motors.cleanup()

    async def motor_loop(self):
        # start the display loop
        # Launch both motor loops in separate threads
        await self._display_thread()

    def start_display_thread(self):
        """Starts the input thread."""
        threading.Thread(target=self._display_thread, daemon=True).start()


    async def _display_thread(self):
        last_display_time = dt.datetime.now()
        # Only refresh terminal every 0.5 seconds
        while not self.stop_event.is_set():
            if (dt.datetime.now() - last_display_time).total_seconds() > 0.5:
                self._print_screen()
                last_display_time = dt.datetime.now()
            await asyncio.sleep(0.1)   
    

    def _update_speeds(self):
        """This function updates all the values based on how fast it should accelerate etc"""
        if(not self.current_speed and not self._is_y_delta and not self._is_x_delta):
            return




    @property
    def _is_x_delta(self):
        return self.forward_pressed or self.back_pressed
    
    @property
    def _is_y_delta(self):
        return self.left_pressed or self.right_pressed



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