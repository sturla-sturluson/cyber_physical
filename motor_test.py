from src.motor.ps4_listener import run_car
from src.motor import Motors
import pygame
import os





def main():
    ain1,ain2 = 20,21
    bin1,bin2 = 6,13
    with Motors((ain1,ain2),(bin1,bin2)) as motors:
        run_car(motors)
    


if __name__ == "__main__":
    main()