from ..display import OledDisplay
from ..sensors import MplSensor
from ..utils import get_current_time_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
import time
import datetime as dt


def run_slide_show(oled_display:OledDisplay,slide_time:int,ip:bool):
    try:
        mpl_sensor = MplSensor()
        display_order = [
        get_current_time_string,

        lambda : get_pressure_string(mpl_sensor),
        lambda : get_temperature_string(mpl_sensor),
        lambda : get_altitude_string(mpl_sensor)]
        if(ip): # Add IP slide to the first position
            display_order.insert(0,get_ip_string)
        count = 0
        last_switch_time = dt.datetime.now()
        while True:
            if (dt.datetime.now() - last_switch_time).seconds > slide_time:
                count += 1
                last_switch_time = dt.datetime.now()
            current_text = display_order[count % len(display_order)]()
            oled_display.display_text(current_text)
            time.sleep(0.25)
    except Exception as e:
        print(e)
        oled_display.display_text("Error\nRun_Slide_Show failed")
        input("Press Enter to quit")