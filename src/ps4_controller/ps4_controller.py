from .ps4_button import PS4Button
import pygame

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