# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print the device's IP address in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import argparse
from src import app
# -slide <seconds> : Run the slide show with the specified number of seconds per slide
SLIDE_FLAG = "slide"

def main():
    slide = False
    slideshow_time = 4




    parser = argparse.ArgumentParser(description="Run the IP display app")
    parser.add_argument(f"--{SLIDE_FLAG}", type=int, help="Run the slide show with the specified number of seconds per slide")
    args = parser.parse_args()
    if args.slide:
        slide = True
        if args.slide > 0:
            slideshow_time = args.slide
    else:
        app(slide=slide, slideshow_time=slideshow_time)




if __name__ == "__main__":
    main()