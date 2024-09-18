from ..sensors import RangeSensor
import time
import os
from ..display import OledDisplay


def run_display_range_sensor(oled_display:OledDisplay):
    range_sensor = RangeSensor()
    input("Press enter to start the compass")
    try:
        print("run_display_compass")
        while True:
            os.system('clear')
            value,voltage,distance = range_sensor.get_data()
            print(f"Value: {value}")
            print(f"Voltage: {voltage}")
            print(f"Distance: {distance}")
            display_text = f"Distance: {distance} cm\nVoltage: {voltage} V\nValue: {value}"
            oled_display.display_text(display_text)
            time.sleep(0.5)
    except KeyboardInterrupt:
        oled_display.clear()
    except Exception as e:
        print(e)
        oled_display.clear()
    finally:
        oled_display.cleanup()
