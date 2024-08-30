# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print the device's IP address in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

from src import OledDisplay,get_local_ip, Mpl_Sensor
import time
import datetime as dt

def get_ip_string():
    ip_address = get_local_ip()
    return f"Local Ip\n{ip_address}"

def get_current_time_string():
    time_now = dt.datetime.now()
    day_short_string = time_now.strftime("%a")
    day_month_string = time_now.strftime("%d %b")
    hour_min_string = time_now.strftime("%H:%M")
    return f"{day_short_string} {day_month_string}\n{hour_min_string}"

def get_pressure_string(mpl_sensor:Mpl_Sensor):
    pressure = mpl_sensor.get_pressure()
    return f"{pressure:.2f} Pa"

def get_temperature_string(mpl_sensor:Mpl_Sensor):
    temperature = mpl_sensor.get_temperature()
    return f"{temperature:.1f} C°"

def get_altitude_string(mpl_sensor:Mpl_Sensor):
    altitude = mpl_sensor.get_altitude()
    return f"{altitude:.1f}m"


def main():
    oled_display = OledDisplay()
    ip_address = get_local_ip()
    mpl_sensor = Mpl_Sensor()
    oled_display.draw_text(ip_address)
    display_order = [
        get_current_time_string,
        get_ip_string,
        lambda : get_pressure_string(mpl_sensor),
        lambda : get_temperature_string(mpl_sensor),
        lambda : get_altitude_string(mpl_sensor)]
    count = 0
    try:
        while True:
            current_text = display_order[count % len(display_order)]()
            oled_display.draw_text(current_text)
            count += 1
            time.sleep(4)

    except KeyboardInterrupt:
        oled_display.draw_text("Goodbye!")
        time.sleep(4)
        oled_display.clear()
    except Exception as e:
        print(e)
        oled_display.draw_text("Error")




if __name__ == "__main__":
    main()