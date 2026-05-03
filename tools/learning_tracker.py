import json
from pathlib import Path

from backend.storage import atomic_write_json

FILE = "learning_progress.json"


def track_learning(event):

    data = []

    if Path(FILE).exists():

        with open(FILE, "r") as f:
            data = json.load(f)

    data.append(event)

    atomic_write_json(FILE, data)
