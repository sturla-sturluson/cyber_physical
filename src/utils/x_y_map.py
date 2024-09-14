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
    def __init__(self) -> None:
        # Scale is the number of degrees per grid
        # 1 would be 180x180 add 1 for the axis
        dimensions = 180 + 1

        self.map = np.zeros((dimensions,dimensions),dtype=int)
        # Create vertical Y axis and horizontal X axis

        for i in range(dimensions):
            self.map[dimensions//2,i] = -1
            self.map[i,dimensions//2] = -1

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
        self.map[row_index,col_index] = 1



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
                for x in range(scale):
                    for y in range(scale):
                        if(self.map[i*scale+x,j*scale+y] == 1):
                            str_map[i][j+1] = _get_color_string("1 ","green")
                            break
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
    

def main():
    map = X_Y_Map()
    map.add_cord(0,90)
    #map.add_cord(89,1)
    print(map.get_scaled_map(10))

if __name__ == "__main__":
    main()