from . import Motor

class Motors:
    def __init__(self,motor_1_pins:tuple[int,int],motor_2_pins:tuple[int,int]):
        self.motor_1 = Motor(*motor_1_pins,name="Left Motor")
        self.motor_2 = Motor(*motor_2_pins,name="Right Motor")

        self.current_speed = 0

    def __enter__(self):
        return self
    
    def speed_up(self):
        self.motor_1.speed_up()
        self.motor_2.speed_up()

    def speed_down(self):
        self.motor_1.speed_down()
        self.motor_2.speed_down()

    def motor_stop(self):
        self.motor_1.motor_stop()
        self.motor_2.motor_stop()      

    # Overload the set_speed method
    def set_speed(self,speed:int,speed_two:int=None): # type: ignore
        if(speed_two):
            self.motor_1.set_speed(speed)
            self.motor_2.set_speed(speed_two)
            return
        self.motor_1.set_speed(speed)
        self.motor_2.set_speed(speed)

    def cleanup(self):
        print("Cleaning up Motors")
        self.motor_1.cleanup()
        self.motor_2.cleanup()

    def __str__(self) -> str:
        return f"{self.motor_1}\n{self.motor_2}"
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()
        