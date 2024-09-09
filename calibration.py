import time
import board
import busio
import adafruit_lsm303dlh_mag

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the magnetometer
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

# Initialize min/max values
MagMinX = float('inf')
MagMaxX = float('-inf')
MagMinY = float('inf')
MagMaxY = float('-inf')
MagMinZ = float('inf')
MagMaxZ = float('-inf')

# Last time the display was updated
last_display_time = time.monotonic()

# Main loop for calibrating the magnetometer
while True:
    # Read magnetometer values
    mag_x, mag_y, mag_z = mag.magnetic

    # Update the min/max calibration values
    MagMinX = min(MagMinX, mag_x)
    MagMaxX = max(MagMaxX, mag_x)
    MagMinY = min(MagMinY, mag_y)
    MagMaxY = max(MagMaxY, mag_y)
    MagMinZ = min(MagMinZ, mag_z)
    MagMaxZ = max(MagMaxZ, mag_z)

    # Display every second
    if (time.monotonic() - last_display_time) > 1.0:
        print(f"Mag Minimums: {MagMinX:.2f}  {MagMinY:.2f}  {MagMinZ:.2f}")
        print(f"Mag Maximums: {MagMaxX:.2f}  {MagMaxY:.2f}  {MagMaxZ:.2f}")
        print()
        last_display_time = time.monotonic()

    # Sleep for a short time to avoid flooding the output
    time.sleep(0.1)