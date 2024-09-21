from ..sensors import RangeSensor
import time
import os
from ..display import OledDisplay


def run_display_range_sensor(oled_display:OledDisplay):
    range_sensor = RangeSensor()
    while True:
        #os.system('clear')
        value,voltage,distance = range_sensor.get_data()
        print(f"Value: {value}")
        print(f"Voltage: {voltage}")
        print(f"Distance: {distance}")
        display_text = f"Distance: {distance:.2f} cm\nVoltage: {voltage:.2f} V\nValue: {value}"
        oled_display.display_text(display_text)
        time.sleep(1)
