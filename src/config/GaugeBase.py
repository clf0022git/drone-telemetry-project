import tkinter as tk


class GaugeBase(tk.Frame):
    def __init__(self, master, name='Default Gauge', title='Gauge', description='', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name
        self.title_text = title
        self.description_text = description
        self.color_ranges = {'blue': 25, 'green': 50, 'yellow': 75, 'red': 100}  # Default values, use update_colors to change
        self.red_limit = 80
        self.alarm_times = 0  # Number of times the alarm has been triggered

        # Create the title label
        self.title_label = tk.Label(self, text=self.title_text)
        self.title_label.pack(side=tk.TOP, fill=tk.X)

        # Create the description label
        self.description_label = tk.Label(self, text=self.description_text)
        self.description_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_value(self, value):
        """Update the gauge's value."""
        raise NotImplementedError("Must be implemented by the subclass.")

    def update_colors(self, blue=None, green=None, yellow=None, red=None):
        """Update the color ranges for the gauge."""
        if blue is not None:
            self.color_ranges['blue'] = blue
        if green is not None:
            self.color_ranges['green'] = green
        if yellow is not None:
            self.color_ranges['yellow'] = yellow
        if red is not None:
            self.color_ranges['red'] = red
            self.red_limit = int(red - 20)  # Set the red limit to 20 less than the red color range

    def check_alarm(self, value):
        """Check if the value exceeds the red limit and trigger an alarm if necessary."""
        if value >= self.red_limit:
            self.trigger_alarm()

    def trigger_alarm(self):
        """Trigger an audible alarm."""
        self.alarm_times += 1
        print(f"Alarm! {self.name} value exceeded red limit {self.alarm_times} times.")  # Placeholder for actual alarm logic
        self.master.bell()  # Ring the system bell

    def set_title(self, title):
        """Set the title of the gauge."""
        self.title_text = title
        self.title_label.config(text=self.title_text)

    def set_description(self, description):
        """Set the description for the gauge."""
        self.description_text = description
        self.description_label.config(text=self.description_text)


# Example gauge subclass
if __name__ == "__main__":
    class NumberDisplayGauge(GaugeBase):
        def __init__(self, master, name='Number Display', *args, **kwargs):
            super().__init__(master, name=name, *args, **kwargs)
            self.display_var = tk.StringVar()
            self.display_label = tk.Label(self, textvariable=self.display_var, font=('Arial', 24))
            self.display_label.pack(expand=True)

        def update_value(self, value):
            """Update the displayed number."""
            self.display_var.set(value)
            self.check_alarm(value)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gauge Example")

    number_gauge = NumberDisplayGauge(root, title='Speed', description='km/h')
    number_gauge.pack(padx=10, pady=10)
    number_gauge.update_value(42)  # Update value example

    root.mainloop()
