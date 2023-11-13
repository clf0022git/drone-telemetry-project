import tkinter as tk
from math import pi, cos, sin
from src.config.GaugeBase import GaugeBase


class CircleGauge(GaugeBase):
    def __init__(self, master, name='Circle Gauge', max_degree=360, show_numbers=False, *args, **kwargs):
        super().__init__(master, name, *args, **kwargs)
        self.max_degree = max_degree
        self.show_numbers = show_numbers
        self.current_value = 0

        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.pack()
        self.draw_gauge()

    def draw_gauge(self):
        """Draw the circle gauge with specific degree options."""
        self.canvas.delete("all")  # Clear the canvas before drawing

        radius = 80
        center_x, center_y = 100, 100
        number_radius = radius * 0.85  # Slightly smaller radius for numbers

        # Draw based on specific degree cases
        if self.max_degree == 90:
            start_angle = 90
            extent_angle = 90
        elif self.max_degree == 180:
            start_angle = 90
            extent_angle = 180
        elif self.max_degree == 270:
            start_angle = 180
            extent_angle = 270
        elif self.max_degree == 360:
            self.canvas.create_oval(center_x-radius, center_y-radius, center_x+radius, center_y+radius, outline="black", width=2)
            self.draw_numbers(center_x, center_y, number_radius, 360)
            return  # No need to draw arc for full circle

        # Draw the arc for 90, 180, 270 degrees
        self.canvas.create_arc(center_x-radius, center_y-radius, center_x+radius, center_y+radius,
                               start=start_angle, extent=extent_angle, style=tk.ARC, outline="black", width=2)

        # Draw numbers for 90, 180, 270 degrees
        self.draw_numbers(center_x, center_y, number_radius, self.max_degree)

    def draw_numbers(self, center_x, center_y, number_radius, max_degree):
        """Draw the numbers for the gauge."""
        if self.show_numbers:
            for num in range(0, max_degree + 1, 30):  # Place numbers every 30 degrees
                # Adjust the angle for the number placement
                angle_rad = pi * (1.5 - 2 * num / 360)
                x = center_x + number_radius * cos(angle_rad)
                y = center_y - number_radius * sin(angle_rad)

                # Draw the number
                if num != max_degree:
                    self.canvas.create_text(x, y, text=str(num), font=('Arial', 8))

    def update_value(self, value):
        """Update the gauge's value."""
        self.current_value = value
        self.draw_needle()
        self.check_alarm(value)

    def draw_needle(self):
        """Draw the arrow on the gauge."""
        self.canvas.delete("needle")  # Remove the old needle

        radius = 80
        center_x, center_y = 100, 100
        needle_length = radius * 0.8  # Length of the needle from the center of the gauge

        # Calculate the angle for the needle
        angle_deg = (self.current_value / self.max_degree) * 360
        angle_rad = pi * (1.5 - angle_deg / 180)  # Convert to radians, adjusting for the canvas coordinates

        # Calculate the end point of the arrow
        end_x = center_x + needle_length * cos(angle_rad)
        end_y = center_y - needle_length * sin(angle_rad)

        # Draw the arrow
        self.canvas.create_line(center_x, center_y, end_x, end_y, arrow=tk.LAST, fill="red", width=2, tags="needle")

    def toggle_numbers(self):
        """Toggle the display of numbers on the gauge."""
        self.show_numbers = not self.show_numbers
        self.draw_gauge()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circle Gauge Example")

    # Create an instance of CircleGauge
    circle_gauge = CircleGauge(root, name='Speedometer', title='Speedometer', max_degree=360, show_numbers=True)
    circle_gauge.pack(padx=20, pady=20)

    circle_gauge.update_colors(red_limit=300)

    # Function to update gauge value for demonstration
    def update_gauge():
        import random
        new_value = random.randint(0, 360)
        circle_gauge.update_value(new_value)
        circle_gauge.set_description(f'Current value: {new_value}')
        circle_gauge.after(1000, update_gauge)  # Update the gauge value every 1 second

    # Start the gauge value update
    update_gauge()

    root.mainloop()
