from src.config.GaugeBase import GaugeBase
import math


class CircleGauge(GaugeBase):
    def __init__(self, master, angle=360, name='Default', **kwargs):
        super().__init__(master, name)
        self.angle = angle
        self.width = self.canvas.winfo_reqwidth()
        self.height = self.canvas.winfo_reqheight()
        self.value = 0
        self.colors = {
            "blue": 25,
            "green": 50,
            "yellow": 75,
            "red": 100
        }
        self.draw_gauge()

    def draw_gauge(self):
        start_angle = 90 - self.angle / 2
        extent_angle = self.angle
        self.canvas.create_arc(10, 10, self.width - 10, self.height - 10,
                               start=start_angle, extent=extent_angle,
                               style='arc', outline='black', width=2)
        self.update_value(self.value)

    def update_value(self, value):
        super().check_alarm(value)
        self.value = value
        angle_rad = math.radians(90 - self.angle / 2 + (value / 100) * self.angle)
        x0 = self.width / 2
        y0 = self.height / 2
        x1 = x0 + (self.width / 2 - 10) * math.cos(angle_rad)
        y1 = y0 - (self.height / 2 - 10) * math.sin(angle_rad)
        self.canvas.delete("needle")
        self.canvas.create_line(x0, y0, x1, y1, fill='blue', width=2, tags="needle")

        # Set the color based on the value
        needle_color = "black"
        for color, limit in self.colors.items():
            if value <= limit:
                needle_color = color
                break
        self.canvas.itemconfig("needle", fill=needle_color)

    def set_colors(self, blue, green, yellow, red):
        self.colors = {
            "blue": blue,
            "green": green,
            "yellow": yellow,
            "red": red
        }


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.title("Circle Gauge Example")

    # Create a CircleGauge instance with a 180-degree view
    gauge = CircleGauge(root, angle=270, name="Speedometer")

    # Set the initial value of the gauge to 0
    gauge.update_value(0)

    # Set the gauge color thresholds
    gauge.set_colors(blue=20, green=40, yellow=60, red=80)

    # Function to update the gauge value periodically
    def update_gauge_value(value):
        if value <= 100:
            gauge.update_value(value)
            # Schedule the function to update the value again after 100ms
            root.after(100, update_gauge_value, value + 1)
        else:
            # Reset the gauge value to 0 when it exceeds 100
            update_gauge_value(0)

    # Start updating the gauge value
    update_gauge_value(0)

    # Start the Tkinter event loop
    root.mainloop()