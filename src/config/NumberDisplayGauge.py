import tkinter as tk
from src.config.GaugeBase import GaugeBase


class NumberDisplayGauge(GaugeBase):
    def __init__(self, master, name='Number Display', *args, **kwargs):
        super().__init__(master, name=f'{name}-{id(self)}', *args, **kwargs)
        self.display_var = tk.StringVar()
        self.display_label = tk.Label(self, textvariable=self.display_var, font=('Arial', 24))
        self.display_label.pack(expand=True)

    def update_value(self, value):
        """Update the displayed number."""
        self.display_var.set(value)
        self.check_alarm(value)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gauge Example")

    number_gauge = NumberDisplayGauge(root, title='Speed', description='km/h')
    number_gauge.pack(padx=10, pady=10)
    number_gauge.update_value(42)  # Update value example

    root.mainloop()
