from src.motor import Motor
import os
import threading
import asyncio


def main():
    a1 = 6
    a2 = 13
    

    with Motor(a1,a2) as right_motor:
        asyncio.run(right_motor.motor_loop())
            
        


if __name__ == '__main__':
    main()