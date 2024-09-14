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
        r,g,b = self.get_rgb()
        return rgb_to_name(r,g,b)