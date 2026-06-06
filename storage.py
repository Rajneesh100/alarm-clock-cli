import json
import os
from typing import List, Dict, Any

JSON_FILE = "alarms.json"

def load_alarms() -> List[Dict[str, Any]]:
    """Loads alarms from the JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []

def save_alarms(alarms: List[Dict[str, Any]]) -> None:
    """Saves the alarms list to the JSON file."""
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(alarms, f, indent=4)
    except IOError as e:
        print(f"Error saving alarms: {e}")

def get_next_id(alarms: List[Dict[str, Any]]) -> int:
    """Generates the next incremental integer ID."""
    if not alarms:
        return 1
    return max(alarm.get("id", 0) for alarm in alarms) + 1
