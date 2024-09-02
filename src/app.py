# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print the device's IP address in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

from .mpl_sensor import Mpl_Sensor
from .str_formatter import get_current_time_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
from .oled_display import OledDisplay
import time
import datetime as dt


def run_slide_show(oled_display:OledDisplay):
    mpl_sensor = Mpl_Sensor()
    display_order = [
    get_current_time_string,
    get_ip_string,
    lambda : get_pressure_string(mpl_sensor),
    lambda : get_temperature_string(mpl_sensor),
    lambda : get_altitude_string(mpl_sensor)]
    count = 0
    slide_time = 6
    last_switch_time = dt.datetime.now()
    while True:
        if (dt.datetime.now() - last_switch_time).seconds > slide_time:
            count += 1
            last_switch_time = dt.datetime.now()
        current_text = display_order[count % len(display_order)]()
        oled_display.display_text(current_text)
        time.sleep(0.25)

def app(slide:bool, slideshow_time:int):
    oled_display = OledDisplay()


    try:
        run_slide_show(oled_display)

    except KeyboardInterrupt:
        oled_display.display_text("Goodbye!")
        time.sleep(4)
        oled_display.clear()
    except Exception as e:
        print(e)
        oled_display.display_text("Error")



