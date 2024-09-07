
import argparse
from src import app
# -slide <seconds> : Run the slide show with the specified number of seconds per slide
SLIDE_FLAG = "slide"
# -compass : Display the compass



def main():
    slide = False
    slide_time = 4

    parser = argparse.ArgumentParser(description="Run the screen app")
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