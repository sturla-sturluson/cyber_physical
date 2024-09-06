from src.oled_display import OledDisplay
from src.magnetic_sensor import MagneticSensor
import time
from os import system


def main():
    oled_display = OledDisplay()
    magnetic_sensor = MagneticSensor()
    try:
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


if __name__ == '__main__':
    main()