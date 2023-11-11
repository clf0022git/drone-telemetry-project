from src.config.GaugeBase import GaugeBase
from datetime import datetime, timedelta


class ClockGauge(GaugeBase):
    def __init__(self, master, name='Clock Gauge', title='Clock', description='', mode='clock', *args, **kwargs):
        super().__init__(master, name=name, title=title, description=description, *args, **kwargs)
        self.mode = mode  # 'clock', 'stopwatch', 'running_time', or 'clock_csv'
        self.start_time = None
        self.current_time = None

        # Label to display the time
        self.time_var = tk.StringVar(value=self.get_initial_time_display())
        self.time_label = tk.Label(self, textvariable=self.time_var, font=('Arial', 24))
        self.time_label.pack(expand=True)

        # Cases for stopwatch mode
        self.running = False
        self.elapsed_time_at_pause = timedelta(0)

        # Label to display the date for clock_csv mode
        self.date_var = tk.StringVar(value="")
        self.date_label = tk.Label(self, textvariable=self.date_var, font=('Arial', 16))
        self.date_label.pack()

    def get_initial_time_display(self):
        if self.mode == 'clock':
            return datetime.now().strftime("%H:%M:%S")
        else:
            return "00:00:00"

    def update_value(self, value=None):
        if self.mode == 'clock':
            # Display the current time
            now = datetime.now()
            self.time_var.set(now.strftime("%H:%M:%S"))
        elif self.mode == 'stopwatch':
            if self.running:
                # If the stopwatch is just starting
                if self.start_time is None:
                    self.start_time = datetime.now()
                # Calculate elapsed time
                elapsed_time = datetime.now() - self.start_time
                # Format as HH:MM:SS.sss (milliseconds)
                # We don't have strftime() for timedelta, so we have to do this manually
                hours, remainder = divmod(elapsed_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                milliseconds = elapsed_time.microseconds // 1000
                self.time_var.set(f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}')
        elif self.mode == 'running_time':
            # Display the running time (value should be the number of seconds elapsed)
            if value is not None:
                running_time = timedelta(seconds=value)
                self.time_var.set(str(running_time).split('.')[0])  # Format as HH:MM:SS
        elif self.mode == 'clock_csv':
            # Expecting value in the format "MM/DD/YYYY HH:MM:SS"
            try:
                date_time_obj = datetime.strptime(value, "%m/%d/%Y %H:%M:%S")
                self.time_var.set(date_time_obj.strftime("%H:%M:%S"))
                self.date_var.set(date_time_obj.strftime("%m/%d/%Y"))
            except ValueError as e:
                print(f"Value provided is not in the expected format: {e}")
        else:
            raise ValueError("Invalid mode for ClockGauge.")

    def reset_stopwatch(self):
        self.start_time = None

    def toggle_stopwatch(self):
        """Toggle the stopwatch start/pause."""
        if self.running:
            self.pause_stopwatch()
        else:
            self.start_stopwatch()

    def start_stopwatch(self):
        """Start the stopwatch."""
        if not self.running:
            self.running = True
            if self.start_time is None:
                self.start_time = datetime.now() - self.elapsed_time_at_pause
            self.update_value()

    def pause_stopwatch(self):
        """Pause the stopwatch."""
        if self.running:
            self.running = False
            self.elapsed_time_at_pause = datetime.now() - self.start_time
            self.start_time = None

    def set_mode(self, mode):
        self.mode = mode
        self.reset_stopwatch()
        self.time_var.set(self.get_initial_time_display())


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.title("Clock Display Gauge Example")

    # Create a ClockGauge instance for the clock
    clock_gauge = ClockGauge(root, title='Current Time', description='Local Time')
    clock_gauge.pack(padx=10, pady=10)

    # Create a ClockGauge instance for clock time from a CSV file
    csv_clock_gauge = ClockGauge(root, title='CSV Clock', mode='clock_csv')
    csv_clock_gauge.pack(padx=10, pady=10)

    # Create a ClockGauge instance for the stopwatch
    stopwatch_gauge = ClockGauge(root, title='Stopwatch', description='Elapsed Time', mode='stopwatch')
    stopwatch_gauge.pack(padx=10, pady=10)

    # Button to toggle the stopwatch start/pause
    toggle_button = tk.Button(root, text="Start/Stop", command=stopwatch_gauge.toggle_stopwatch)
    toggle_button.pack(pady=5)

    # Create a ClockGauge instance for the running time
    running_time_gauge = ClockGauge(root, title='Running Time', description='Video Time', mode='running_time')
    running_time_gauge.pack(padx=10, pady=10)

    video_time_seconds = 0

    def update_clock():
        clock_gauge.update_value()
        root.after(1000, update_clock)  # Update the clock every second

    def update_stopwatch():
        if stopwatch_gauge.running:
            stopwatch_gauge.update_value()
        root.after(100, update_stopwatch)  # Update the stopwatch every 100 milliseconds

    def update_running_time():
        global video_time_seconds
        running_time_gauge.update_value(video_time_seconds)
        video_time_seconds += 1
        root.after(1000, update_running_time)  # Increment the running time every second

    # Start the updates
    update_clock()

    # Update the clock with a value from a CSV file (format: "MM/DD/YYYY HH:MM:SS")
    csv_time_str = "1/25/2020 20:08:03"
    csv_clock_gauge.update_value(csv_time_str)

    update_stopwatch()

    update_running_time()

    root.mainloop()
