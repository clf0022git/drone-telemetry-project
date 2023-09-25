import tkinter as tk
from tkinter import ttk

class ConfigurationPanel(ttk.Frame):
    """
    Panel for configuration settings like selecting telemetry data fields,
    specifying display gauges, etc.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Configuration Panel")
        self.label.pack(pady=20)
        self.videoButton = ttk.Button(
            self,
            text='Load Video Playback'
        )
        self.videoButton.pack(
            ipadx=20,
            ipady=20,
            expand=True
        )
        self.videoButton.place(x=415, y=240)

        self.dataButton = ttk.Button(
            self,
            text='Load Flight Data'
        )
        self.dataButton.pack(
            ipadx=20,
            ipady=20,
            expand=True
        )
        self.dataButton.place(x=425, y=280)

class PlaybackPanel(ttk.Frame):
    """
    Panel for video and telemetry data playback.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Playback Panel")
        self.label.pack(pady=20)

        # TODO: Add widgets for video playback, gauges, playback controls, etc.

class StatisticsPanel(ttk.Frame):
    """
    Panel for displaying statistics of selected telemetry data fields.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Statistics Panel")
        self.label.pack(pady=20)

        # TODO: Add widgets to display statistics like min, max, average, etc.

# Additional panels can be added here...

