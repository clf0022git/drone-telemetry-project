import tkinter as tk
from src.config.GaugeBase import GaugeBase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class XYPlotGauge(GaugeBase):
    def __init__(self, master, name=f'XY Plot Gauge', title='XY Plot', description='', connect_dots=False, crosshair_colormatch=False, *args, **kwargs):
        super().__init__(master, name=f'{name}-{id(self)}', title=title, description=description, *args, **kwargs)

        # Initialize the figure and axis for the plot
        self.figsize = kwargs.get('figsize', (4, 3))  # Default figure size can be overridden with kwargs
        self.figure = Figure(figsize=self.figsize, dpi=100)
        self.axis = self.figure.add_subplot(111)

        # Create the canvas and add it to the GaugeBase frame
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize lists to hold the x and y values
        self.x_values = []
        self.y_values = []
        self.colors = []

        self.current_color = None

        self.connect_dots = connect_dots
        if self.connect_dots:
            self.line, = self.axis.plot([], [], color='black')

        # Holds the matplotlib scatter plot objects
        self.current_point = None
        self.previous_point = None

        # Initialize default plot bounds
        self.x_bounds = (-15, 15)
        self.y_bounds = (-15, 15)

        # Color matching for crosshairs
        self.crosshair_colormatch = crosshair_colormatch

        # Additional text for the matplotlib figure
        self.figure_text = None

    def draw_crosshairs(self, x, y):
        """Draw crosshairs on the current dot."""
        # Clear existing crosshairs
        if hasattr(self, 'crosshair_hline') and hasattr(self, 'crosshair_vline'):
            self.crosshair_hline.remove()
            self.crosshair_vline.remove()

        # Draw horizontal and vertical lines for crosshairs
        self.crosshair_hline = self.axis.axhline(y, color=(self.current_color if self.crosshair_colormatch else 'black'), linestyle='--')
        self.crosshair_vline = self.axis.axvline(x, color=(self.current_color if self.crosshair_colormatch else 'black'), linestyle='--')
        self.canvas.draw_idle()

    def update_value(self, x, y, value):
        """Update the plot with a new data point and its value."""
        # Store the current point as the previous point
        self.previous_point = self.current_point
        # Update the current point
        self.current_point = (x, y, value)

        # Clear the plot and reset bounds
        self.axis.clear()
        self.set_bounds(x_bounds=self.x_bounds, y_bounds=self.y_bounds)

        # Redraw the previous point if it exists
        if self.previous_point:
            px, py, pvalue = self.previous_point
            pcolor = self.get_color_for_value(pvalue)
            self.axis.scatter(px, py, color=pcolor)

        # Draw the current point
        self.current_color = color = self.get_color_for_value(value)
        self.axis.scatter(x, y, color=color)

        # Add crosshairs to the current dot
        self.draw_crosshairs(x, y)

        # Redraw the plot
        self.canvas.draw_idle()

        # Check for alarm condition
        self.check_alarm(value)

    def get_color_for_value(self, value):
        """Determine the color of the bar based on the current value."""
        for color, (lower_bound, upper_bound) in self.color_ranges.items():
            if lower_bound <= value <= upper_bound:
                return color
        return 'red'  # Default to 'red' if value exceeds all defined ranges

    def set_figure_title(self, title):
        """Set the title for the matplotlib plot. This is different from the GaugeBase title."""
        self.axis.set_title(title)
        self.canvas.draw_idle()

    def set_figure_text(self, text):
        """Set additional text on the matplotlib figure."""
        if self.figure_text is not None:
            self.figure_text.remove()
        # Position the text at the top center of the figure
        self.figure_text = self.axis.text(0.5, 0.9, text, ha='center', va='center', transform=self.axis.transAxes)
        self.canvas.draw_idle()

    def set_figure_size(self, width, height):
        """Set the figure size."""
        self.figsize = (width, height)
        self.figure.set_size_inches(self.figsize, forward=True)
        self.figure.canvas.draw_idle()

    def set_bounds(self, x_bounds=None, y_bounds=None):
        """Set the x/y bounds of the plot."""
        if x_bounds:
            self.x_bounds = x_bounds
        if y_bounds:
            self.y_bounds = y_bounds
        self.axis.set_xlim(self.x_bounds)
        self.axis.set_ylim(self.y_bounds)
        self.canvas.draw_idle()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("XY Plot Gauge Example")

    xy_plot_gauge = XYPlotGauge(root, title='Drone Position', description='Drone X-Y Plot', crosshair_colormatch=False)
    xy_plot_gauge.pack(fill=tk.BOTH, expand=True)

    # xy_plot_gauge.set_bounds(x_bounds=(-10, 10), y_bounds=(-10, 10))  # Uncomment to set custom bounds

    xy_plot_gauge.set_figure_title("Drone Position")

    # Function to simulate data points being added to the plot over time
    def simulate_data():
        # Here you would retrieve or generate actual x, y, and value data
        # For simulation, we're using random data
        import random
        new_x, new_y = random.uniform(-10, 10), random.uniform(-10, 10)
        new_value = random.uniform(0, 100)  # Value used to determine the color
        xy_plot_gauge.update_value(new_x, new_y, new_value)
        xy_plot_gauge.set_figure_text(f"Color Value: {new_value}\nX: {new_x}\nY: {new_y}")

        # Schedule the next data point update in 1 second (1000 ms)
        root.after(1000, simulate_data)


    simulate_data()
    root.mainloop()
