import tkinter as tk
from tkinter import ttk, filedialog


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Setting window properties
        self.title("Drone Telemetry Playback")
        self.geometry("800x600")
        self.configure(bg="white")

        # Creating frames (or panels) as placeholders
        self.create_frames()

    def create_frames(self):
        """Create frames or panels for different sections of the app"""

        # Frame for file selection
        self.file_frame = ttk.Frame(self, padding="10")
        self.file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.csv_label = ttk.Label(self.file_frame, text="Select CSV:")
        self.csv_label.pack(side=tk.LEFT, padx=(0, 10))

        self.csv_path_var = tk.StringVar()
        self.csv_entry = ttk.Entry(self.file_frame, textvariable=self.csv_path_var, width=50)
        self.csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.csv_button = ttk.Button(self.file_frame, text="Browse", command=self.browse_csv)
        self.csv_button.pack(side=tk.LEFT, padx=(10, 0))

        # TODO: Add similar blocks for video selection and other interface elements.

    def browse_csv(self):
        """Open file dialog to select CSV"""
        csv_file_path = tk.filedialog.askopenfilename(title="Select the telemetry CSV file",
                                                      filetypes=[("CSV files", "*.csv")])
        if csv_file_path:
            self.csv_path_var.set(csv_file_path)

        # TODO: Implement file reading and other functionalities


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
