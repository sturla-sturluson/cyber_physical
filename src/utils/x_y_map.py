import numpy as np



def _get_color_string(value:str,color:str)->str:
    """Colorizes a string"""
    if color == "red":
        return f"\033[91m{value}\033[00m"
    elif color == "green":
        return f"\033[92m{value}\033[00m"
    elif color == "yellow":
        return f"\033[93m{value}\033[00m"
    elif color == "blue":
        return f"\033[94m{value}\033[00m"
    else:
        return value



class X_Y_Map:
    """ A 180x180 map that shows the cords
    from -90 to 90 degrees
    cord (52,32) would be added map[142,122]
    All of them will be 0, if a cord is added it will be 1
    """



    def __init__(self,display_count:int = -1) -> None:
        # Scale is the number of degrees per grid
        # 1 would be 180x180 add 1 for the axis
        dimensions = 180 + 1

        self.map = np.zeros((dimensions,dimensions),dtype=int)
        # Create vertical Y axis and horizontal X axis
        self._added_cords = [] # List of cords that have been added
        self._display_count = display_count # How many cords to display, -1 for all

        # for i in range(dimensions):
        #     self.map[dimensions//2,i] = -1
        #     self.map[i,dimensions//2] = -1

    def _update_display_count(self):
        """Updates the display count"""
        if self._display_count == -1:
            return
        if len(self._added_cords) > self._display_count:
            for i in range(len(self._added_cords) - self._display_count):
                x,y = self._added_cords.pop(0)
                row_index = 180-max(min(int(y) + 90, 180), 0) 
                col_index = max(min(int(x) + 90, 180), 0)
                self.map[row_index,col_index] -= 1

    def add_cord(self,x:int|float,y:int|float):
        """Adds a cord to the map"""
        # If the cord is for example (0,90), which is north
        # Start by finding the row index
        # The row is gonna be the y value. -90 would be row 180
        # We add 90 but subtract it from 180 to get the correct row index
        # Using a min max clamp to make sure the value is within the range
        row_index = 180-max(min(int(y) + 90, 180), 0) 
        # Column index is -90 = 0 and 90 = 180
        col_index = max(min(int(x) + 90, 180), 0)
        self.map[row_index,col_index] += 1
        self._added_cords.append((x,y))
        self._update_display_count()

    def _get_icon(self,count:int)->str:
        """Gets correctly formatted number"""
        if count == 0:
            return "  "
        elif count < 10:
            return f"{count} "
        else:
            return f"9+"

    def _get_row_list(self,width:int,value:str = "  ",center:str = "Y ")->list[str]:
        """Returns a list of strings for a row"""
        list_str = ["  "] # Adding space for left border
        for i in range(width+1):
            if(i == width//2):
                list_str.append(center)
            else:
                list_str.append(value)
        list_str.append("  ") # Adding space for right border
        return list_str
    
    def get_scaled_map(self,scale:int = 1)->str:
        """Returns a scaled map"""
        scaled_ratio = (180//scale) + 1 # 1 for Axis and adding 2 for the borders
        str_map = [[] for i in range(scaled_ratio)]
        for i in range(scaled_ratio):
            if(i == scaled_ratio//2):
                str_map[i] = self._get_row_list(scaled_ratio,"X ","+ ")
            else:
                str_map[i] = self._get_row_list(scaled_ratio)         
        for i in range(scaled_ratio-1):   
            for j in range(scaled_ratio-1):
                grid_count = 0
                for x in range(scale):
                    for y in range(scale):
                        grid_count += self.map[i*scale+x,j*scale+y]
                if(grid_count > 0):
                    str_map[i][j+1] = _get_color_string(self._get_icon(grid_count),"green")

        # Settings NESW directions with N,E,S,W
        new_str_map = []
        # Adding top border
        new_str_map.append(self._get_row_list(scaled_ratio,"  ","  "))
        # adding the old map
        new_str_map.extend(str_map)
        # Adding bottom border
        new_str_map.append(self._get_row_list(scaled_ratio,"  ","  "))
        # Adding the NESW directions
        new_str_map[0][scaled_ratio//2 +1] = _get_color_string("N ","red")
        new_str_map[scaled_ratio//2+1][-1] = _get_color_string("E ","red")
        new_str_map[-1][scaled_ratio//2 +1] = _get_color_string("S ","red")
        new_str_map[scaled_ratio//2+1][0] = _get_color_string("W ","red")
        return "\n".join(["".join(row) for row in new_str_map])

    def __str__(self) -> str:
        return self.get_scaled_map(1)

def random_test():
    import random
    import os
    import time
    map = X_Y_Map(10)
    while True:
        os.system('clear')
        x = random.uniform(-90,90)
        y = random.uniform(-90,90)
        map.add_cord(x,y)
        print(map.get_scaled_map(10))
        time.sleep(1)

def circle_test():
    import os
    import random
    import math
    import time
    def degrees_to_coordinates(angle_degrees: int) -> tuple[float, float]:
        # Convert angle from degrees to radians, and reverse for clockwise
        angle_degrees -= 90
        angle_radians = math.radians(360 - angle_degrees)

        # Calculate the x and y coordinates
        x = 90 * math.cos(angle_radians)
        y = 90 * math.sin(angle_radians)

        return x, y
    
    map = X_Y_Map()
    current_angle = 0
    while True:
        os.system('clear')
        x,y = degrees_to_coordinates(int(current_angle))
        map.add_cord(x,y)
        print(map.get_scaled_map(10))
        print(f"Angle: {current_angle:.1f}")
        print(f"X: {x:.1f} Y: {y:.1f}")
        #input()
        current_angle += random.randint(1,10)
        current_angle %= 360
        time.sleep(0.2)

def main():
    circle_test()




if __name__ == "__main__":
    main()