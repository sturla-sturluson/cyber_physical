import time
import board
import adafruit_mpl3115a2 as mpl


class Mpl_Sensor:
    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = mpl.MPL3115A2(self.i2c)
        
    def get_pressure(self):
        return self.sensor.pressure
    
    def get_temperature(self):
        return self.sensor.temperature
    
    def get_altitude(self):
        return self.sensor.altitude