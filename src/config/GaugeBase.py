import tkinter as tk


class GaugeBase(tk.Frame):
    def __init__(self, master, name='Default Gauge', title='Gauge', description='', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name
        self.title_text = title
        self.description_text = description
        self.color_ranges = {'blue': (0, 25), 'green': (25, 50), 'yellow': (50, 75), 'red': (75, 90)}  # Default values, use update_colors to change
        self.red_limit = int(self.color_ranges['red'][1] + 1)  # Value at which the alarm is triggered (default is 1 above the red limit)
        self.alarm_times = 0  # Number of times the alarm has been triggered

        # Create the title label
        self.title_label = tk.Label(self, text=self.title_text)
        self.title_label.pack(side=tk.TOP, fill=tk.X)

        # Create the description label
        self.description_label = tk.Label(self, text=self.description_text)
        self.description_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Create the alarm label
        self.alarm_label = tk.Label(self, text='ALARM!', fg='red')
        self.alarm_label_visible = False

    def update_value(self, value):
        """Update the gauge's value."""
        raise NotImplementedError("Must be implemented by the subclass.")

    def update_colors(self, blue=None, green=None, yellow=None, red=None, red_limit=None):
        """Update the color ranges for the gauge."""
        # Update each color range
        if blue is not None:
            self.color_ranges['blue'] = blue if isinstance(blue, tuple) else (0, blue)
        if green is not None:
            self.color_ranges['green'] = green if isinstance(green, tuple) else (self.color_ranges['blue'][1], green)
        if yellow is not None:
            self.color_ranges['yellow'] = yellow if isinstance(yellow, tuple) else (self.color_ranges['green'][1], yellow)
        if red is not None:
            self.color_ranges['red'] = red if isinstance(red, tuple) else (self.color_ranges['yellow'][1], red)

        # Update the red limit
        if red_limit is not None:
            self.red_limit = red_limit
        else:
            self.red_limit = int(self.color_ranges['red'][1] + 1)  # Default to 1 above the upper bound of the red range

    def set_alarm_threshold(self, threshold):
        """Set the alarm threshold for the gauge."""
        self.red_limit = threshold

    def check_alarm(self, value):
        """Check if the value exceeds the red limit and trigger an alarm if necessary."""
        if value >= self.red_limit:
            self.trigger_alarm()

    def trigger_alarm(self):
        """Trigger an audible alarm and flash the description label."""
        self.alarm_times += 1
        print(f"Alarm! {self.name} value exceeded red limit {self.alarm_times} times.")  # Placeholder for actual alarm logic
        self.master.bell()  # Ring the system bell
        self.flash_alarm_text()  # Flash the alarm text

    def flash_alarm_text(self, count=1):
        """Flash the alarm text in the alarm label."""
        if count > 0:
            # Toggle the visibility of the alarm label
            if self.alarm_label_visible:
                self.alarm_label.pack_forget()
                self.alarm_label_visible = False
            else:
                self.alarm_label.pack(side=tk.BOTTOM, fill=tk.X)
                self.alarm_label_visible = True
            # Schedule the next flash
            self.after(800, self.flash_alarm_text, count - 1)
        else:
            # Ensure the alarm label is hidden after flashing
            self.alarm_label.pack_forget()
            self.alarm_label_visible = False

    def set_title(self, title):
        """Set the title of the gauge."""
        self.title_text = title
        self.title_label.config(text=self.title_text)

    def set_description(self, description):
        """Set the description for the gauge."""
        self.description_text = description
        self.description_label.config(text=self.description_text)

    def resize(self, width, height):
        """Resize the gauge/frame to the given dimensions."""
        self.config(width=width, height=height)
        self.pack_propagate(False)  # Prevents the frame from resizing to fit its contents


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
    number_gauge.resize(200, 100)  # Resize example

    root.mainloop()
