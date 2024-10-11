from .common import get_clamped_dead_zone

class PS4Button:
    type:str   # Button or Axis
    id:int     # Button or Axis id
    value:int|float  # Value of the button or axis
    # Button or Axis name
    name:str
    # Min and Max values for the axis
    released:int
    min:int
    max:int
    def __init__(self,type:str,id:int,name:str,released:int=0,min:int=0,max:int=1):
        self.type = type
        self.id = id
        self.value = released
        self.name = name
        self.released = released
        self.min = min
        self.max = max
    def __str__(self):
        if(self.type == "Button"):
            return f"{self.name} : {self.value>0 if 'Pressed' else 'Released'}"
        return f"{self.name} : {self.value}"
    
    def set_value(self,value:int|float,dead_zone:float):
        self.value = get_clamped_dead_zone(value,dead_zone,self.released)
    
    @property
    def is_pressed(self):
        return self.value != self.released
    
    def get_normalized_value(self,min:int=0,max:int=100)->int:
        """Returns the value normalized between min and max"""
        curr_range_value = self.max - self.min
        normalize_range_value = max - min
        normalized_value = (self.value - self.min) / curr_range_value
        return int(min + (normalized_value * normalize_range_value))
