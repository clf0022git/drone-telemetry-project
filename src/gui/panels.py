import tkinter as tk
from tkinter import ttk, filedialog
from src.data.dataManager import get_statistics, swap_metric

import csv
import math

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

        self.label = ttk.Label(self, text="Configuration Panel")
        self.label.pack(pady=20)
        self.videoButton = ttk.Button(
            self,
            text='Load Video Playback'
        )
        self.videoButton.pack(pady=10)

        self.dataButton = ttk.Button(self, text="Load CSV", command=self.load_csv)
        self.dataButton.pack(pady=10)

        self.metricButton = ttk.Button(self, text="Swap from meters to feet", command=swap_metric(fields, rows, m_or_f))
        self.metricButton.pack(pady=10)

        self.statisticsButton = ttk.Button(self, text="Produce statistics", command=get_statistics(rows))
        self.statisticsButton.pack(pady=10)

    def load_csv(self):
        global fields
        global rows
        del fields[:]
        del rows[:]
        """Prompt the user to select a CSV file."""
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select a CSV File")
        if filename:  # If a file is selected
            print(f"CSV File Loaded: {filename}")
            # reading csv file
            with open(filename, 'r') as csvfile:
                # creating a csv reader object
                csvreader = csv.reader(csvfile)

                # extracting field names through first row
                fields = next(csvreader)

                # extracting each data row one by one
                for row in csvreader:
                    rows.append(row)

                # get total number of rows
                print("Total no. of rows: %d" % csvreader.line_num)

            # printing the field names
            print('Field names are:' + ', '.join(field for field in fields))


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
