import tkinter as tk
from src.config.GaugeBase import GaugeBase
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class XYPlotGauge(GaugeBase):
    def __init__(self, master, name=f'XY Plot Gauge', title='XY Plot', description='', connect_dots=False, *args, **kwargs):
        super().__init__(master, name=f'{name}-{id(self)}', title=title, description=description, *args, **kwargs)

        # Initialize the figure and axis for the plot
        self.figsize = kwargs.get('figsize', (5, 4))  # Default figure size can be overridden with kwargs
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

        self.connect_dots = connect_dots
        if self.connect_dots:
            self.line, = self.axis.plot([], [], color='black')

        # Additional text for the matplotlib figure
        self.figure_text = None

    def update_value(self, x, y, value):
        """Update the plot with a new data point and its value."""
        # Add the new data point and its color based on the value
        self.x_values.append(x)
        self.y_values.append(y)
        color = self.get_color_for_value(value)
        self.colors.append(color)

        # Plot the new data point
        self.axis.scatter(x, y, color=color)
        self.canvas.draw_idle()

        # If connect_dots is True, update the line with the new data point
        if self.connect_dots:
            self.line.set_data(self.x_values, self.y_values)
            self.canvas.draw_idle()

        # Check for alarm condition
        self.check_alarm(value)

    def get_color_for_value(self, value):
        """Determine the color of the data point based on the value."""
        for color, limit in self.color_ranges.items():
            if value <= limit:
                return color
        return 'red'

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
            self.axis.set_xlim(x_bounds)
        if y_bounds:
            self.axis.set_ylim(y_bounds)
        self.canvas.draw_idle()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("XY Plot Gauge Example")

    xy_plot_gauge = XYPlotGauge(root, title='Drone Position', description='Drone X-Y Plot', connect_dots=True)
    xy_plot_gauge.pack(fill=tk.BOTH, expand=True)

    xy_plot_gauge.set_bounds(x_bounds=(-10, 10), y_bounds=(-10, 10))

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
