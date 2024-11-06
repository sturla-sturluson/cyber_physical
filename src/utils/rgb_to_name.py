import webcolors
import math
from ..enums import TapeColor


# {'Black': R    26.42
# G    20.01
# B     4.58
# dtype: float64, 'Blue': R     7.62
# G    26.50
# B    21.35
# dtype: float64, 'Red': R    118.10
# G      4.34
# B      2.00
# dtype: float64}

AVG_RGB = {
    TapeColor.BLACK: (26.42,20.01,4.58),
    TapeColor.BLUE: (7.62,26.50,21.35),
    TapeColor.RED: (118.10,4.34,2.00)
}

# {'Black': R    25.0
# G    21.0
# B     4.0
# dtype: float64, 'Blue': R     8.0
# G    26.0
# B    21.0
# dtype: float64, 'Red': R    117.0
# G      4.0
# B      2.0
# dtype: float64}
MEDIAN_RGB = {
    TapeColor.BLACK: (25,21,4),
    TapeColor.BLUE: (8,26,21),
    TapeColor.RED: (117,4,2)

}

AVG_RGB_LIST = [AVG_RGB[x] for x in AVG_RGB]

MEDIAN_RGB_LIST = [MEDIAN_RGB[x] for x in MEDIAN_RGB]

ALL_LIST = AVG_RGB_LIST + MEDIAN_RGB_LIST

_MATTER = [TapeColor.BLACK,TapeColor.BLUE,TapeColor.RED]

ALL_MATTER_LIST = [AVG_RGB[x] for x in AVG_RGB if x in _MATTER] + [MEDIAN_RGB[x] for x in MEDIAN_RGB if x in _MATTER]

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
    for name, rgb in MEDIAN_RGB.items():
        distance = calc_distance(requested_color, rgb)
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name

def calc_distances(main_color:tuple[float,float,float],colors:list[tuple[float,float,float]]):
    return [calc_distance(main_color,x) for x in colors]

def get_closest_tape_color(rgb:tuple[int,int,int]) -> TapeColor:
    distances = calc_distances(rgb,ALL_MATTER_LIST)
    # 
    for i in range(len(distances)):
        if distances[i] < 10:
            index = i % len(_MATTER)
            return _MATTER[index]
    return TapeColor.OTHER

def get_tape_color(rgb:tuple[int,int,int])->TapeColor:
    """Since the colors are not perfect, we need to check the ranges"""
    r,g,b =  rgb
    if(r>90):
        return TapeColor.RED
    if(r>60 and (g+b)<30):
        return TapeColor.RED
    
    
    if (r>30 and g > 30 and b<30):
        return TapeColor.BLACK
    if (r== 45 and g == 45):
        return TapeColor.BLACK
    if (r<30 and g < 30 and b<30):
        return TapeColor.BLUE
    if (r<40 and g < 40 and b<40 and (r+g+b)<100):
        return TapeColor.BLUE
    return TapeColor.OTHER