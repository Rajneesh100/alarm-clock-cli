import sys
import manager
import runner

def print_usage() -> None:
    """Prints standard help and usage information."""
    print("Usage:")
    print("  python main.py run                  - Start the background alarm monitor daemon")
    print("  python main.py add <time> <message> - Add a new alarm (e.g., add 14:30 'Wake up')")
    print("  python main.py list                 - List all alarms")
    print("  python main.py delete <id>          - Delete an alarm by ID")

def main() -> None:
    """Main CLI driver function."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "run":
        runner.run_loop()
    elif command == "add":
        if len(sys.argv) < 4:
            print("Error: Missing time or message.")
            print("Usage: python main.py add <time> <message>")
            sys.exit(1)
        time_str = sys.argv[2]
        message = sys.argv[3]
        manager.add_alarm(time_str, message)
    elif command == "list":
        manager.list_alarms()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Missing alarm ID.")
            print("Usage: python main.py delete <id>")
            sys.exit(1)
        alarm_id_str = sys.argv[2]
        manager.delete_alarm(alarm_id_str)
    else:
        print(f"Unknown command: '{command}'")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
