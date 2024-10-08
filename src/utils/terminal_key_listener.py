import sys
import tty
import termios
import threading


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

