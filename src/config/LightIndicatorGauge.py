import tkinter as tk
from src.config.GaugeBase import GaugeBase


class LightIndicatorGauge(GaugeBase):
    def __init__(self, master, name='Light Indicator', title='Light', description='', *args, **kwargs):
        super().__init__(master, name=f'{name}-{id(self)}', title=title, description=description, *args, **kwargs)

        # Canvas for the light indicator
        self.light_canvas = tk.Canvas(self, width=60, height=60, bg='white')
        self.light_canvas.pack()

        # Draw the initial light indicator (off)
        self.light = self.light_canvas.create_oval(10, 10, 50, 50, fill='grey')
        self.is_on = False

    def update_value(self, value):
        """Toggle the light on or off based on the value."""
        self.is_on = value
        self.light_canvas.itemconfig(self.light, fill='green' if self.is_on else 'grey')

    def toggle_light(self):
        """Toggle the light state."""
        self.update_value(not self.is_on)

    def resize(self, width, height):
        """Resize the gauge frame and adjust the canvas and oval size."""
        # Resize the frame
        self.config(width=width, height=height)

        # Adjust the canvas size to fit the new frame size
        new_canvas_width = width - 20
        new_canvas_height = height - 20
        self.light_canvas.config(width=new_canvas_width, height=new_canvas_height)

        # Calculate new oval size and position
        oval_size = min(new_canvas_width, new_canvas_height) * 0.4  # 40% of the smallest dimension
        oval_padding_x = (new_canvas_width - oval_size) / 2
        oval_padding_y = (new_canvas_height - oval_size) / 2
        new_oval_coords = (
            oval_padding_x, oval_padding_y,
            oval_padding_x + oval_size, oval_padding_y + oval_size
        )

        # Update the oval's coordinates to scale it
        self.light_canvas.coords(self.light, new_oval_coords)

        # Ensure the layout updates
        self.light_canvas.pack()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Light Indicator Example")

    light_gauge = LightIndicatorGauge(root, title='Power Status', description='System Power')
    light_gauge.pack(padx=10, pady=10)

    # Button to toggle the light on/off
    toggle_button = tk.Button(root, text="Toggle Light", command=light_gauge.toggle_light)
    toggle_button.pack(pady=5)

    #light_gauge.resize(500, 500)

    root.mainloop()
