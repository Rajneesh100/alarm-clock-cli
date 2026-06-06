from datetime import datetime
import storage

def validate_time(time_str: str) -> bool:
    """Validates if time_str is in strict 24-hour format 'HH:MM'."""
    if len(time_str) != 5 or time_str[2] != ':':
        return False
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def add_alarm(time_str: str, message: str) -> None:
    """Validates, creates, and saves a new alarm."""
    if not validate_time(time_str):
        print(f"Error: Invalid time format '{time_str}'. Please use 24-hour format HH:MM (e.g., 14:30).")
        return

    alarms = storage.load_alarms()
    alarm_id = storage.get_next_id(alarms)
    
    new_alarm = {
        "id": alarm_id,
        "time": time_str,
        "message": message
    }
    alarms.append(new_alarm)
    storage.save_alarms(alarms)
    print(f"Alarm {alarm_id} added for {time_str} - '{message}'")

def list_alarms() -> None:
    """Lists all configured alarms."""
    alarms = storage.load_alarms()
    if not alarms:
        print("No alarms scheduled.")
        return

    print(f"{'ID':<5} {'Time':<8} {'Message'}")
    print("-" * 30)
    for alarm in alarms:
        alarm_id = alarm.get("id")
        time_str = alarm.get("time")
        message = alarm.get("message", "")
        print(f"{alarm_id:<5} {time_str:<8} {message}")

def delete_alarm(alarm_id_str: str) -> None:
    """Deletes an alarm by ID."""
    try:
        alarm_id = int(alarm_id_str)
    except ValueError:
        print(f"Error: Invalid alarm ID '{alarm_id_str}'. ID must be an integer.")
        return

    alarms = storage.load_alarms()
    filtered_alarms = [a for a in alarms if a.get("id") != alarm_id]
    
    if len(filtered_alarms) == len(alarms):
        print(f"Error: Alarm with ID {alarm_id} not found.")
        return

    storage.save_alarms(filtered_alarms)
    print(f"Alarm {alarm_id} deleted successfully.")
