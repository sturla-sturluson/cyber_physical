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
    
    def get_data(self) -> tuple[int,float]:
        """Returns the raw value and the voltage
        Returns:
            tuple[int,float]: (raw value, voltage)
        """
        return self.chan0.value, self.chan0.voltage
    
    def __str__(self) -> str:
        return f"Raw ADC Value: {self.chan0.value} ADC Voltage: {self.chan0.voltage:.2f}"



def remap_range(value: int, left_min: int, left_max: int, right_min: int, right_max: int) -> int:
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))


def get_distance_calc(k:float,voltage:float) -> float:
    """
        1/D = k*V
    """
    if(voltage == 0):
        return 0.0001   # to avoid division by zero
    distance = 1 / (k * voltage)
    return distance