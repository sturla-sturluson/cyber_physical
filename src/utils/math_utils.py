from ..models import Cords
import math

def get_dot_product(cord1:Cords,cord2:Cords):
    """Returns the dot product of two cords
    Args:
        cord1 (Cords): The first cord
        cord2 (Cords): The second cord
    Returns:
        int|float: The dot product of the two cords    
    """
    x1 = cord1.x
    y1 = cord1.y
    x2 = cord2.x
    y2 = cord2.y
    return x1*x2 + y1*y2

def get_angle(cord1:Cords,cord2:Cords):
    """Returns the angle between two cords
    Args:
        cord1 (Cords): The first cord
        cord2 (Cords): The second cord
    Returns:
        int|float: The angle between the two cords    
    """
    dot_product = get_dot_product(cord1,cord2)
    magnitude1 = cord1.get_magnitude()
    magnitude2 = cord2.get_magnitude()
    theta = dot_product / (magnitude1 * magnitude2)
    degrees = math.degrees(math.acos(theta))
    return degrees

def get_midpoints(max_cords:Cords,min_cords:Cords):
    """Returns the midpoints of the max and min cords
    Args:
        max_cords (Cords): The max cords
        min_cords (Cords): The min cords
    Returns:
        tuple: The midpoints of the max and min cords    

    Example:
        x_max = 74 x_min = -34
    x_midpoint = (74 + (-34)) / 2 = 20  
    The center is 20
        x_max = 90 x_min = -90
    x_midpoint = (90 + (-90)) / 2 = 0
    The center is 0
    
    """
    x_midpoint = (max_cords.x + min_cords.x) / 2
    y_midpoint = (max_cords.y + min_cords.y) / 2
    return x_midpoint, y_midpoint