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
# -compass : Display the compass








def main():
    slide = False
    slide_time = 4

    parser = argparse.ArgumentParser(description="Run the IP display app")
    parser.add_argument(f"--{SLIDE_FLAG}", type=int, help="Run the slide show with the specified number of seconds per slide")
    parser.add_argument("--compass", action="store_true", help="Display the compass")
    args = parser.parse_args()
    print(f"Args: {args}")
    if args.slide:
        slide = True
        if args.slide > 0:
            slide_time = args.slide
        app(slide=slide, slide_time=slide_time)
    elif args.compass:
        app(compass=True)
    else:
        app(slide=slide, slide_time=slide_time)




if __name__ == "__main__":
    main()