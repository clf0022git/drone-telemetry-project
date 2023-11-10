from src.config.GaugeBase import GaugeBase


class NumberDisplay(GaugeBase):
    def __init__(self, master, name='Default', **kwargs):
        super().__init__(master, name, **kwargs)
        self.display_value = self.canvas.create_text(150, 150, text='', font=('Arial', 48))

    def update_value(self, value):
        # Check for alarm conditions
        self.check_alarm(value)

        # Update the display with the new value and color based on the value
        color = self.get_color_for_value(value)
        self.canvas.itemconfig(self.display_value, text=str(value), fill=color)

    def get_color_for_value(self, value):
        for color, (lower, upper) in self.color_ranges.items():
            if lower is None and value < upper:
                return color
            if upper is None and value >= lower:
                return color
            if lower is not None and upper is not None and lower <= value < upper:
                return color
        return 'black'  # Default color if no range is matched


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    number_display = NumberDisplay(root, name="Numeric Display")
    number_display.set_color_ranges(blue=25, green=50, yellow=75, red=100)

    # Function to update the display over time
    def update_display(value):
        number_display.update_value(value)
        if value < 100:  # Increment the value until it reaches 100
            root.after(200, update_display, value + 1)
        else:
            root.after(200, update_display, 0)  # Reset the value after it reaches 100

    # Start updating the display
    update_display(0)

    root.mainloop()
