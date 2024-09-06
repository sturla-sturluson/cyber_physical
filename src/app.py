from .sensors import MplSensor,RgbSensor,MagneticSensor
from .utils import get_current_time_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
from .display import OledDisplay
import time
import datetime as dt
from .display_slides import run_slide_show
from .display_compass import run_display_compass



def app(
        slide:bool = False,
        slide_time:int = 4,
        compass:bool = False
        ):
    oled_display = OledDisplay()


    try:
        if(slide):
            run_slide_show(oled_display,slide_time)
        elif(compass):
            run_display_compass(oled_display)
        else:
            oled_display.display_text(get_ip_string())
            input("Press Enter to quit")

    except KeyboardInterrupt:
        oled_display.display_text("Goodbye!")
        time.sleep(4)
        oled_display.clear()
    except Exception as e:
        print(e)
        oled_display.display_text("Error")
    finally:
        oled_display.cleanup()
        print("Done")



