import json
from pathlib import Path

filename = Path("routine_data.json")

def load_data():
    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    else:
        data = {}
        return data


def save_data(data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
