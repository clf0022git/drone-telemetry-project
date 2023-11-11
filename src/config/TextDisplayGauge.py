import tkinter as tk
from src.config.GaugeBase import GaugeBase


class TextDisplayGauge(GaugeBase):
    def __init__(self, master, name='Text Display', title='Text Gauge', description='', *args, **kwargs):
        super().__init__(master, name=name, title=title, description=description, *args, **kwargs)

        # Variable to hold the text value
        self.text_var = tk.StringVar(value="")

        # Label to display the text
        self.text_label = tk.Label(self, textvariable=self.text_var, font=('Arial', 24))
        self.text_label.pack(expand=True)

    def update_value(self, value):
        """Update the displayed text."""
        # Check if value is a string, as it should display text
        if isinstance(value, str):
            self.text_var.set(value)
            self.check_alarm(len(value))  # Example: trigger an alarm based on the length of the string
        else:
            raise ValueError("TextDisplayGauge can only display string values.")


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Text Display Gauge Example")

    text_gauge = TextDisplayGauge(root, title='Message', description='Current Status')
    text_gauge.pack(padx=10, pady=10)
    text_gauge.update_value("Hello, World!")  # Update value example

    root.mainloop()
