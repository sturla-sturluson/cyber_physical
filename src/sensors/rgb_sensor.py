import board
from adafruit_tcs34725 import TCS34725


class RgbSensor():
    def __init__(self):
        ioc = board.I2C()
        self.sensor = TCS34725(ioc)
        self.sensor.integration_time = 200
        self.sensor.gain = 16

    def get_rgb(self):
        return self.sensor.color_rgb_bytes