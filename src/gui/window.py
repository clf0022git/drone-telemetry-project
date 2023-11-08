import tkinter as tk
from tkinter import ttk
from src.gui.panels import ConfigurationPanel, PlaybackPanel, StatisticsPanel
from src.data.input import DataManager


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Setting window properties
        self.title("Drone Telemetry Playback")
        self.geometry("1000x700")
        self.configure(bg="white")

        # Creating notebook for tabbed interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

        # Adding panels to the notebook as separate tabs

        self.playback_panel = PlaybackPanel(self.notebook)
        self.stats_panel = StatisticsPanel(self.notebook)
        self.config_panel = ConfigurationPanel(self.notebook, self.playback_panel, self.stats_panel)

        self.notebook.add(self.config_panel, text="Configuration")
        self.notebook.add(self.playback_panel, text="Playback")
        self.notebook.add(self.stats_panel, text="Statistics")

    def create_frames(self):
        # (If there's any additional frame creation logic, it goes here)
        pass


class gaugeWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window properties
        self.title("Telemetry Data Gauges")
        self.geometry("1000x700")
        self.configure(bg="white")
        self.playback_panel = PlaybackPanel
        self.config_panel = ConfigurationPanel

    #def drawGauges(self):



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
