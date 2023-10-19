import tkinter as tk
from tkinter import ttk
from src.data.dataManager import DataProcessor


# initializing the titles and rows list
fields = []
rows = []
m_or_f = 0  # 0 = f and 1 = m


class ConfigurationPanel(ttk.Frame):
    """
    Panel for configuration settings like selecting telemetry data fields,
    specifying display gauges, etc.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.data_processor = DataProcessor(fields, rows)

        self.label = ttk.Label(self, text="Configuration Panel")
        self.label.pack(pady=20)
        self.videoButton = ttk.Button(
            self,
            text='Load Video Playback'
        )
        self.videoButton.pack(pady=10)

        self.dataButton = ttk.Button(
            self,
            text="Load CSV",
            command=self.load_csv
        )
        self.dataButton.pack(pady=10)

        self.metricButton = ttk.Button(
            self,
            text="Swap metrics",
            command=self.metric_swap
        )
        self.metricButton.pack(pady=10)

        self.statisticsButton = ttk.Button(
            self,
            text="Produce statistics",
            command=self.data_processor.get_statistics
        )
        self.statisticsButton.pack(pady=10)

    def load_csv(self):
        global fields
        global rows
        self.data_processor.load_csv()
        fields = self.data_processor.fields
        rows = self.data_processor.rows

    def metric_swap(self):
        global rows
        print(f"{self.data_processor.rows}")
        self.data_processor.swap_metric()
        rows = self.data_processor.rows
        print(f"First 6 rows after conversion: {rows[:6]}")


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
