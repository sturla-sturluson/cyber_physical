from ..display import OledDisplay
from ..sensors import MagneticSensor
import time
from ..led import Led
from os import system
from ..utils import X_Y_Map


def run_display_compass(oled_display:OledDisplay):
    magnetic_sensor = MagneticSensor()
    led = Led(26)
    x_y_map = X_Y_Map(15)
    input("Press enter to start the compass")
    try:
        print("run_display_compass")
        while True:
            system('clear')
            orientation, (x, y), nsew_string = magnetic_sensor.get_data()
            _orientation, (x_2,y_2), _ = magnetic_sensor.get_non_translate_data()
            x_y_map.add_cord(x,y)
            x_y_map.add_cord(x_2,y_2,2)

            oled_display.display_text(nsew_string)
            print(f"Orientation: {orientation}°")
            print(f"X: {x} Y: {y}")
            print(nsew_string)
            print(x_y_map.get_scaled_map(10))
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