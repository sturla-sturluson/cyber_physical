import webcolors
import math
from ..enums import TapeColor


# Avg RGB values for each color
# {'Black': R    18.76 G    15.35 B    15.35

# 'Blue': R    11.50   G    22.25 B    19.03

# 'Red': R    60.12 G    14.51 B    12.30

# 'Other': R    52.12 G    14.05 B     2.46

# 'Table': R    69.54 G    11.25 B     2.50
# Median RGB values for each color
# {'Black': R    16.0 G    16.0 B    16.0
# 'Blue': R     8.0 G    24.0 B    19.0

# 'Red': R    32.5 G    12.0 B    12.0

# 'Other': R    52.0 G    14.0 B     2.0

# 'Table': R    55.0 G    13.0 B     3.0

AVG_RGB = {
    TapeColor.BLACK: (18.76, 15.35, 15.35),
    TapeColor.BLUE: (11.50, 22.25, 19.03),
    TapeColor.RED: (60.12, 14.51, 12.30),
    TapeColor.OTHER: (52.12, 14.05, 2.46),
    TapeColor.TABLE: (69.54, 11.25, 2.50)
}

MEDIAN_RGB = {
    TapeColor.BLACK: (16.0, 16.0, 16.0),
    TapeColor.BLUE: (8.0, 24.0, 19.0),
    TapeColor.RED: (32.5, 12.0, 12.0),
    TapeColor.OTHER: (52.0, 14.0, 2.0),
    TapeColor.TABLE: (55.0, 13.0, 3.0)
}

def rgb_to_hex(r:int,g:int,b:int) -> str:
    """Converts an RGB value to a hex string."""
    return webcolors.rgb_to_hex((r, g, b))

def calc_distance(color1:tuple[float,float,float],color2:tuple[float,float,float]) -> float:
    """Calculate the distance between two RGB colors."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(color1, color2)))

def get_closest_color(requested_color:tuple[int,int,int]) -> TapeColor:
    """Find the closest color name to the requested RGB value."""
    min_distance = float('inf')
    closest_name = TapeColor.OTHER
    for name, rgb in AVG_RGB.items():
        distance = calc_distance(requested_color, rgb)
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name



