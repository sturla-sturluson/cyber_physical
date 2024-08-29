import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class OledDisplay:
    # Change these
    # to the right size for your display!
    WIDTH = 128
    HEIGHT = 64
    BORDER = 5
    def __init__(self) -> None:
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C, reset=self.oled_reset)



    def draw_text(self,text:str):
        """Draws the text on the OLED display"""
        self.oled.fill(0)
        self.oled.show()
        image = Image.new("1", (self.oled.width, self.oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)

        # Draw a smaller inner rectangle
        draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )

        # Load default font.
        font = ImageFont.load_default()
        # Draw it into a box.
        bbox = font.getbbox(str(text))
        (font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            (self.oled.width // 2 - font_width // 2, self.oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )

        # Display image
        self.oled.image(image)
        self.oled.show()





