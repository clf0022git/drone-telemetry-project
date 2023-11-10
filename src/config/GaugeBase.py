import tkinter as tk
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


# class GaugeBase:
#     def __init__(self, master, name='Default'):
#         self.master = master
#         self.name = name
#         self.canvas = tk.Canvas(master, width=300, height=300)
#         self.canvas.pack()
#         self.red_limit = 80  # Example limit for the red range
#
#     def update_value(self, value):
#         raise NotImplementedError("This method should be implemented by subclasses.")
#
#     def check_alarm(self, value):
#         if value > self.red_limit:
#             # This is where you'd trigger the audible alarm
#             print("Alarm! Value exceeded red limit.")
#             self.master.bell()


class GaugeBase:
    def __init__(self, master, name='Default'):
        self.master = master
        self.name = name
        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.pack()
        self.color_ranges = {
            'blue': (None, 25),
            'green': (25, 50),
            'yellow': (50, 75),
            'red': (75, None)
        }
        self.red_limit = 80  # Default red limit

    def update_value(self, value):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def check_alarm(self, value):
        if value > self.red_limit:
            # Trigger the audible alarm
            print("Alarm! Value exceeded red limit.")
            self.master.bell()

    def set_color_ranges(self, blue=None, green=None, yellow=None, red=None):
        if blue is not None:
            self.color_ranges['blue'] = (None, blue)
        if green is not None:
            self.color_ranges['green'] = (blue, green)
        if yellow is not None:
            self.color_ranges['yellow'] = (green, yellow)
        self.red_limit = red if red is not None else self.red_limit
        if red is not None:
            self.color_ranges['red'] = (yellow, None)


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


# class BarGauge(GaugeBase):
#     def __init__(self, master, name='Default', max_value=100, **kwargs):
#         super().__init__(master, name)
#         self.max_value = max_value
#         self.bar = None
#         self.create_bar()
#
#     def create_bar(self):
#         self.canvas.create_rectangle(10, 135, 290, 165, outline='black', fill='white')
#         self.bar = self.canvas.create_rectangle(10, 135, 10, 165, outline='', fill='green')
#
#     def update_value(self, value):
#         self.check_alarm(value)
#         # Calculate the width of the bar based on the value
#         bar_width = (value / self.max_value) * (280 - 10)
#         # Update the bar's width
#         self.canvas.coords(self.bar, 10, 135, 10 + bar_width, 165)
#         # Change the bar color based on the value
#         if value > self.red_limit:
#             self.canvas.itemconfig(self.bar, fill='red')
#         elif value > self.colors['yellow']:
#             self.canvas.itemconfig(self.bar, fill='yellow')
#         elif value > self.colors['green']:
#             self.canvas.itemconfig(self.bar, fill='green')
#         else:
#             self.canvas.itemconfig(self.bar, fill='blue')
#
#     def set_colors(self, blue, green, yellow, red):
#         self.colors = {
#             "blue": blue,
#             "green": green,
#             "yellow": yellow,
#             "red": red
#         }
#         self.update_value(self.max_value)  # Update the bar to reflect the new color settings

class BarGauge(GaugeBase):
    def __init__(self, master, name='Default', max_value=100, **kwargs):
        super().__init__(master, name, **kwargs)
        self.max_value = max_value
        self.bar_length = 280  # Length of the bar in pixels
        self.bar_height = 30   # Height of the bar in pixels
        self.bar = self.canvas.create_rectangle(10, 150 - self.bar_height / 2,
                                                10, 150 + self.bar_height / 2,
                                                outline='black', fill='green')

    def update_value(self, value):
        # Check if the value exceeds the red limit
        self.check_alarm(value)
        # Calculate the new width of the bar based on the value
        fill_width = (value / self.max_value) * self.bar_length
        # Update the bar
        self.canvas.coords(self.bar, 10, 150 - self.bar_height / 2,
                           10 + fill_width, 150 + self.bar_height / 2)
        # Set the color based on the value
        if value > self.red_limit:
            self.canvas.itemconfig(self.bar, fill='red')
        elif value >= 60:  # Assuming yellow limit is at 60% of red_limit
            self.canvas.itemconfig(self.bar, fill='yellow')
        elif value >= 40:  # Assuming green limit is at 40% of red_limit
            self.canvas.itemconfig(self.bar, fill='green')
        else:
            self.canvas.itemconfig(self.bar, fill='blue')


# class XYPlotGauge(GaugeBase):
#     def __init__(self, master, name='Default', x_range=(0, 100), y_range=(0, 100), **kwargs):
#         super().__init__(master, name, **kwargs)
#         self.x_range = x_range
#         self.y_range = y_range
#         self.point = None
#         self.create_plot()
#
#     def create_plot(self):
#         # Clear any existing drawings
#         self.canvas.delete("all")
#         # Draw the plot area
#         self.canvas.create_rectangle(10, 10, 290, 290, outline='black')
#         # Draw a point in the center to start with
#         self.update_value((self.x_range[1] / 2, self.y_range[1] / 2))
#
#     def update_value(self, xy_values):
#         # Calculate canvas coordinates
#         x, y = xy_values
#         x_canvas = 10 + (x - self.x_range[0]) / (self.x_range[1] - self.x_range[0]) * 280
#         y_canvas = 290 - (y - self.y_range[0]) / (self.y_range[1] - self.y_range[0]) * 280
#
#         # Check if the point is beyond the red limit
#         if x > self.red_limit or y > self.red_limit:
#             self.check_alarm(max(x, y))
#
#         # Create or move the point
#         if self.point is None:
#             self.point = self.canvas.create_oval(x_canvas - 5, y_canvas - 5,
#                                                  x_canvas + 5, y_canvas + 5,
#                                                  fill='blue', outline='blue')
#         else:
#             self.canvas.coords(self.point, x_canvas - 5, y_canvas - 5,
#                                x_canvas + 5, y_canvas + 5)


class XYPlotGauge(GaugeBase):
    def __init__(self, master, name='Default', x_range=(0, 100), y_range=(0, 100), **kwargs):
        super().__init__(master, name, **kwargs)
        self.x_range = x_range
        self.y_range = y_range
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.plot.set_xlim(self.x_range)
        self.plot.set_ylim(self.y_range)

        # Embed the matplotlib figure in the tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        self.points, = self.plot.plot([], [], 'o')

    def update_value(self, xy_values):
        x, y = xy_values
        self.points.set_data(x, y)
        self.check_alarm(max(x, y))  # Check for alarm conditions

        # Update the plot with the new point
        self.canvas.draw()

    def check_alarm(self, value):
        super().check_alarm(value)
        color = 'red' if value > self.red_limit else 'blue'
        self.points.set_color(color)



# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Circle Gauge Example")
#
#     # Create a CircleGauge instance with a 180-degree view
#     gauge = CircleGauge(root, angle=270, name="Speedometer")
#
#     # Set the initial value of the gauge to 0
#     gauge.update_value(0)
#
#     # Set the gauge color thresholds
#     gauge.set_colors(blue=20, green=40, yellow=60, red=80)
#
#     # Function to update the gauge value periodically
#     def update_gauge_value(value):
#         if value <= 100:
#             gauge.update_value(value)
#             # Schedule the function to update the value again after 100ms
#             root.after(100, update_gauge_value, value + 1)
#         else:
#             # Reset the gauge value to 0 when it exceeds 100
#             update_gauge_value(0)
#
#     # Start updating the gauge value
#     update_gauge_value(0)
#
#     # Start the Tkinter event loop
#     root.mainloop()


# if __name__ == "__main__":
#     root = tk.Tk()
#     bar_gauge = BarGauge(root, name="Volume")
#     bar_gauge.set_colors(blue=20, green=50, yellow=75, red=90)
#
#     # Function to update the gauge value periodically
#     def update_gauge_value(value):
#         if value <= bar_gauge.max_value:
#             bar_gauge.update_value(value)
#             # Schedule the function to update the value again after 100ms
#             root.after(100, update_gauge_value, value + 1)
#         else:
#             # Reset the gauge value to 0 when it exceeds the max_value
#             update_gauge_value(0)
#
#     # Start updating the gauge value
#     update_gauge_value(0)
#
#     root.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     bar_gauge = BarGauge(root, name="Volume", max_value=100)
#
#     def increment_value(gauge, value):
#         if value <= gauge.max_value:
#             gauge.update_value(value)
#             root.after(100, increment_value, gauge, value + 1)
#         else:
#             # Resetting the gauge for demonstration purposes
#             root.after(100, increment_value, gauge, 0)
#
#     # Start the demo
#     increment_value(bar_gauge, 0)
#
#     root.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("XY Plot Gauge Example")
#
#     # Create an XYPlotGauge instance with specific x and y ranges
#     xy_plot_gauge = XYPlotGauge(root, name="Temperature-Humidity Plot", x_range=(0, 100), y_range=(0, 100))
#
#     # Initialize time for the animation
#     start_time = time.time()
#
#
#     # Function to update the gauge value periodically
#     def update_gauge():
#         # Use sine and cosine functions to create circular motion for the example
#         t = time.time() - start_time
#         x_value = 50 + 30 * math.sin(math.radians(t * 60))
#         y_value = 50 + 30 * math.cos(math.radians(t * 60))
#
#         # Update the XYPlotGauge with the new values
#         xy_plot_gauge.update_value((x_value, y_value))
#
#         # Schedule the function to update the gauge again after 50ms
#         root.after(50, update_gauge)
#
#
#     # Start the animation
#     update_gauge()
#
#     # Start the Tkinter event loop
#     root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    xy_plot_gauge = XYPlotGauge(root, name="XY Plot Gauge", x_range=(0, 100), y_range=(0, 100))

    # Function to update the plot over time
    def update_plot():
        # Generate some random x, y values for demonstration
        x, y = np.random.rand(2) * 100
        xy_plot_gauge.update_value((x, y))
        root.after(1000, update_plot)

    # Start updating the plot
    update_plot()

    root.mainloop()
