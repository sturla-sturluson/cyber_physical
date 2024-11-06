import board
from adafruit_tcs34725 import TCS34725
from ..enums import TapeColor
import threading
import time
from queue import Queue

RED_TAPE = (255,0,0) # 100 0 0    
BLACK_TAPE = (0,0,0) # 45 45 45 
BLUE_TAPE = (0,0,255) # 12 12 12



class RgbSensor():
    """Class to handle the RGB sensor"""
    def __init__(self):
        ioc = board.I2C()
        self.sensor = TCS34725(ioc)
        # Set the integration time to 150ms
        self.sensor.integration_time = 10      

    def get_rgb(self):
        return self.sensor.color_rgb_bytes
    
    def get_color(self):
        return self.sensor.color
    
    def get_color_name(self):
        """Returns the name of the color, that the sensor is currently detecting"""
        #self.sensor.color
        rgb = self.get_rgb()
        primary_color = self.get_primary_color()
        temperature = self.get_color_from_temp()
        return f"Name: {primary_color} Temp: {temperature}"

    

    def get_primary_color(self):
        """Returns the primary color of the given RGB values"""
        r, g, b = self.get_rgb()
        if(r <= 15 and g <= 15 and b <= 15):
            return "Black"
        if(r >= 240 and g >= 240 and b >= 240):
            return "White"
        # Set thresholds for determining primary color
        if r > g and r > b:
            return "Red"
        elif g > r and g > b:
            return "Green"
        elif b > r and b > g:
            return "Blue"
        elif r == g == b:
            return "White"
        elif r == g > b:
            return "Yellow"
        elif r == b > g:
            return "Magenta"
        elif g == b > r:
            return "Cyan"
        else:
            return "Undefined"

    def get_color_from_temp(self):
        # Approximate color ranges based on temperature (in Kelvin)
        temp = self.sensor.color_temperature
        if temp < 2000:
            return "Red"
        elif temp < 3500:
            return "Orange/Yellow"
        elif temp < 5000:
            return "Neutral White"
        elif temp < 6500:
            return "Cool White"
        else:
            return "Bluish"
        
