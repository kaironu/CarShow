import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showroom.settings")

from showroom.wsgi import application

app = application
