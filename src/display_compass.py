from .display import OledDisplay
from .sensors import MagneticSensor
from .utils import get_current_time_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
import time
import datetime as dt
from os import system


def run_display_compass(oled_display:OledDisplay):
    magnetic_sensor = MagneticSensor()

    try:
        print("run_display_compass")
        while True:
            deg, x_max, x_min, y_max, y_min,x_avg,y_avg= magnetic_sensor.get_full_data().values()       
            system('clear')
            print(f"Degrees: {deg}\nMAX | MIN | AVG\nX: {x_max:.2f} | {x_min:.2f} | {x_avg:.2f}\nY: {y_max:.2f} | {y_min:.2f} | {y_avg:.2f}")
            nsew_string = magnetic_sensor.get_orientation_string(deg)
            oled_display.display_text(nsew_string)
            print(nsew_string)
            time.sleep(0.5)
    except KeyboardInterrupt:
        oled_display.clear()
    except Exception as e:
        print(e)
        oled_display.clear()
    finally:
        oled_display.cleanup()