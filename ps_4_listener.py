from src.ps4_controller import PS4Listener
from src.motor import Motors
import pygame
import os





def main():
    ain1,ain2 = 20,21
    bin1,bin2 = 6,13
    with Motors((ain1,ain2),(bin1,bin2)) as motors:
        listener = PS4Listener(motors)

    


if __name__ == "__main__":
    main()