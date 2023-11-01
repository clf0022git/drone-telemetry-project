import sys
import traceback
from src.gui.window import MainWindow


def main():
    """
    Entry point for the Drone Telemetry Playback application.
    Initializes and runs the main GUI window.
    (Add more details here as needed)
    """
    try:
        root = MainWindow()
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
