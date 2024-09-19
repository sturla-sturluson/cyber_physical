import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from .. import utils as UTILS
import json
from ..constants import RANGE_CALIBRATION_FILE_PATH
import numpy as np

DEFAULT_DATA = "base_range.json"

DISTANCES = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]

class RangeSensor:
    VOLTAGE_ARR: list[float] = []
    def __init__(self,gpio_pin_number = 5):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        i2c = board.I2C()
        cs = digitalio.DigitalInOut(UTILS.get_gpio_pin_number(gpio_pin_number))
        mcp = MCP.MCP3008(spi, cs)
        self.chan0 = AnalogIn(mcp, MCP.P0)
        self._load_calibration()

    def _load_calibration(self):
        try:
            with open(RANGE_CALIBRATION_FILE_PATH) as file:
                data = json.load(file)
        except FileNotFoundError:
            with open(DEFAULT_DATA, "r") as file:
                data = json.load(file)
        # 10cm to 150cm
        self.VOLTAGE_ARR = []
        for distance in DISTANCES:
            _,_,voltage = data.get(str(distance),(0,0,0))
            self.VOLTAGE_ARR.append(voltage)


    def get_voltage(self):
        return self.chan0.voltage
    
    def get_raw_value(self):
        return self.chan0.value
    def get_cm_distance(self)->int:
        try:
            #TODO FIx crashing when its too fucking far from sensor
            voltage_arr_measurements = np.ndarray([])
            for i in range(50):
                voltage_arr_measurements = np.append(voltage_arr_measurements,self.get_voltage())
            voltage = UTILS.get_robust_avg(voltage_arr_measurements)
            # Start by finding the index in the voltage array the first one smaller than the current voltage
            index = 0
            for i in range(len(self.VOLTAGE_ARR)):
                if self.VOLTAGE_ARR[i] < voltage:
                    index = i
                    break
            # Now we have the index we can calculate the distance
            if index > len(DISTANCES) - 1:
                return -1
            if index == len(DISTANCES) - 1:
                return DISTANCES[-1]
            # Calculate the distance between the two points
            voltage1 = self.VOLTAGE_ARR[index]
            voltage2 = self.VOLTAGE_ARR[index + 1]
            distance1 = DISTANCES[index]
            distance2 = DISTANCES[index + 1]
            # Calculate the slope
            m = (distance2 - distance1) / (voltage2 - voltage1)
            # Calculate the y intercept
            b = distance1 - m * voltage1
            # Calculate the distance
            distance = m * voltage + b
            return int(distance)
        except RuntimeWarning as e:
            print(e)
            return -1
        except AttributeError as e:
            print(e)
            return -1
    
    def get_data(self) -> tuple[int,float,int]:
        """Returns the raw value and the voltage, and estimated distance in cm.
        Returns:
            tuple[int,float]: (raw value, voltage)
        """
        # TODO implement the distance calculation
        return self.chan0.value, self.chan0.voltage , self.get_cm_distance()
    
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


def distance(voltage:float) -> float:
    runningTotal = 0
    avgFactor = 30
    for x in range(avgFactor):
        v = (voltage / 1023.0) * 5.0
        distance1 = (16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 301.439)
        runningTotal = runningTotal + distance1
    else:
        distance = (runningTotal / avgFactor)

    return distance