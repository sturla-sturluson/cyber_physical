import math

class Cords:
    x:int|float
    y:int|float
    def __init__(self, x:int|float, y:int|float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        x_str = "None" if self.x is None else str(f"{self.x:.2f}")
        y_str = "None" if self.y is None else str(f"{self.y:.2f}")
        x_str = x_str.rjust(5)
        y_str = y_str.rjust(5)
        return f"{x_str} | {y_str}"

    def set_cords(self,x:int|float,y:int|float):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def get_rotated_cords(self,angle:int|float):
        """Creates a new Cords object where the cords are rotated by the given angle"""
        cos_a = math.cos(math.radians(angle))
        sin_a = math.sin(math.radians(angle))
        x_new = self.x * cos_a - self.y * sin_a
        y_new = self.x * sin_a + self.y * cos_a
        return Cords(x_new,y_new)