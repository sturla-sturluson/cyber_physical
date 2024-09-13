from ..display import OledDisplay
from ..sensors import RgbSensor
from ..utils import rgb_to_name
import time
import datetime as dt
import os

def run_slide_rgb_reader(oled_display:OledDisplay):
    rgb_sensor = RgbSensor()

    while True:
        os.system('clear')
        r,g,b = rgb_sensor.get_rgb()
        print(f"R: {r}, G: {g}, B: {b}")
        color_name = rgb_to_name(r,g,b)
        print(color_name)
        #oled_display.display_text(color_name)
        time.sleep(1)