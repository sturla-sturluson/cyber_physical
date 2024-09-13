from ..interfaces import IMagneticSensor
import random

class FakeMagneticSensor(IMagneticSensor):
    """Fake magnetic sensor for testing"""
    def get_x_y_z(self) -> tuple[float,float,float]:
        return random.uniform(-90,90),random.uniform(-90,90),random.uniform(-90,90)