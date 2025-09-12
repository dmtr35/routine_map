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

def add_row(new_key, full_data):
    if new_key in full_data:
        return
    
    full_data[new_key] = []
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=4)
    return full_data

def rename_row(new_key, key, full_data):
    if not new_key or new_key in full_data:
        return
    
    full_data[new_key] = full_data[key]
    keys = list(full_data.keys())
    idx = keys.index(key)
    
    keys[idx], keys[len(keys) - 1] = keys[len(keys) - 1], keys[idx]
    del keys[len(keys) - 1]
    new_data = {k: full_data[k] for k in keys}

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4)
    return new_data

def move_up_row(key, full_data):
    keys = list(full_data.keys())
    if key not in keys:
        return
    
    idx = keys.index(key)
    if idx == 0:
        return
    
    keys[idx - 1], keys[idx] = keys[idx], keys[idx - 1]
    new_data = {k: full_data[k] for k in keys}

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4)
    return new_data

def move_down_row(key, full_data):
    keys = list(full_data.keys())
    if key not in keys:
        return
    
    idx = keys.index(key)
    if idx == len(keys) - 1:
        return
    
    keys[idx + 1], keys[idx] = keys[idx], keys[idx + 1]
    new_data = {k: full_data[k] for k in keys}

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4)
    return new_data