from src.config.GaugeBase import GaugeBase
from datetime import datetime, timedelta


class ClockGauge(GaugeBase):
    def __init__(self, master, name='Clock Gauge', title='Clock', description='', mode='clock', *args, **kwargs):
        super().__init__(master, name=name, title=title, description=description, *args, **kwargs)
        self.mode = mode  # 'clock', 'stopwatch', or 'running_time'
        self.start_time = None
        self.current_time = None

        # Label to display the time
        self.time_var = tk.StringVar(value=self.get_initial_time_display())
        self.time_label = tk.Label(self, textvariable=self.time_var, font=('Arial', 24))
        self.time_label.pack(expand=True)

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
            # If the stopwatch is just starting
            if self.start_time is None:
                self.start_time = datetime.now()
            # Calculate elapsed time
            elapsed_time = datetime.now() - self.start_time
            # Format as HH:MM:SS.sss (milliseconds)
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = elapsed_time.microseconds // 1000
            self.time_var.set(f'{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}')
        elif self.mode == 'running_time':
            # Display the running time (value should be the number of seconds elapsed)
            if value is not None:
                running_time = timedelta(seconds=value)
                self.time_var.set(str(running_time).split('.')[0])  # Format as HH:MM:SS
        else:
            raise ValueError("Invalid mode for ClockGauge.")

    def reset_stopwatch(self):
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

    # Create a ClockGauge instance for the stopwatch
    stopwatch_gauge = ClockGauge(root, title='Stopwatch', description='Elapsed Time', mode='stopwatch')
    stopwatch_gauge.pack(padx=10, pady=10)

    # Create a ClockGauge instance for the running time
    running_time_gauge = ClockGauge(root, title='Running Time', description='Video Time', mode='running_time')
    running_time_gauge.pack(padx=10, pady=10)

    video_time_seconds = 0  # This is now a global variable

    def update_clock():
        clock_gauge.update_value()
        root.after(1000, update_clock)  # Update the clock every second

    def update_stopwatch():
        stopwatch_gauge.update_value()
        root.after(100, update_stopwatch)  # Update the stopwatch every second

    def update_running_time():
        global video_time_seconds  # Declare the use of the global variable
        running_time_gauge.update_value(video_time_seconds)
        video_time_seconds += 1
        root.after(1000, update_running_time)  # Increment the running time every second

    # Start the stopwatch and running time updates
    update_clock()
    update_stopwatch()
    update_running_time()

    root.mainloop()
