import bluetooth
import time
from src.motor.motors import Motors

# Setup for motor control
motors = Motors()

# Bluetooth connection to master car
server_mac_address = "XX:XX:XX:XX:XX:XX"  # Replace with your lead car's MAC address
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_mac_address, port))

try:
    while True:
        data = sock.recv(1024).decode('utf-8')  # Receiving command from the lead car
        if data:
            if data == "forward":
                motors.set_throttle(0.5, 0.5)  # Adjust as needed
            elif data == "left":
                motors.set_throttle(0.3, 0.5)
            elif data == "right":
                motors.set_throttle(0.5, 0.3)
            elif data == "stop":
                motors.set_throttle(0, 0)
            else:
                print("Unknown command:", data)
        time.sleep(0.1)  # Adjust delay as needed

except KeyboardInterrupt:
    sock.close()
    motors.set_throttle(0, 0)
    print("Connection closed, car stopped.")