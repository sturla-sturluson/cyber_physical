from PIL import Image, ImageDraw, ImageFont


def _draw_text(
                self,
                draw:ImageDraw,
                text:str):
    """Draws the text on the OLED display
    Args:
        draw (ImageDraw.Draw): The ImageDraw object to draw on the OLED display
        text (str): The text to draw
    """
    # Load default font.
    width = 128
    height = 64
    split_text = text.split("\n")
    if(len(split_text) > 1):
        _draw_multiline_text(draw,split_text)
        return
    font = ImageFont.load_default()
    bbox = font.getbbox(str(text))
    font_width = bbox[2] - bbox[0]
    font_height = bbox[3] - bbox[1]
    draw.text(
        ((width - font_width) // 2, (height - font_height ) // 2),
        text,
        font=font,
        fill=255,
        #anchor="mm",
        align="center",
    )

def _draw_multiline_text(self, draw:ImageDraw, split_text:list[str]):
    """Draws the text on the OLED display
    Args:
        draw (ImageDraw.Draw): The ImageDraw object to draw on the OLED display
        text (str): The text to draw
    """
    # Load default font.
    width = 128
    height = 64
    line_1, line_2, line_3, line_4 = "","","",""
    # At most do 4 lines
    if(len(split_text) == 2):
        line_2 = split_text[0]
        line_3 = split_text[1]
    elif(len(split_text) == 3):
        line_1 = split_text[0]
        line_2 = split_text[1]
        line_3 = split_text[2]
    else:
        line_1 = split_text[0]
        line_2 = split_text[1]
        line_3 = split_text[2]
        line_4 = split_text[3]

    combined_text = f"{line_1}\n{line_2}\n{line_3}\n{line_4}"
    font = ImageFont.load_default()
    bbox1 = font.getbbox(line_1)
    bbox = font.getbbox(combined_text)
    font_width = bbox[2] - bbox[0]
    font_height = bbox[3] - bbox[1]
    draw.multiline_text(
        (0,0),
        combined_text,
        font=font,
        fill=255,
        #anchor="mm",
        #align="center",
    )

def main():
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image) 

    _draw_text(draw,"Hello World")


    image.show()

if __name__ == "__main__":
    main()