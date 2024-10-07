import pygame
import os

def clamp_speed(speed:int|float,lower:int|float,upper:int|float)->int|float:
    """Clamps the speed value between the MAX_SPEED and MIN_SPEED"""
    return max(min(speed,upper),lower)

ps4_buttons = {
    0: "X",
    1: "Circle",
    2: "Square",
    3: "Triangle",
    # D-pad
    11: "Up",
    12: "Down",
    13: "Left",
    14: "Right",
    # L1, R1, L2, R2
    9: "L1",
    10: "R1",
    # joystick buttons
    7: "L3",
    8: "R3",
    # Share, Options, PS
    4: "Share",
    6: "Options",
    5: "PS",
    
}

ps4_axis = {
    0: "Left Stick X",
    1: "Left Stick Y",
    2: "Right Stick X",
    3: "Right Stick Y",
    4: "L2", # -1 Neutral , 1 Fully pressed
    5: "R2", # -1 Neutral , 1 Fully pressed
}

def get_clamped_dead_zone(value:float,dead_zone:float,released:int=0)-> float:
    """Returns the value if its outside the dead zone"""
    if abs(value) < dead_zone:
        return released
    return clamp_speed(value,-1,1)

class PS4Button:
    type:str   # Button or Axis
    id:int     # Button or Axis id
    value:int|float  # Value of the button or axis
    # Button or Axis name
    name:str
    # Min and Max values for the axis
    released:int
    min:int
    max:int
    def __init__(self,type:str,id:int,name:str,released:int=0,min:int=0,max:int=1):
        self.type = type
        self.id = id
        self.value = released
        self.name = name
        self.released = released
        self.min = min
        self.max = max
    def __str__(self):
        if(self.type == "Button"):
            return f"{self.name} : {self.value>0 if 'Pressed' else 'Released'}"
        return f"{self.name} : {self.value}"
    
    def set_value(self,value:int|float,dead_zone:float):
        self.value = get_clamped_dead_zone(value,dead_zone,self.released)
    
    @property
    def is_pressed(self):
        return self.value != self.released
    
    def get_normalized_value(self,min:int=0,max:int=100)->int:
        """Returns the value normalized between min and max"""
        curr_range_value = self.max - self.min
        normalize_range_value = max - min
        normalized_value = (self.value - self.min) / curr_range_value
        return int(min + (normalized_value * normalize_range_value))

    


class PS4ControllerInput:
    ACCELERATE_BTN:PS4Button
    REVERSE_BTN:PS4Button
    STEER_BTN:PS4Button
    BRAKE_BTN:PS4Button
    DEAD_ZONE:float

    AXIS_IDS:list[int]
    BUTTON_IDS:list[int]

    PS_TYPES_BUTTONS = [pygame.JOYBUTTONDOWN,pygame.JOYBUTTONUP]

    PS_TYPES = [pygame.JOYAXISMOTION,*PS_TYPES_BUTTONS]


    def __init__(self,
                 accelerate_btn:PS4Button,
                    reverse_btn:PS4Button,
                    steer_btn:PS4Button,
                    brake_btn:PS4Button,
                    dead_zone:float = 0.10):

        self.ACCELERATE_BTN = accelerate_btn
        self.REVERSE_BTN = reverse_btn
        self.STEER_BTN = steer_btn
        self.BRAKE_BTN = brake_btn
        self.DEAD_ZONE = dead_zone

        self.ALL_BTNS = [self.ACCELERATE_BTN,self.REVERSE_BTN,self.STEER_BTN,self.BRAKE_BTN]
        self.AXIS_IDS = [button.id for button in self.ALL_BTNS if button.type == "Axis"]
        self.BUTTON_IDS = [button.id for button in self.ALL_BTNS if button.type == "Button"]

    def get_values_from_game(self,joy_stick:pygame.joystick.JoystickType)->tuple[int,int]:
        """Returns the values for the car based on the game state"""
        # Fetching the values from all the buttons and axis
        self.BRAKE_BTN.set_value(joy_stick.get_button(self.BRAKE_BTN.id),self.DEAD_ZONE)
        self.ACCELERATE_BTN.set_value(joy_stick.get_axis(self.ACCELERATE_BTN.id),self.DEAD_ZONE)
        self.REVERSE_BTN.set_value(joy_stick.get_axis(self.REVERSE_BTN.id),self.DEAD_ZONE)
        self.STEER_BTN.set_value(joy_stick.get_axis(self.STEER_BTN.id),self.DEAD_ZONE)

        # If we are braking, we return 0,0
        if self.BRAKE_BTN.is_pressed:
            return 0,0
        # If we are accelerating and reversing at the same time, we return 0,0
        if self.ACCELERATE_BTN.is_pressed and self.REVERSE_BTN.is_pressed:
            return 0,0
        # If we are accelerating, we return the acceleration value
        # However, since that value is from -1 to 1, we need to +1 and divide by 2 and multiply by 100
        # to get a value from 0 to 100
        forward_motion = 0
        if self.ACCELERATE_BTN.is_pressed:
            forward_motion = self.ACCELERATE_BTN.get_normalized_value()
        elif self.REVERSE_BTN.is_pressed:
            forward_motion = -self.REVERSE_BTN.get_normalized_value()
        # If we are steering, we return the steering value
        turning_motion = self.STEER_BTN.get_normalized_value(-100,100)
        return forward_motion,turning_motion



def main():
    # Init pygame
    pygame.init()
    window = pygame.display.set_mode((800, 600))

    running = True
    fps = 10
    clock = pygame.time.Clock()

    # Init joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick : {joystick.get_name()}")


    
    ps_4_axis_dead_zone = 0.10
    l2_button = PS4Button("Axis",id=4,name="L2",released=-1,min=-1,max=1)
    r2_button = PS4Button("Axis",id=5,name="R2",released=-1,min=-1,max=1)
    left_joystick_x_axis = PS4Button("Axis",id=0,name="Left Stick X",released=0,min=-1,max=1)
    square_button = PS4Button("Button",id=2,name="Square",released=0)

    ps4_controller = PS4ControllerInput(r2_button,l2_button,left_joystick_x_axis,square_button,ps_4_axis_dead_zone)

    forward_motion,turning_motion = 0,0
    # Game loop
    while running:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Going to fetch the status of the controller
        forward_motion,turning_motion = ps4_controller.get_values_from_game(joystick)

        os.system('clear')
        print(forward_motion,turning_motion)
            





if __name__ == '__main__':
    main()