from src import CarRunner
import asyncio
import threading
import os
import sys
import tty
import termios
import datetime as dt



def standard_in_key_listener(key_map):
    """Listen for key presses and call appropriate functions from key_map."""
    print("Press keys (press 'q' to quit)")
    
    # Save the original terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        # Set the terminal to raw mode to capture key presses immediately
        tty.setraw(sys.stdin.fileno())

        while True:
            # Read a single character from stdin (without waiting for Enter)
            key = sys.stdin.read(1).lower()

            if key in key_map:
                key_map[key]()           
            if key == "q":
                break
    finally:
        # Restore the original terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

async def launch_key_listener(key_map):
    """Launch a key listener in a separate thread."""
    threading.Thread(target=standard_in_key_listener, args=(key_map,), daemon=True).start()

        

def main():
    motor_2_gpio_1 = 6
    motor_2_gpio_2 = 13
    motor_1_gpio_1 = 20
    motor_1_gpio_2 = 21

    with CarRunner((motor_1_gpio_1,motor_1_gpio_2),(motor_2_gpio_1,motor_2_gpio_2)) as car_runner:
        key_map = {
            "w" :lambda: car_runner.speed_up(),
            "s" :lambda: car_runner.speed_down(),
            "q" :lambda: car_runner.shut_down(),
            " " :lambda: car_runner.motor_stop(),
        }

            
        # Launch the key listener in a separate thread
        asyncio.run(launch_key_listener(key_map))
        # Start the motor loop
        asyncio.run(car_runner.motor_loop())

if __name__ == "__main__":
    main()