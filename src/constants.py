from pathlib import Path
import os


_DIR_PATH = "~/.config/cyber_physical_systems"
Path(_DIR_PATH).expanduser().mkdir(parents=True, exist_ok=True)
CONFIG_DIR = Path(_DIR_PATH).expanduser()
COMPASS_CALIBRATION_FILE_PATH = Path(CONFIG_DIR) / "compass_calibration.json"
RANGE_CALIBRATION_FILE_PATH = Path(CONFIG_DIR) / "range_calibration.json"

DEFAULT_LED_PIN = 26
# Read the .env file for the pin number
try:
    LED_PIN_NUMBER = int(os.getenv("LED_PIN_NUMBER", DEFAULT_LED_PIN))
except ValueError:
    LED_PIN_NUMBER = DEFAULT_LED_PIN

                   