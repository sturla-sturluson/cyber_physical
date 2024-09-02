import os 
import time
import datetime as dt
import asyncio
import subprocess

class Display:
    def __init__(self) -> None:
        self.slideshow = False
        self.slides = []
        self.slide_index = 0
        self.slide_time = 2

        self.last_switch_time = dt.datetime.now()

    def toggle_slideshow(self):
        self.slideshow = not self.slideshow

    def add_slide(self, slide:str):
        self.slides.append(slide)

    def run_display(self):
        
        while True:
            os.system('clear')
            timestamp = dt.datetime.now()
            clock = timestamp.strftime("%H:%M:%S")
            print(f"Current Time: {clock}")
            if(len(self.slides) > 0):
                print(f"Slide: {self.slides[self.slide_index]}")
            if self.slideshow:
                if (timestamp - self.last_switch_time).seconds > self.slide_time:
                    self.slide_index += 1 
                    self.last_switch_time = timestamp
                    if self.slide_index >= len(self.slides):
                        self.slide_index = 0
            time.sleep(0.2)

def main():
    display = Display()
    display.add_slide("Slide 1")
    display.add_slide("Slide 2")
    display.add_slide("Slide 3")
    display.add_slide("Slide 4")
    display.toggle_slideshow()
    # Launch the display in a separate thread and run that display in a different console window

    while True:
        command = input("Enter command: ")
        if command == "exit":
            break
        elif command == "toggle":
            display.toggle_slideshow()
        elif command == "add":
            slide = input("Enter slide: ")
            display.add_slide(slide)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()