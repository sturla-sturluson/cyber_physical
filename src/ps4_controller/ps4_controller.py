from .ps4_button import PS4Button
import pygame
from ..enums import ButtonType

class PS4ControllerInput:
    DEAD_ZONE:float

    PS_TYPES_BUTTONS = [pygame.JOYBUTTONDOWN,pygame.JOYBUTTONUP]
    PS_TYPES_HATS = [pygame.JOYHATMOTION]

    PS_TYPES = [pygame.JOYAXISMOTION,*PS_TYPES_BUTTONS,*PS_TYPES_HATS]


    def __init__(self,joy_stick:pygame.joystick.JoystickType,dead_zone:float = 0.1):
        self.joy_stick = joy_stick
        self.DEAD_ZONE = dead_zone

    def get_values_from_game(self,accelerate:PS4Button,brake:PS4Button,reverse:PS4Button,steer:PS4Button)->tuple[int,int]:
        """Returns the values for the car based on the game state"""
        # Fetching the values from all the buttons and axis
        brake.set_value(self.joy_stick.get_button(brake.id),self.DEAD_ZONE)
        accelerate.set_value(self.joy_stick.get_axis(accelerate.id),self.DEAD_ZONE)
        reverse.set_value(self.joy_stick.get_axis(reverse.id),self.DEAD_ZONE)
        steer.set_value(self.joy_stick.get_axis(steer.id),self.DEAD_ZONE)

        # If we are braking, we return 0,0
        if brake.is_pressed:
            return 0,0
        # If we are accelerating and reversing at the same time, we return 0,0
        if accelerate.is_pressed and reverse.is_pressed:
            return 0,0
        # If we are accelerating, we return the acceleration value
        # However, since that value is from -1 to 1, we need to +1 and divide by 2 and multiply by 100
        # to get a value from 0 to 100
        forward_motion = 0
        if accelerate.is_pressed:
            forward_motion = accelerate.get_normalized_value()
        elif reverse.is_pressed:
            forward_motion = -reverse.get_normalized_value()
        # If we are steering, we return the steering value
        turning_motion = steer.get_normalized_value(-100,100)
        return forward_motion,turning_motion
    
    def set_value(self,button:PS4Button)->None:
        """Returns the value of the button"""
        value = 0
        if(button.type == ButtonType.BUTTON):
            value = self.joy_stick.get_button(button.id)
        elif(button.type == ButtonType.AXIS):
            value = self.joy_stick.get_axis(button.id)
        # elif button.type == ButtonType.HAT:
        #     value = self.joy_stick.get_hat(button.id)
        button.set_value(value,self.DEAD_ZONE)
