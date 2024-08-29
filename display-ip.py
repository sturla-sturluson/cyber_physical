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
    return dt.datetime.now().strftime("%H:%M:%S")

def get_pressure_string(mpl_sensor:Mpl_Sensor):
    pressure = mpl_sensor.get_pressure()
    return f"Prs: {pressure:.2f} Pa"

def get_temperature_string(mpl_sensor:Mpl_Sensor):
    temperature = mpl_sensor.get_temperature()
    return f"Tmp: {temperature:.2f} C"

def get_altitude_string(mpl_sensor:Mpl_Sensor):
    altitude = mpl_sensor.get_altitude()
    return f"Alt: {altitude:.2f} m"


def main():
    oled_display = OledDisplay()
    ip_address = get_local_ip()
    mpl_sensor = Mpl_Sensor()
    oled_display.draw_text(ip_address)
    display_order = [
        get_current_time_string,
        get_local_ip,
        lambda : get_pressure_string(mpl_sensor),
        lambda : get_temperature_string(mpl_sensor),
        lambda : get_altitude_string(mpl_sensor)]
    count = 0
    while True:
        try:
            text_to_display = display_order[count]()
            oled_display.draw_text(text_to_display)
            count = (count + 1) % len(display_order)
        except Exception as e:
            print(e)
            oled_display.draw_text("Error")
        time.sleep(2)



if __name__ == "__main__":
    main()