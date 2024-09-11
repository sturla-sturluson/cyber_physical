# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# from adafruit_ssd1306 import SSD1306_I2C



# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
i2c = board.I2C()
# oled = SSD1306_I2C(128, 64, i2c)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

while True:
    # oled.fill(0)
    # oled.text(f"Raw ADC Value: {chan0.value}", 0, 0, 255)
    # oled.text(f"ADC Voltage: {chan0.voltage:.2f}", 0, 10, 255)
    # oled.show()
    os.system('clear')
    print(f"Raw ADC Value: {chan0.value} ADC Voltage: {chan0.voltage:.2f}")
    time.sleep(0.5)