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
            return int(volt_to_cm(voltage))
        
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



def volt_to_cm(voltage:float):  
    return 46.371 * voltage**6 - 462.87 * voltage**5 + 1878.4 * voltage**4 - 3975.3 * voltage**3 + 4655.9 * voltage**2 - 2916.3 * voltage + 828.41