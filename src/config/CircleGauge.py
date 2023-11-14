import tkinter as tk
from math import pi, cos, sin
from src.config.GaugeBase import GaugeBase


class CircleGauge(GaugeBase):
    def __init__(self, master, name='Circle Gauge', max_degree=360, show_numbers=True, number_range=(0, 100), number_step=10, *args, **kwargs):
        super().__init__(master, name=f'{name}-{id(self)}', *args, **kwargs)
        self.max_degree = max_degree
        self.show_numbers = show_numbers
        self.number_range = number_range
        self.number_step = number_step
        self.current_value = 0
        self.gauge_shape = None

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
            start_angle = 0
            extent_angle = 90
        elif self.max_degree == 180:
            start_angle = 0
            extent_angle = 180
        elif self.max_degree == 270:
            start_angle = 0
            extent_angle = 270
        elif self.max_degree == 360:
            self.gauge_shape = self.canvas.create_oval(center_x-radius, center_y-radius, center_x+radius, center_y+radius, outline="black", width=2)
            self.draw_numbers(center_x, center_y, number_radius, 360)
            return  # No need to draw arc for full circle

        # Draw the arc for 90, 180, 270 degrees
        self.gauge_shape = self.canvas.create_arc(center_x-radius, center_y-radius, center_x+radius, center_y+radius,
                               start=start_angle, extent=extent_angle, style=tk.ARC, outline="black", width=2)

        # Draw numbers for 90, 180, 270 degrees
        self.draw_numbers(center_x, center_y, number_radius, self.max_degree)

    def draw_numbers(self, center_x, center_y, number_radius, max_degree):
        """Draw the numbers for the gauge."""
        if self.show_numbers:
            start, end = self.number_range
            step = self.number_step
            num = start
            while num <= end:
                # Calculate the angle for each number
                angle_deg = (num - start) / (end - start) * max_degree
                if max_degree == 90:
                    angle_rad = pi * (0.5 - angle_deg / 180)
                elif max_degree == 180:
                    angle_rad = pi * (1 - angle_deg / 180)
                else:
                    angle_rad = pi * (1.5 - 2 * angle_deg / 360)
                x = center_x + number_radius * cos(angle_rad)
                y = center_y - number_radius * sin(angle_rad)

                # Draw the number
                if num != end:
                    self.canvas.create_text(x, y, text=str(num), font=('Arial', 8))
                else:
                    if max_degree == 360:
                        self.canvas.create_text(x, y + 20, text=str(num), font=('Arial', 8))
                    else:
                        self.canvas.create_text(x, y, text=str(num), font=('Arial', 8))

                # Increment the number by the step
                num += step
                num = round(num, 10)  # To avoid floating point arithmetic issues

    def update_value(self, value):
        """Update the gauge's value."""
        self.current_value = value
        self.draw_needle()
        self.update_gauge_color(value)
        self.check_alarm(value)

    def update_gauge_color(self, value):
        """Change the gauge color based on the value."""
        color = 'blue'  # Default color

        # Check against each color range
        for color_key, (lower_bound, upper_bound) in self.color_ranges.items():
            if lower_bound <= value <= upper_bound:
                color = color_key
                break

        # Update the color of the needle
        # self.canvas.itemconfig(self.gauge_shape, outline=color)  # Uncomment this if you want to change the outline color
        self.canvas.itemconfig("needle", fill=color)

    def draw_needle(self):
        """Draw the arrow on the gauge."""
        self.canvas.delete("needle")  # Remove the old needle

        radius = 80
        center_x, center_y = 100, 100
        needle_length = radius * 0.8  # Length of the needle from the center of the gauge

        # Adjust the needle to point based on the value and number range
        start, end = self.number_range
        if start <= self.current_value <= end:
            # Normalize the value within the range
            normalized_value = (self.current_value - start) / (end - start)

            # Adjust angle calculation for different gauge types
            if self.max_degree == 90:
                angle_deg = normalized_value * 90  # Only for 90-degree gauge
                angle_rad = pi * (0.5 - angle_deg / 180)  # Adjust for 90-degree gauge
            elif self.max_degree == 180:
                angle_deg = normalized_value * 180
                angle_rad = pi * (1 - angle_deg / 180)  # Adjust for 180-degree gauge
            else:
                angle_deg = normalized_value * self.max_degree
                angle_rad = pi * (1.5 - 2 * angle_deg / 360)
        else:
            # If the value is outside the range, keep the needle at the start or end
            angle_rad = 0 if self.current_value < start else pi * 0.5 if self.max_degree == 90 else pi * 1.5

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
    root.title("Circle Gauge Examples with Floats")

    # Configuration for each gauge with floating-point number ranges
    gauge_configs = [
        {'max_degree': 90, 'number_range': (0.0, 45.0), 'number_step': 5.0},
        {'max_degree': 180, 'number_range': (0.0, 90.0), 'number_step': 10.0},
        {'max_degree': 270, 'number_range': (0.0, 135.0), 'number_step': 15.0},
        {'max_degree': 360, 'number_range': (0.0, 180.0), 'number_step': 20.0}
    ]

    gauge_alarms = [35.0, 70.0, 105.0, 150.0]

    gauges = []
    for i, config in enumerate(gauge_configs):
        gauge = CircleGauge(root, name=f'Circle-{config["max_degree"]}', title=f'Circle {config["max_degree"]}°',
                            show_numbers=True, **config)
        gauge.grid(row=i//2, column=i%2, padx=20, pady=20)
        gauges.append(gauge)

    for i, alarm in enumerate(gauge_alarms):
        gauges[i].update_colors(red_limit=alarm)

    # Function to update gauge values for demonstration with floating-point values
    def update_gauges():
        import random
        for gauge in root.winfo_children():
            if isinstance(gauge, CircleGauge):
                new_value = round(random.uniform(0, gauge.number_range[1]), 1)
                gauge.update_value(new_value)
                gauge.set_description(f'Current value: {new_value}')
        root.after(1000, update_gauges)  # Update the gauge values every 1 second

    # Start the gauge value updates
    update_gauges()

    root.mainloop()
