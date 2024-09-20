from ..display import OledDisplay
from ..sensors import MplSensor, RangeSensor,MagneticSensor,RgbSensor
from ..led import Led
from ..utils import get_current_time_string,get_compass_string, get_ip_string, get_pressure_string, get_temperature_string, get_altitude_string
import time
import datetime as dt
from typing import Callable
import asyncio
import threading
import os

def timed_slides(oled_display:OledDisplay,slide_time:int,display_order:list[Callable]):
    count = 0
    last_switch_time = dt.datetime.now()
    while True:
        if (dt.datetime.now() - last_switch_time).seconds > slide_time:
            count += 1
            last_switch_time = dt.datetime.now()
        current_text = display_order[count % len(display_order)]()
        oled_display.display_text(current_text)
        time.sleep(0.25)

class UserPromptSlides:
    def __init__(self,oled_display:OledDisplay,display_order:list[Callable],
                 display_names:list[str],
                    led:Led,
                    magnetic_sensor:MagneticSensor
                 ) -> None:
        self.count = 0
        self.oled_display = oled_display
        self.display_order = display_order
        self.display_names = display_names
        self.led = led
        self.magnetic_sensor = magnetic_sensor

        self.stop_event = threading.Event()
        self._update_ui_event = asyncio.Event()


    async def _user_prompt_slides_loop(self):
        while not self.stop_event.is_set():
            os.system('clear')
            current_text = self.display_order[self.count % len(self.display_order)]()
            current_nsew = self.magnetic_sensor.get_data()[2]
            if(current_nsew == "N"):
                self.led.turn_on()
            else:
                self.led.turn_off()
            self.oled_display.display_text(current_text)
            print(f"Slide {self.count+1}/{len(self.display_order)}")
            print(f"Slide Name: {self.display_names[self.count % len(self.display_names)]}")
            print(f"{current_text}")
            print("Press Enter to go to the next slide")
            
            await asyncio.sleep(0.25)

    def _input_thread(self):
        while True:
            input("Press Enter to go to the next slide")
            self.count += 1
            self.count = self.count % len(self.display_order)


    async def user_prompt_slides(self):
        threading.Thread(target=self._input_thread).start()
        await self._user_prompt_slides_loop()

        

def run_slide_show(oled_display:OledDisplay,slide_time:int,ip:bool):
    try:
        mpl_sensor = MplSensor()
        range_sensor = RangeSensor()
        magnetic_sensor = MagneticSensor()
        rgb_sensor = RgbSensor()
        led_22 = Led(22)
        display_names = ["Time","Pressure","Temperature","Altitude",
                        "Range",
                         "Compass","RGB"]
        display_order = [
        get_current_time_string,
        lambda : get_pressure_string(mpl_sensor),
        lambda : get_temperature_string(mpl_sensor),
        lambda : get_altitude_string(mpl_sensor),   
        lambda : f"Range Sensor\n{range_sensor.get_cm_distance()}cm",
        lambda : get_compass_string(magnetic_sensor),       
        lambda : f"RGB Sensor\n{rgb_sensor.get_rgb()}\n{rgb_sensor.get_color_name()}"
        ]

        if(ip): # Add IP slide to the first position
            display_names.insert(0,"IP")
            display_order.insert(0,get_ip_string)


        # If slide time is less than 1, run the user prompt slide show, wait for user input to switch slides
        #if(slide_time < 1):
        user_prompt_slides = UserPromptSlides(oled_display,display_order,display_names,led_22,magnetic_sensor)
        asyncio.run(user_prompt_slides.user_prompt_slides())
        # else:
        #     timed_slides(oled_display,slide_time,display_order)

    except Exception as e:
        print(e)
        oled_display.display_text("Error\nRun_Slide_Show failed")
        input("Press Enter to quit")