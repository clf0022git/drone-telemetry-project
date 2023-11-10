from src.config.GaugeBase import GaugeBase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import numpy as np


# class XYPlotGauge(GaugeBase):
#     def __init__(self, master, name='Default', x_range=(0, 100), y_range=(0, 100), **kwargs):
#         super().__init__(master, name, **kwargs)
#         self.x_range = x_range
#         self.y_range = y_range
#         self.figure = Figure(figsize=(5, 5), dpi=100)
#         self.plot = self.figure.add_subplot(111)
#         self.plot.set_xlim(self.x_range)
#         self.plot.set_ylim(self.y_range)
#
#         # Embed the matplotlib figure in the tkinter canvas
#         self.canvas = FigureCanvasTkAgg(self.figure, master)
#         self.canvas_widget = self.canvas.get_tk_widget()
#         self.canvas_widget.pack()
#
#         self.points, = self.plot.plot([], [], 'o')
#
#     def update_value(self, xy_values):
#         x, y = xy_values
#         self.points.set_data(x, y)
#         self.check_alarm(max(x, y))  # Check for alarm conditions
#
#         # Update the plot with the new point
#         self.canvas.draw()
#
#     def check_alarm(self, value):
#         super().check_alarm(value)
#         color = 'red' if value > self.red_limit else 'blue'
#         self.points.set_color(color)

# class XYPlotGauge(GaugeBase):
#     def __init__(self, master, name='Default', x_range=(0, 100), y_range=(0, 100), **kwargs):
#         super().__init__(master, name, **kwargs)
#         self.x_range = x_range
#         self.y_range = y_range
#         self.figure = Figure(figsize=(5, 5), dpi=100)
#         self.plot = self.figure.add_subplot(111)
#         self.plot.set_xlim(self.x_range)
#         self.plot.set_ylim(self.y_range)
#
#         # Embed the matplotlib figure in the tkinter canvas
#         self.canvas = FigureCanvasTkAgg(self.figure, master)
#         self.canvas_widget = self.canvas.get_tk_widget()
#         self.canvas_widget.pack()
#
#         # Initialize empty lists to store the x and y values
#         self.x_values = []
#         self.y_values = []
#
#         # Plot an empty line, we will add points to this line in the update_value method
#         self.points, = self.plot.plot([], [], 'o')
#
#     def update_value(self, xy_values):
#         x, y = xy_values
#         # Append the new x and y values to the lists
#         self.x_values.append(x)
#         self.y_values.append(y)
#
#         # Set the new data for the points
#         self.points.set_data(self.x_values, self.y_values)
#
#         # Check for alarm conditions
#         if max(x, y) > self.red_limit:
#             self.check_alarm(max(x, y))
#             self.points.set_color('red')  # Set the point's color to red if the alarm condition is met
#         else:
#             self.points.set_color('blue')  # Set the point's color to blue otherwise
#
#         # Re-draw the canvas to show the updated plot
#         self.canvas.draw()


# if __name__ == "__main__":
#     import tkinter as tk
#     import numpy as np
#     root = tk.Tk()
#     xy_plot_gauge = XYPlotGauge(root, name="XY Plot Gauge", x_range=(0, 100), y_range=(0, 100))
#
#
#     # Function to update the plot over time
#     def update_plot():
#         # Generate some random x, y values for demonstration
#         x, y = np.random.rand(2) * 100
#         xy_plot_gauge.update_value((x, y))
#         root.after(1000, update_plot)
#
#
#     # Start updating the plot
#     update_plot()
#
#     root.mainloop()

import matplotlib.pyplot as plt


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

        self.x_values = []
        self.y_values = []
        self.colors = []

    def update_value(self, xy_values):
        x, y = xy_values
        self.x_values.append(x)
        self.y_values.append(y)

        # Determine color based on the threshold
        color = 'red' if max(x, y) > self.red_limit else 'blue'
        self.colors.append(color)

        # Check for alarm conditions
        if max(x, y) > self.red_limit:
            self.check_alarm(max(x, y))

        # Clear the plot to draw new points and lines
        self.plot.clear()
        self.plot.set_xlim(self.x_range)
        self.plot.set_ylim(self.y_range)

        # Plot the line connecting all points
        self.plot.plot(self.x_values, self.y_values, marker='', linestyle='-', color='gray')

        # Plot points with their respective colors
        for i in range(len(self.x_values)):
            self.plot.scatter(self.x_values[i], self.y_values[i], color=self.colors[i])

        # Re-draw the canvas to show the updated plot
        self.canvas.draw()


# Example usage
if __name__ == "__main__":
    import tkinter as tk
    import numpy as np
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
