import tkinter as tk
from src.config.GaugeBase import GaugeBase


class LightIndicatorGauge(GaugeBase):
    def __init__(self, master, name='Light Indicator', title='Light', description='', *args, **kwargs):
        super().__init__(master, name=name, title=title, description=description, *args, **kwargs)

        # Canvas for the light indicator
        self.light_canvas = tk.Canvas(self, width=60, height=60, bg='white')
        self.light_canvas.pack()

        # Draw the initial light indicator (off)
        self.light = self.light_canvas.create_oval(10, 10, 50, 50, fill='grey')
        self.is_on = False

    def update_value(self, value):
        """Toggle the light on or off based on the value."""
        self.is_on = value
        self.light_canvas.itemconfig(self.light, fill='green' if self.is_on else 'grey')

    def toggle_light(self):
        """Toggle the light state."""
        self.update_value(not self.is_on)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Light Indicator Example")

    light_gauge = LightIndicatorGauge(root, title='Power Status', description='System Power')
    light_gauge.pack(padx=10, pady=10)

    # Button to toggle the light on/off
    toggle_button = tk.Button(root, text="Toggle Light", command=light_gauge.toggle_light)
    toggle_button.pack(pady=5)

    root.mainloop()
