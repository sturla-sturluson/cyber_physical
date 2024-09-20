from ..models import Cords
import math
import numpy as np



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


def degrees_to_coordinates(angle_degrees: int) -> tuple[float, float]:
    # Convert angle from degrees to radians, and reverse for clockwise
    angle_degrees -= 90
    angle_radians = math.radians(360 - angle_degrees)

    # Calculate the x and y coordinates
    x = 90 * math.cos(angle_radians)
    y = 90 * math.sin(angle_radians)

    return x, y

def calculate_orientation(x: int | float, y: int | float) -> int:
    """Takes in x and y coordinates and returns the orientation in degrees.
    X and Y range from -90 to 90.
    0,90 -> 0  # North
    90,0 -> 90  # East
    0,-90 -> 180  # South
    -90,0 -> 270  # West
    """
    angle_degrees = math.degrees(math.atan2(y, x))   
    adjusted_angle = 90 - angle_degrees # Adjust the angle to match the orientation
    # Clamp the angle to 0-360
    if adjusted_angle < 0:
        adjusted_angle += 360
    return int(round(adjusted_angle))

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


def get_removed_outliers(array:np.ndarray) -> np.ndarray:
    """Returns the array with the outliers removed
    Args:
        array (np.array): The array to remove outliers from
    Returns:
        np.array: The array with the outliers removed
    """
    quartile_1 = np.percentile(array, 25)
    quartile_3 = np.percentile(array, 75)
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (1.5 * iqr)
    upper_bound = quartile_3 + (1.5 * iqr)
    array = array[(array > lower_bound) & (array < upper_bound)]
    return array

def get_robust_avg(array:np.ndarray) -> float:
    """Returns the robust average of the array
    Args:
        array (np.array): The array to average
    Returns:
        float: The average of the array
    """
    array = get_removed_outliers(array)
    return float(np.mean(array))

def print_out_python_formatted_poly(coefficients:np.ndarray):
    """Prints out the coefficients in a python formatted polynomial"""
    equation_string = ""
    for i in range(len(coefficients)):
        equation_string += f"{coefficients[i]:.2f} * voltage**{len(coefficients)-i-1} + "
    print(equation_string.rstrip(" + "))

# Creating compound typehint for the function


def generate_coefficients_equation(degree:int,y_rr:np.ndarray|list[float]|list[int],x:np.ndarray|list[float]|list[int]) -> np.ndarray:
    """Generates the coefficients for a polynomial equation
    Args:
        degree (int): The degree of the polynomial
        y_rr (np.ndarray): The y values
        x (np.ndarray): The x values
    Returns:
        np.ndarray: The coefficients of the polynomial
    Example:
        degree = 4
        y_rr = np.array([1,2,3,4,5])
        x = np.array([4,3,2,5,0])
        generate_coefficients_equation(degree,y_rr,x)
        Output:
        array([
        -5.36784506e-09             
         4.00801473e-07        
         3.02151621e-04        
        -5.57442814e-02        
         3.28273748e+00  
        ])
    """
    coefficients =  np.polyfit(y_rr,x,degree)
    return coefficients

def volt_to_cm_poly(voltage:float,coefficients:np.ndarray)->float:
    cm = 0
    for i in range(len(coefficients)):
        cm += coefficients[i] * voltage**(len(coefficients)-i-1)
    return float(cm)

