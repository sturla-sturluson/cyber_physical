from ..display import OledDisplay
from ..sensors import MagneticSensor
from ..utils import get_current_time_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
import time
import datetime as dt
from ..led import Led
from os import system


def run_display_compass(oled_display:OledDisplay):
    magnetic_sensor = MagneticSensor()
    led = Led(22)
    input("Press enter to start the compass")
    try:
        print("run_display_compass")
        while True:
            system('clear')
            degrees = magnetic_sensor.get_orientation()
            nsew_string = magnetic_sensor.get_NSEW_string(degrees)
            oled_display.display_text(nsew_string)
            print(nsew_string)
            if(nsew_string == "N"):
                led.turn_on()
            else:
                led.turn_off()
            time.sleep(0.5)
    except KeyboardInterrupt:
        oled_display.clear()
    except Exception as e:
        print(e)
        oled_display.clear()
    finally:
        oled_display.cleanup()
        led.cleanup()