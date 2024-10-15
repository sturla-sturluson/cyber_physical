from pathlib import Path
import os
from dotenv import load_dotenv


_DIR_PATH = "~/.config/cyber_physical_systems"
Path(_DIR_PATH).expanduser().mkdir(parents=True, exist_ok=True)
CONFIG_DIR = Path(_DIR_PATH).expanduser()
COMPASS_CALIBRATION_FILE_PATH = Path(CONFIG_DIR) / "compass_calibration.json"
RANGE_CALIBRATION_FILE_PATH = Path(CONFIG_DIR) / "range_calibration.json"

ENV_PATH = Path(Path.cwd()) / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# The led pin
DEFAULT_LED_PIN=26
# Range sensor gpio pin
DEFAULT_RANGE_SENSOR_PIN=5
# Engine gpio pins
DEFAULT_AIN1_PIN=20
DEFAULT_AIN2_PIN=21
DEFAULT_BIN1_PIN=6
DEFAULT_BIN2_PIN=13
# The motor controller sleep pin
DEFAULT_SLEEP_PIN=25

# PS4 Controller constants
DEFAULT_PS4_DEADZONE = 0.1

# Read the .env file for the pin number

LED_PIN = int(os.getenv("LED_PIN", None))
RANGE_SENSOR_PIN = int(os.getenv("RANGE_SENSOR_PIN", None))
AIN1_PIN = int(os.getenv("AIN1_PIN", None))
AIN2_PIN = int(os.getenv("AIN2_PIN", None))
BIN1_PIN = int(os.getenv("BIN1_PIN", None))
BIN2_PIN = int(os.getenv("BIN2_PIN", None))
SLEEP_PIN = int(os.getenv("SLEEP_PIN", None))
PS4_DEADZONE = float(os.getenv("PS4_DEADZONE", DEFAULT_PS4_DEADZONE))
print("PINS USED:")
for pin_name,pin in zip(["LED_PIN","RANGE_SENSOR_PIN","AIN1_PIN","AIN2_PIN","BIN1_PIN","BIN2_PIN","SLEEP_PIN"],[LED_PIN,RANGE_SENSOR_PIN,AIN1_PIN,AIN2_PIN,BIN1_PIN,BIN2_PIN,SLEEP_PIN]):
    print(f"{pin_name}: {pin}")


# Motors constants

MAX_SPEED = 100
MIN_SPEED = -100

MAX_DUTY_CYCLE = 100
MIN_DUTY_CYCLE = 0