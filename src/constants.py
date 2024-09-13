
from pathlib import Path
_DIR_PATH = "~/.config/cyber_physical_systems"
Path(_DIR_PATH).expanduser().mkdir(parents=True, exist_ok=True)
CONFIG_DIR = Path(_DIR_PATH).expanduser()
CALIBRATION_FILE_PATH = Path(CONFIG_DIR) / "compass_calibration.json"
