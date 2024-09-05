import board
import digitalio
from adafruit_ssd1306 import SSD1306_I2C
import busio
from PIL import Image, ImageDraw, ImageFont

DEFAULT_BORDER = 2


class OledDisplay:
    # Change these
    # to the right size for your display!
    WIDTH = 128
    HEIGHT = 64

    def __init__(self,borderWidth:int = DEFAULT_BORDER) -> None:
        """Initializes the OLED display"""
        try:    
            self.border = borderWidth
            self.screen_dim = (self.WIDTH, self.HEIGHT)
            self.font = ImageFont.load_default()
            i2c = busio.I2C(board.SCL, board.SDA)
        except Exception as e:
            print(e)
            raise e
        print("Font name: ",self.font.getname())

        # Create the reset pin
        self.oled_reset = digitalio.DigitalInOut(board.D4)


        # Create the SSD1306 OLED class.
        self.oled = SSD1306_I2C(self.WIDTH, self.HEIGHT, i2c, addr=0x3c, reset=self.oled_reset)



    def display_text(self,
        text:str):
        """Draws the text on the OLED display"""
        #self.oled.fill(0)   # Clear the display
        #self.oled.show()    # Display the cleared image
        # Create blank image for drawing.
        image = Image.new("1", self.screen_dim)
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image) 
        # Draw the border
        self._draw_screen_border(draw)
        # Draw the text
        self._draw_text(draw,text)


        # Display image
        self.oled.image(image)
        self.oled.show()




    def _draw_text(self,draw:ImageDraw.Draw,text:str):
        """Draws the text on the OLED display
        Args:
            draw (ImageDraw.Draw): The ImageDraw object to draw on the OLED display
            text (str): The text to draw
        """
        # Load default font.
        bbox = self.font.getbbox(str(text))
        font_width = bbox[2] - bbox[0]
        font_height = bbox[3] - bbox[1]
        draw.text(
            (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
            text,
            font=self.font,
            fill=255,
            #anchor="mm",
            #align="center",
        )

    def _draw_screen_border(self,draw:ImageDraw.Draw):
        """Draws a border around the OLED display
        Args:
            draw (ImageDraw.Draw): The ImageDraw object to draw on the OLED display
        """

        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        # Draw a smaller inner rectangle
        draw.rectangle(
            (self.border, self.border, self.oled.width - self.border - 1, self.oled.height - self.border - 1),
            outline=0, fill=0,
        )


    def clear(self):
        """Clears the OLED display"""
        self.oled.fill(0)
        self.oled.show()


    def cleanup(self):
        """Cleans up the OLED display"""
        self.clear()
        self.oled.fill(0)
        self.oled.show()
        self.oled_reset.deinit()
        self.i2c.deinit()
        print("OLED display cleaned up")

