
import argparse
from src import app
# -slide <seconds> : Run the slide show with the specified number of seconds per slide
SLIDE_FLAG = "slide"
# -compass : Display the compass
COMPASS_FLAG = "compass"
# -cal : Calibrate the compass
# This is added as a flag behind compass or range sensor
COMPASS_CALIBRATION_FLAG = "cal"
# -rgb : Display the RGB sensor
RGB_FLAG = "rgb"
# -range : Display the range sensor
RANGE_FLAG = "range"



def main():
    slide = False
    slide_time = 4

    parser = argparse.ArgumentParser(description="Run the screen app")
    parser.add_argument(f"-{SLIDE_FLAG}", type=int, metavar='<seconds>', help="Run the slide show with the specified number of seconds per slide")
    parser.add_argument(f"-{COMPASS_FLAG}", action="store_true", help="Display the compass, add --cal to calibrate the compass")
    parser.add_argument(f"-{COMPASS_CALIBRATION_FLAG}", action="store_true", help="Calibrate the compass or range sensor")
    parser.add_argument(f"-{RGB_FLAG}", action="store_true", help="Display the RGB sensor")
    parser.add_argument(f"-{RANGE_FLAG}", action="store_true", help="Display the range sensor, add --cal to calibrate the range sensor")
    args = parser.parse_args()
    print(f"Args: {args}")
     
    if args.slide:
        slide = True
        if args.slide > 0:
            slide_time = args.slide
        app(slide=slide, slide_time=slide_time)
    elif args.compass:
        app(compass=True, calibrate=args.cal)
    elif args.rgb:
        app(rgb=True)
    elif args.range:
        app(range_sensor=True, calibrate=args.cal)
    else:
        app(slide=slide, slide_time=slide_time)




if __name__ == "__main__":
    main()