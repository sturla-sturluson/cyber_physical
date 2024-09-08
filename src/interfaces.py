from typing import Protocol

class IMagneticSensor(Protocol):
    def get_x_y_z(self) -> tuple[float,float,float]:
        ...
    def get_orientation(self) -> int:
        ...
    @classmethod
    def get_NSEW_string(cls,degrees:int) -> str:
        ...