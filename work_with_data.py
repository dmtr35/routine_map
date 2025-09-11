import json
from pathlib import Path
from month_grid import date

filename = Path("routine_data.json")

def load_data():
    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    else:
        data = {}
        return data


def add_date(cell, key, full_data):
    date_str = date(cell)
    full_data[key].append(date_str)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=4)


def delete_date(cell, key, full_data):
    date_str = date(cell)
    full_data[key].remove(date_str)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=4)

def delete_row(key, full_data):
    del full_data[key]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=4)