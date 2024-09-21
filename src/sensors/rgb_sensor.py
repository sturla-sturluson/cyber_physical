import board
from adafruit_tcs34725 import TCS34725
from ..utils import rgb_to_name


class RgbSensor():
    def __init__(self):
        ioc = board.I2C()
        self.sensor = TCS34725(ioc)
        #self.sensor.integration_time = 200
        #self.sensor.gain = 16

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
        return f"Name: {primary_color}\nTemp: {temperature}"

    

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