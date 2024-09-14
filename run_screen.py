
import argparse
from src import app
# --slide <seconds> : Run the slide show with the specified number of seconds per slide
SLIDE_FLAG = "slide"
# --compass : Display the compass
COMPASS_FLAG = "compass"
# --calibrate : Calibrate the compass
COMPASS_CALIBRATION_FLAG = "calibrate"
# --rgb : Display the RGB sensor
RGB_FLAG = "rgb"



def main():
    slide = False
    slide_time = 4

    parser = argparse.ArgumentParser(description="Run the screen app")
    parser.add_argument(f"--{SLIDE_FLAG}", type=int, help="Run the slide show with the specified number of seconds per slide")
    parser.add_argument(f"--{COMPASS_FLAG}", action="store_true", help="Display the compass")
    parser.add_argument(f"--{COMPASS_CALIBRATION_FLAG}", action="store_true", help="Calibrate the compass")
    parser.add_argument(f"--{RGB_FLAG}", action="store_true", help="Display the RGB sensor")
    args = parser.parse_args()
    print(f"Args: {args}")
    if args.slide:
        slide = True
        if args.slide > 0:
            slide_time = args.slide
        app(slide=slide, slide_time=slide_time)
    elif args.compass:
        app(compass=True)
    elif args.calibrate:
        app(calibrate=True)
    elif args.rgb:
        app(rgb=True)
    else:
        app(slide=slide, slide_time=slide_time)




if __name__ == "__main__":
    main()