import tkinter as tk
from tkinter import ttk
from src.gui.panels import ConfigurationPanel, PlaybackPanel, GaugeCustomizationPanel


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

        self.playback_panel = PlaybackPanel(self.notebook,)
        self.gauge_panel = GaugeCustomizationPanel(self.notebook)
        self.config_panel = ConfigurationPanel(self.notebook, self.playback_panel, self.gauge_panel)

        # Pass a reference of the playback panel to the gauge panel
        self.gauge_panel.set_data_manager(self.config_panel)

        # Pass a reference of the gauge customization panel to the config panel
        self.config_panel.gauge_customization_panel = self.gauge_panel

        self.notebook.add(self.config_panel, text="Configuration")
        self.notebook.add(self.gauge_panel, text="Gauge Customization")
        self.notebook.add(self.playback_panel, text="Playback")
        #self.notebook.add(self.stats_panel, text="Statistics")

    def create_frames(self):
        # (If there's any additional frame creation logic, it goes here)
        pass


class GaugeWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        # Window properties
        self.title("Telemetry Data Gauges")
        self.geometry("300x300")
        self.configure(bg="white")
        self.playback_panel = PlaybackPanel
        self.config_panel = ConfigurationPanel

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
