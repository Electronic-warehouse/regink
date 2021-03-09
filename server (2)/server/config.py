import json
import os
from pathlib import Path

_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
_FILE_NAME = Path("config.json")
CONFIG = {"work_dir": str(_PATH)}


with open(_PATH / _FILE_NAME) as fp:
    CONFIG.update(json.load(fp))

__all__ = ["CONFIG"]
