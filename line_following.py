import time
import RPi.GPIO as GPIO
from adafruit_tcs34725 import TCS34725
from src.motor import Motors, CarRunner

# Setup GPIO for motors
GPIO.setmode(GPIO.BCM)

# Initialize motor driver and color sensor
motors = Motors()
car_runner = CarRunner()
color_sensor = TCS34725()  # Initialize color sensor with your specific bus
IR_SENSOR_PIN = 4  # GPIO pin connected to IR sensor
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

# Define line color threshold (modify these with calibrated values)
TARGET_COLOR = {"red": 100, "green": 50, "blue": 50}
COLOR_TOLERANCE = {"red": 15, "green": 15, "blue": 15}

# Movement functions
def stop():
    car_runner.motor_stop()

def move_forward():
    car_runner.set_speed(forward_motion=20)  # Adjust speed for slow precision

def turn_left():
    car_runner.set_speed(forward_motion=20, turning_motion=-20)

def turn_right():
    car_runner.set_speed(forward_motion=20, turning_motion=20)

# Helper function to check if color is within target color range
def is_on_target_line():
    color = color_sensor.color_raw
    return (TARGET_COLOR["red"] - COLOR_TOLERANCE["red"] <= color.red <= TARGET_COLOR["red"] + COLOR_TOLERANCE["red"] and
            TARGET_COLOR["green"] - COLOR_TOLERANCE["green"] <= color.green <= TARGET_COLOR["green"] + COLOR_TOLERANCE["green"] and
            TARGET_COLOR["blue"] - COLOR_TOLERANCE["blue"] <= color.blue <= TARGET_COLOR["blue"] + COLOR_TOLERANCE["blue"])

# Helper function to check boundary
def is_near_boundary():
    return GPIO.input(IR_SENSOR_PIN) == GPIO.LOW  # Adjust based on IR sensor's active state

# Main loop
try:
    while True:
        # Check if on line
        if is_on_target_line():
            move_forward()
        else:
            # If off line, adjust direction to search for line
            stop()
            time.sleep(0.2)
            
            # Rotate slowly to find the line again
            turn_left()
            time.sleep(0.1)  # Adjust duration for gradual left search
            if is_on_target_line():
                continue  # Resume forward if line is found
            
            turn_right()
            time.sleep(0.2)  # Rotate to the right for longer if not found on left
            if is_on_target_line():
                continue  # Resume forward if line is found

        # Check if near boundary
        if is_near_boundary():
            stop()
            print("Boundary detected! Stopping...")
            break  # Optionally add more logic to reverse or turn back
            
        time.sleep(0.05)  # Adjust delay for control sensitivity

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    motors.cleanup()
    GPIO.cleanup()