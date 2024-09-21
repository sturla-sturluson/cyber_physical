
import argparse
from src import app
# -ip : Display the IP address
IP_FLAG = "ip"
# -slide <seconds> : Run the slide show with the specified number of seconds per slide
SLIDE_FLAG = "slide"
# -compass : Display the compass
COMPASS_FLAG = "compass"
# -cal : Calibrate the compass
# This is added as a flag behind compass or range sensor
CALIBRATION_FLAG = "cal"
# -rgb : Display the RGB sensor
RGB_FLAG = "rgb"
# -range : Display the range sensor
RANGE_FLAG = "range"



def main():
    slide = False
    slide_time = 4

    parser = argparse.ArgumentParser(description="Run the screen app")
    parser.add_argument(f"-{IP_FLAG}", action="store_true", help="Display the IP address")
    parser.add_argument(f"-{SLIDE_FLAG}", type=int, metavar='<seconds>', help=f"Run the slide show with the specified number of seconds per slide, can be paired with -{IP_FLAG}")
    parser.add_argument(f"-{COMPASS_FLAG}", action="store_true", help=f"Display the compass, add -{CALIBRATION_FLAG} to calibrate the compass")
    parser.add_argument(f"-{CALIBRATION_FLAG}", action="store_true", help="Calibrate the compass or range sensor")
    parser.add_argument(f"-{RGB_FLAG}", action="store_true", help="Display the RGB sensor")
    parser.add_argument(f"-{RANGE_FLAG}", action="store_true", help=f"Display the range sensor, add -{CALIBRATION_FLAG} to calibrate the range sensor")
    args = parser.parse_args()
    print(f"Args: {args}")
     
    if args.slide:
        slide = True
        if args.slide > 0:
            slide_time = args.slide
        app(slide=slide, slide_time=slide_time,ip=args.ip)
    elif args.ip:
        app(ip=True)
    elif args.compass:
        app(compass=True, calibrate=args.cal)
    elif args.rgb:
        app(rgb=True)
    elif args.range:
        app(range_sensor=True, calibrate=args.cal)
    else:
        app()




if __name__ == "__main__":
    main()