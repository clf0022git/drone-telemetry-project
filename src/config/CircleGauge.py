import tkinter as tk
from src.config.GaugeBase import GaugeBase
from math import pi, cos, sin


class CircleGauge(GaugeBase):
    def __init__(self, master, name='Circle Gauge', title='Circle Gauge', description='', degrees=360, *args, **kwargs):
        super().__init__(master, name=name, title=title, description=description, *args, **kwargs)
        self.degrees = degrees
        self.value = 0
        self.max_value = 100  # Default max value for the gauge

        # Canvas for drawing the gauge
        self.gauge_canvas = tk.Canvas(self, width=200, height=200, bg='white')
        self.gauge_canvas.pack()

        # Needle to indicate the value
        self.needle_length = 90
        self.needle = self.gauge_canvas.create_line(100, 100, 100 + self.needle_length, 100, arrow=tk.LAST)

        # Adjust the start angle based on the degrees
        #start_angle = 90 + ((360 - degrees) / 2)
        #self.arc = self.gauge_canvas.create_arc(10, 10, 190, 190, start=start_angle, extent=-degrees, style='arc')

        # Adjust the starting angle based on the degrees
        if degrees == 360:
            start_angle = 90  # Start from the left (9 o'clock position)
        else:
            start_angle = -90  # For a semi-circle, start from the top (12 o'clock position)

        self.arc = self.gauge_canvas.create_arc(10, 10, 190, 190, start=start_angle, extent=degrees, style='arc')

    def update_value(self, value):
        """Update the gauge's value and redraw the needle."""
        self.value = value
        self.check_alarm(value)
        # Adjust the angle calculation for the new orientation
        angle_rad = (pi / 2) - (value / self.max_value) * (self.degrees * pi / 180)
        if self.degrees == 180:
            # For a 180-degree gauge, we adjust the angle calculation
            angle_rad += pi / 2
        x = 100 + self.needle_length * cos(angle_rad)
        y = 100 - self.needle_length * sin(angle_rad)
        self.gauge_canvas.coords(self.needle, 100, 100, x, y)
        self.update_gauge_color(value)

    def update_gauge_color(self, value):
        """Change the gauge color based on the value."""
        if value >= self.red_limit:
            color = 'red'
        elif value >= self.color_ranges['yellow']:
            color = 'yellow'
        elif value >= self.color_ranges['green']:
            color = 'green'
        else:
            color = 'blue'
        self.gauge_canvas.itemconfig(self.arc, outline=color)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circle Gauge Example")

    circle_gauge = CircleGauge(root, title='Speed', degrees=180)
    circle_gauge.pack(padx=10, pady=10)
    circle_gauge.update_value(10)  # Update to a sample value

    root.mainloop()
