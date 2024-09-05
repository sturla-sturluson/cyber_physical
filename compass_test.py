from src.oled_display import OledDisplay
from src.magnetic_sensor import MagneticSensor
import time
from os import system


def main():
    oled_display = OledDisplay()
    magnetic_sensor = MagneticSensor()
    try:
        while True:
            x,y,z = magnetic_sensor._get_micro_teslas()
            orientation_1 = magnetic_sensor._calculate_orientation(x,y)

            orientation_2 = magnetic_sensor._calculate_orientation(y,x)

            orientation_3 = magnetic_sensor._calculate_orientation(x,z)

            orientation_1_full = f"X: {x:1f}, Y: {y:1f}, Z: {z:1f}, Orientation (x,y): {int(orientation_1)}"

            orientation_2_full = f"X: {x:1f}, Y: {y:1f}, Z: {z:1f}, Orientation (y,x): {int(orientation_2)}"

            orientation_3_full = f"X: {x:1f}, Y: {y:1f}, Z: {z:1f}, Orientation (x,z): {int(orientation_3)}"
            


            #orientation = magnetic_sensor.get_orientation_in_degrees()
            #print(orientation)
            system('clear')
            print(orientation_1_full)
            print(orientation_2_full)
            print(orientation_3_full)
            #oled_display.display_text(str(orientation_1) ) # + "\n" + orientation_2 + "\n" + orientation_3)
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