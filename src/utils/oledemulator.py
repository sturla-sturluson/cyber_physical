import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageTk as imgTk
import math
from time import sleep

class OledScreenEmulator:
    def __init__(self, width=128, height=64):
        # Create a new 1-bit image, same oled setup
        self._image = Image.new("1", (width, height))
        self._draw = ImageDraw.Draw(self._image)
        self._font = ImageFont.load_default()

        # Setup the window and label that contains the image
        self._root = tk.Tk()
        self._label = tk.Label(self._root)
        self._label.pack()

        # Center the window
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        window_width = width
        window_height = height
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self._root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down-100}")
        
    def _update(self):
        ''' Convert the pillow image to a tkinter image and reload it into the label '''
        tk_image = imgTk.PhotoImage(self._image)
        # 'Cast' it to a _ImageSpec 
        self._label.configure(image=tk_image) # type: ignore

        # Setting the image on the label
        self._label.image = tk_image # type: ignore

    def __del__(self):
        ''' Small hack to keep the window open after the last show() call '''
        self._root.mainloop()

    ### OLED SCREEN EMULATOR FUNCTIONS ###
    def text(self, x, y, text):
        ''' Draw text on the image, same functionality as the oled screen '''
        self._draw.text((x, y), text, font=self._font, fill=255)
    
    def pixel(self, x, y, color):
        ''' Draw a pixel on the image, same functionality as the oled screen '''
        self._draw.point((x, y), fill=color)

    def show(self):
        ''' Shows the image on the screen by updating the label, sleep added to emulate the oled refresh rate '''
        self._update()
        self._root.update()
        self._root.update_idletasks()
        sleep(0.01) 
    
    def clear(self):
        ''' Not an actual oled function, but clears the image, this should be fill() '''
        self._draw.rectangle((0, 0, 128, 64), fill=0)
        self._update()


def main():
    oled = OledScreenEmulator()
    oled.clear()
    oled.text(0, 0, "Hello, World!")
    for i in range(128):
        y = 32 + int(32 * math.sin(math.radians(i * 2 + i)))
        oled.pixel(i, y, 255)
        oled.show()


if __name__ == "__main__":
    main()