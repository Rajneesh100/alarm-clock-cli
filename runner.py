import time
from datetime import datetime
import storage

def check_alarms(current_time: str, alarms: list) -> list:
    """Returns a list of alarms that match the current_time."""
    triggered = []
    for alarm in alarms:
        if alarm.get("time") == current_time:
            triggered.append(alarm)
    return triggered

def run_loop() -> None:
    """Runs the background alarm-monitoring loop."""
    print("Alarm daemon started. Polling every 10 seconds...")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M")
            alarms = storage.load_alarms()
            triggered = check_alarms(current_time, alarms)
            
            for alarm in triggered:
                alarm_id = alarm.get("id")
                message = alarm.get("message", "")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TRIGGERED: Alarm {alarm_id} ({current_time}) - {message}")
            
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nAlarm daemon stopped.")
