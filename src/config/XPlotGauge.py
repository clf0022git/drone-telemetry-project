import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.config.GaugeBase import GaugeBase


class XPlotGauge(GaugeBase):
    def __init__(self, master, name='X Plot Gauge', title='X Plot', description='', *args, **kwargs):
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
        self.time_values = []  # Represents each data point's occurrence over time
        self.lines, = self.axis.plot([], [], color='blue')  # Initialize a Line2D object for the plot

        # Additional text for the matplotlib figure
        self.figure_text = None

    def update_value(self, value):
        """Update the plot with a new data point."""
        # Append the new data value and its corresponding time value
        self.x_values.append(value)
        self.time_values.append(len(self.time_values))  # Assuming uniform time intervals

        # Update the plot line with the new data
        self.lines.set_data(self.x_values, self.time_values)

        # Adjust the plot limits
        self.axis.relim()
        self.axis.autoscale_view()

        # Update the line color based on the value
        color = self.get_color_for_value(value)
        self.lines.set_color(color)

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
    CASE = 1  # Change this to 0 or 1 to run the corresponding example below
    if CASE == 0:  # Simulate (random) data points being added to the plot over time
        root = tk.Tk()
        root.title("X Plot Gauge Example")

        x_plot_gauge = XPlotGauge(root, title='Data over Time', description='X values plotted over time')
        x_plot_gauge.pack(fill=tk.BOTH, expand=True)
        # Function to simulate data points being added to the plot over time
        def simulate_data():
            import random
            # Here you would retrieve or generate actual data
            # For simulation, we're using random data
            new_value = random.uniform(0, 100)
            x_plot_gauge.update_value(new_value)

            # Update the figure text with the new value
            x_plot_gauge.set_figure_text(f"Value: {new_value:.2f}")

            # Schedule the next data point update in 1 second (1000 ms)
            root.after(1000, simulate_data)


        simulate_data()
        root.mainloop()
    elif CASE == 1:  # Update the plot with the next data point from a sample list
        root = tk.Tk()
        root.title("X Plot Gauge Example")

        x_plot_gauge = XPlotGauge(root, title='Data over Time', description='X values plotted over time')
        x_plot_gauge.pack(fill=tk.BOTH, expand=True)

        # Sample x-values (could represent anything, such as temperature readings)
        sample_x_values = [23, 25, 22, 26, 24, 28, 27, 29, 30, 25, 81, 24, 23, 22]
        # Function to update the plot with the next data point from the sample list
        def update_plot(index=0):
            x_line = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
            if index < len(x_line):
                x_plot_gauge.update_value(x_line[index])
                x_plot_gauge.set_figure_text(f"Value: {x_line[index]}")
                root.after(1000, update_plot, index + 1)


        update_plot()  # Start updating the plot with sample data points

        root.mainloop()
