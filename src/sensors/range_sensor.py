import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from .. import utils as UTILS
# from adafruit_ssd1306 import SSD1306_I2C

class RangeSensor:
    def __init__(self,gpio_pin_number = 5):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        i2c = board.I2C()
        cs = digitalio.DigitalInOut(UTILS.get_gpio_pin_number(gpio_pin_number))
        mcp = MCP.MCP3008(spi, cs)
        self.chan0 = AnalogIn(mcp, MCP.P0)

    def get_distance(self):
        return self.chan0.voltage
    
    def get_raw_value(self):
        return self.chan0.value
    
    def __str__(self) -> str:
        return f"Raw ADC Value: {self.chan0.value} ADC Voltage: {self.chan0.voltage:.2f}"

