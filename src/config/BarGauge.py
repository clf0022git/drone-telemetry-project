import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.config.GaugeBase import GaugeBase


class BarGauge(GaugeBase):
    def __init__(self, master, name='Bar Gauge', title='Bar Gauge', description='', orientation='vertical', *args, **kwargs):
        super().__init__(master, name=name, title=title, description=description, *args, **kwargs)
        self.orientation = orientation
        self.figsize = kwargs.get('figsize', (4, 2))  # Default figure size can be overridden with kwargs

        self.figure = Figure(figsize=self.figsize, dpi=100)
        self.plot = self.figure.add_subplot(111)

        # Initialize the bar with 0 height/width
        if self.orientation == 'vertical':
            self.bar_container = self.plot.bar([0], [0], color='blue')
        elif self.orientation == 'horizontal':
            self.bar_container = self.plot.barh([0], [0], color='blue')  # Use barh for horizontal bars
        else:
            raise ValueError("Invalid orientation: choose 'vertical' or 'horizontal'")

        self.bar = self.bar_container[0]

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Additional text for the matplotlib figure
        self.figure_text = None

    def update_value(self, value):
        """Update the bar graph's value and color based on the value."""
        if self.orientation == 'vertical':
            self.bar.set_height(value)
        else:  # 'horizontal'
            self.bar.set_width(value)

        color = self.get_color_for_value(value)
        self.bar.set_color(color)
        self.figure.canvas.draw_idle()
        self.check_alarm(value)

    def get_color_for_value(self, value):
        """Determine the color of the bar based on the current value."""
        for color, limit in self.color_ranges.items():
            if value <= limit:
                return color
        return 'red'

    def set_figure_text(self, text):
        """Set additional text on the matplotlib figure."""
        if self.figure_text is not None:
            self.figure_text.remove()
        # Position the text above the bar (e.g., at the top center of the figure)
        self.figure_text = self.plot.text(0.5, 0.9, text, ha='center', va='center', transform=self.plot.transAxes)
        self.figure.canvas.draw_idle()

    def set_figure_size(self, width, height):
        """Set the figure size."""
        self.figsize = (width, height)
        self.figure.set_size_inches(self.figsize, forward=True)
        self.figure.canvas.draw_idle()

    def set_bounds(self, x_bounds=None, y_bounds=None):
        """Set the x/y bounds of the graph."""
        if x_bounds:
            self.plot.set_xlim(x_bounds)
        if y_bounds:
            self.plot.set_ylim(y_bounds)
        self.figure.canvas.draw_idle()


# Example usage
if __name__ == "__main__":
    import random
    root = tk.Tk()
    root.title("Bar Gauge Example")

    # Initialize vertical bar gauge
    v_bar_gauge = BarGauge(root, title='Vertical Bar', description='Vertical bar description', orientation='vertical')
    v_bar_gauge.pack(padx=10, pady=10)

    # Initialize horizontal bar gauge
    h_bar_gauge = BarGauge(root, title='Horizontal Bar', description='Horizontal bar description', orientation='horizontal')
    h_bar_gauge.pack(padx=10, pady=10)

    # Change figure size as needed
    v_bar_gauge.set_figure_size(4, 3)
    h_bar_gauge.set_figure_size(4, 1)

    # Set the bounds for the bar gauges
    v_bar_gauge.set_bounds(y_bounds=(0, 100))
    h_bar_gauge.set_bounds(x_bounds=(0, 100))

    # Function to simulate the bar graph value changing over time
    def simulate_data_point():
        new_value = random.randint(0, 100)
        v_bar_gauge.update_value(new_value)
        v_bar_gauge.set_figure_text(f"Value: {new_value}")
        h_bar_gauge.update_value(new_value)
        h_bar_gauge.set_figure_text(f"Value: {new_value}")
        root.after(1000, simulate_data_point)


    simulate_data_point()
    root.mainloop()
