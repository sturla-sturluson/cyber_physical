import numpy as np
from queue import Queue



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

        #self.map = np.zeros((dimensions,dimensions),dtype=int)
        # Create vertical Y axis and horizontal X axis
        # cords map key is x and value is y 
        self.cords_queue:Queue[tuple[int,int]] = Queue()
        self.cords_map:dict[int,dict[int,int]] = {}
        self._display_count = display_count # How many cords to display, -1 for all

        # for i in range(dimensions):
        #     self.map[dimensions//2,i] = -1
        #     self.map[i,dimensions//2] = -1

    def add_cord(self,x:int|float,y:int|float):
        """Adds a cord to the map"""
        # If the cord is for example (0,90), which is north
        # Start by finding the row index
        # The row is gonna be the y value. -90 would be row 180
        # We add 90 but subtract it from 180 to get the correct row index
        # Using a min max clamp to make sure the value is within the range
        self.cords_map.setdefault(int(x),dict()) # Adding the x key
        self.cords_map[int(x)].setdefault(int(y),0) # Adding the y key
        self.cords_map[int(x)][int(y)] += 1
        self.cords_queue.put((int(x),int(y)))
        if(self._display_count == -1):
            return

        if self.cords_queue.qsize() > self._display_count:
            x,y = self.cords_queue.get()
            self.cords_map[x][y] -= 1
            if self.cords_map[x][y] == 0:
                del self.cords_map[x][y]
                if len(self.cords_map[x]) == 0:
                    del self.cords_map[x]
        


    def _get_icon(self,count:int)->str:
        """Gets correctly formatted number"""
        if count == 0:
            return "  "
        elif count < 10:
            return f"{count} "
        else:
            return f"# "

    def _get_row_list(self,width:int,value:str = "  ",center:str = "Y ")->list[str]:
        """Returns a list of strings for a row"""
        # Width should always be odd 
        list_str = ["| "] # Adding space for left border
        half_width = width//2
        list_str += [value for _ in range(half_width)]
        list_str.append(center)
        list_str += [value for _ in range(half_width)]
        list_str.append(" |")
        return list_str
    
    def _get_count(self,scaled_x:int,scaled_y:int,scale:int)->int:
        """Gets the count for a specific cord"""
        x = (scaled_x - 1) * scale
        y = (scaled_y - 1) * scale
        count = 0
        for i in range(scale):
            for j in range(scale):
                count += self.cords_map.get(x+i,{}).get(y+j,0)
        return count

    def _dict_search(self,scale:int,str_map:list[list[str]])->None:
        """Adding the cords that have been added"""
        scaled_map:dict[int,dict[int,int]] = {}
        x_cords = list(self.cords_map.keys()) # All the x cords that have been added
        for x in x_cords:
            scaled_x = x//scale
            scaled_map.setdefault(scaled_x,{})
            y_cords = list(self.cords_map[x].keys())
            for y in y_cords:
                scaled_y = y//scale
                scaled_map[scaled_x].setdefault(scaled_y,0)
                scaled_map[scaled_x][scaled_y] += 1
        for curr_x in list(scaled_map.keys()):
            for curr_y in list(scaled_map[curr_x].keys()):
                count = scaled_map[curr_x][curr_y]
                if(count == 0):
                    continue
                # We need to flip the y axis 
                # Since the grid that is drawing it is a 2d array
                # [[0 1 Y 3 4]
                #  [0 1 Y 3 4]
                #  [X X X X X]
                #  [0 1 Y 3 4]
                #  [0 1 Y 3 4]]
                # We get point (-2,2)
                # the grid is 0 indexed so we need to add half the grid size
                grid_size_scaled = 180//scale
                grid_half = grid_size_scaled//2
                grid_x = grid_size_scaled - (grid_half + curr_y)
                grid_y = grid_half + curr_x
                grid_length = len(str_map)
                # Just making sure that min index is always from 1 to grid_length-2
                grid_x = max(min(grid_x,grid_length-1),0)
                grid_y = max(min(grid_y,grid_length-1),0)
                str_map[grid_x][grid_y+1] = _get_color_string(self._get_icon(count),"green")

                
            

    


    def get_scaled_map(self,scale:int = 1)->str:
        """Returns a scaled map
        Scale is a map scale 1:1 would be 180x180
        1:10 would be 18x18
        fast: If fast is true, it will only display if there is a cord, not the count
        """
        import time
        if scale < 1:
            raise ValueError("Scale must be greater than 0")
        if scale > 45:
            raise ValueError("Scale must be less than 45")
        timer = time.time()
        print("Starting")
        scaled_ratio = (180//scale) # 1 for Axis and adding 2 for the borders
        scaled_ratio += int(scaled_ratio % 2 == 0)
        str_map:list[list[str]] = [[] for i in range(scaled_ratio)]
        for i in range(scaled_ratio):
            if(i == scaled_ratio//2):
                str_map[i] = self._get_row_list(scaled_ratio,"X ","+ ")
            else:
                str_map[i] = self._get_row_list(scaled_ratio)         
        generate_time = time.time()
        print(f"Time Taken to generate: {(generate_time - timer) *1000:.2f}ms")
        self._dict_search(scale,str_map)

        count_time = time.time()
        print(f"\tTime Taken to count: {(count_time - generate_time) *1000:.2f}ms")

        # Settings NESW directions with N,E,S,W
        new_str_map = []
        # Adding top border
        new_str_map.append(self._get_row_list(scaled_ratio,"  ","  "))
        # adding the old map
        new_str_map.extend(str_map)
        print(f"\tTime Taken to add old map: {(time.time() - count_time) *1000:.2f}ms")
        # Adding bottom border
        new_str_map.append(self._get_row_list(scaled_ratio,"  ","  "))
        # Adding the NESW directions
        new_str_map[0][scaled_ratio//2 +1] = _get_color_string("N ","red")
        new_str_map[scaled_ratio//2+1][-1] = _get_color_string("E ","red")
        new_str_map[-1][scaled_ratio//2 +1] = _get_color_string("S ","red")
        new_str_map[scaled_ratio//2+1][0] = _get_color_string("W ","red")
        print(f"Total Time Taken: {(time.time() - timer) *1000:.2f}ms")
        return "\n".join(["".join(row) for row in new_str_map])

    def __str__(self) -> str:
        return self.get_scaled_map(1)

def random_test():
    import random
    import os
    import time
    map = X_Y_Map()
    while True:
        os.system('clear')
        x = random.uniform(-90,90)
        y = random.uniform(-90,90)
        map.add_cord(x,y)
        print(map.get_scaled_map(1))
        time.sleep(0.01)

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
    # add all corners
    map.add_cord(-90,-90)
    map.add_cord(-90,90)
    map.add_cord(90,-90)
    map.add_cord(90,90)
    current_angle = 0
    while True:
        os.system('clear')
        x,y = degrees_to_coordinates(int(current_angle))
        map.add_cord(x,y)
        print(map.get_scaled_map(1))
        print(f"Angle: {current_angle:.1f}")
        print(f"X: {x:.1f} Y: {y:.1f}")
        current_angle += random.randint(1,10)
        current_angle %= 360
        input()
        #time.sleep(0.01)

def main():
    circle_test()




if __name__ == "__main__":
    main()