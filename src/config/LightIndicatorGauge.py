import tkinter as tk
from src.config.GaugeBase import GaugeBase


class LightIndicatorGauge(GaugeBase):
    def __init__(self, master,  name='Light Indicator', title='Light', description='', *args, **kwargs):
        super().__init__(master, name=f'{name}-{id(self)}', title=title, description=description, *args, **kwargs)

        # Canvas for the light indicator
        self.light_canvas = tk.Canvas(self, width=60, height=60, bg='white')
        self.light_canvas.pack()

        # Draw the initial light indicator (off)
        self.light = self.light_canvas.create_oval(10, 10, 50, 50, fill='grey')
        self.is_on = False

        #self.data_set1 = data_set.copy()
        self.increment = 0

    def update_value(self, value):
        """Toggle the light on or off based on the value."""
        self.is_on = value
        self.light_canvas.itemconfig(self.light, fill='green' if self.is_on else 'grey')

    '''def update_value2(self):
        self.is_on = self.data_set1[self.increment]
        if (self.data_set1[self.increment] != self.data_set1[++self.increment]):
            self.light_canvas.itemconfig(self.light, fill='grey')
        else:
            self.light_canvas.itemconfig(self.light, fill='green')
        self.increment += 1'''

    def toggle_light(self):
        """Toggle the light state."""
        self.update_value(not self.is_on)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Light Indicator Example")

    example_data = [0]

    light_gauge = LightIndicatorGauge(example_data, root, title='Power Status', description='System Power')
    light_gauge.pack(padx=10, pady=10)

    # Button to toggle the light on/off
    toggle_button = tk.Button(root, text="Toggle Light", command=light_gauge.toggle_light)
    toggle_button.pack(pady=5)

    root.mainloop()
