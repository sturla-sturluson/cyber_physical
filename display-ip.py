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

def main():
    oled_display = OledDisplay()
    ip_address = get_local_ip()
    mpl_sensor = Mpl_Sensor()
    oled_display.draw_text(ip_address)



if __name__ == "__main__":
    main()