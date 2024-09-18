from .sensors import MplSensor,RgbSensor,MagneticSensor
from .utils import get_current_time_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
from .display import OledDisplay
import time
import datetime as dt
from .ui_funcs import (
    run_slide_show,
    run_display_compass,
    run_slide_rgb_reader,
    run_display_range_sensor,
    run_compass_calibration,
    run_range_sensor_calibration)





def app(
        slide:bool = False,
        slide_time:int = 4,
        compass:bool = False,
        rgb:bool = False,
        calibrate:bool = False,
        range_sensor:bool = False,
        ):
    

    oled_display = OledDisplay()
    try:
        if(slide):
            run_slide_show(oled_display,slide_time)
        elif(compass):
            if(calibrate):
                run_compass_calibration()
            else:
                run_display_compass(oled_display)
        elif(rgb):
            run_slide_rgb_reader(oled_display)
        elif(range_sensor):
            if(calibrate):
                run_range_sensor_calibration()
            else:
                run_display_range_sensor(oled_display)
        else:
            oled_display.display_text(get_ip_string())
            input("Press Enter to quit")

    except KeyboardInterrupt:
        oled_display.clear()
        oled_display.cleanup()
    except Exception as e:
        print(e)
        oled_display.display_text("Error")
    finally:
        oled_display.cleanup()
        print("Done")



