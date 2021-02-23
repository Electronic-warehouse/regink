import sys
import re
from os import path, getenv, environ
from pathlib import Path

# don't change these variables
CWD = path.abspath(".")
ENTRY_POINT = sys.argv[0]
DIR_NAME = Path(path.dirname(__file__))
DIR_ENTRY = path.dirname(ENTRY_POINT)
SERVICE_DIR = path.join(CWD, DIR_ENTRY) \
    if re.match("^.*py$", ENTRY_POINT)   \
    else path.join(CWD, ENTRY_POINT)
sys.path.append(SERVICE_DIR)

STATIC_DIR = path.join(SERVICE_DIR, "static")

CLIENT_CONFIG = {
    'host': '127.0.0.1',
    'port': 5000,
}

BASE_CONFIG = {
    'BASE_URL': '/',
}

DIRS = {
    'upload': './files'
}

SERVER_CONFIG = {
    "debug": True,
    "host": "127.0.0.1",
    "port": 9991
}

SQLITE = {
    "file": DIR_NAME / "db" / "warehouse.db"
}
