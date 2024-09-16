import math

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



def main():
    while True:
        x,y = input().split()
        x = int(x)
        y = int(y)
        print(calculate_orientation(x,y))


if __name__ == "__main__":
    main()