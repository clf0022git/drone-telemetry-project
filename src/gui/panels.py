import tkinter as tk
import pandas as pd
import csv
import time

# initializing the titles and rows list
fields = []
rows = []
m_or_f = 0  # 0 = f and 1 = m

import datetime
from tkinter import ttk, filedialog
from src.playback.video import VideoPlayer
from src.data.input import DataManager


class ConfigurationPanel(ttk.Frame):
    """
    Panel for configuration settings like selecting telemetry data fields,
    specifying display gauges, etc.
    """

    def __init__(self, parent, playback_panel, stats_panel):
        super().__init__(parent)

        # Instantiate a DataManager object
        self.data_manager = DataManager()

        self.label = ttk.Label(self, text="Configuration Panel")
        self.label.pack(pady=10)
        self.playback_panel = playback_panel
        self.stats_panel = stats_panel

        # Button to load video file
        self.load_video_btn = ttk.Button(self, text="Load Video", command=self.load_video)
        self.load_video_btn.pack(pady=5)

        # Button to load CSV file
        self.load_csv_btn = ttk.Button(self, text="Load CSV", command=self.load_csv)
        self.load_csv_btn.pack(pady=5)

        self.metricButton = ttk.Button(self, text="Swap from meters to feet", command=self.swap_metric)
        self.metricButton.pack(pady=10)

        # Frames that hold the fieldnames and their options
        self.fieldnames_gauge_group = tk.Frame(self)
        self.fieldnames_gauge_group.pack(pady=5, side=tk.TOP)
        self.fieldnames_group = tk.Frame(self.fieldnames_gauge_group)
        self.fieldnames_group.pack(side=tk.LEFT)
        self.datatypes_group = tk.Frame(self.fieldnames_gauge_group)
        self.datatypes_group.pack(side=tk.LEFT)
        self.gauge_options_group = tk.Frame(self.fieldnames_gauge_group)
        self.gauge_options_group.pack(side=tk.LEFT)

        # Combobox that allows changing datatypes
        self.current_datatype_label = ttk.Label(self.datatypes_group, text="Current Datatype:")
        self.current_datatype_label.pack(pady=5)
        self.current_datatype_text = ttk.Label(self.datatypes_group, text="No item selected.")
        self.current_datatype_text.pack(pady=5)

        self.datatypes_label = ttk.Label(self.datatypes_group, text="Change Datatype:")
        self.datatypes_label.pack(pady=5)
        self.available_datatypes = ["object", "bool", "int64", "float64"]
        self.datatype_combo = ttk.Combobox(self.datatypes_group, value=self.available_datatypes, width=10)
        self.datatype_combo.current(0)
        self.datatype_combo.pack(pady=5)
        self.datatype_combo.bind("<<ComboboxSelected>>", self.change_datatype)

        # Listbox to select one field
        self.fieldnames_label = ttk.Label(self.fieldnames_group, text="Select Field:")
        self.fieldnames_label.pack(pady=5)
        self.fieldnames_list = tk.Listbox(self.fieldnames_group, selectmode=tk.SINGLE, height=5, exportselection=0,
                                          width=30)
        self.fieldnames_list.pack(pady=5)
        self.fieldnames = []
        # Button to show gauges
        self.show_gauges_btn = ttk.Button(self.fieldnames_group, text="Show Gauges", command=self.show_gauges)
        self.show_gauges_btn.pack(pady=10)

        # Listbox to show gauge options for a field
        self.gauge_types_label = ttk.Label(self.gauge_options_group, text="Possible Gauges:")
        self.gauge_types_label.pack(pady=5)
        self.gauge_types_list = tk.Listbox(self.gauge_options_group, selectmode=tk.SINGLE, height=5, exportselection=0,
                                           width=30)
        self.gauge_types_list.pack(pady=5)
        self.gauge_types = []
        # Button to select field with gauge
        self.select_field_btn = ttk.Button(self.gauge_options_group, text="Select Field", command=self.select_field)
        self.select_field_btn.pack(pady=10)

        # Defines a frame for user selections to be placed into
        self.user_selection_frame = tk.Frame(self)
        self.user_selection_frame.pack(pady=5, side=tk.TOP)
        self.user_selection_list = tk.Listbox(self.user_selection_frame, selectmode=tk.SINGLE, height=5,
                                              exportselection=0, width=30)
        self.user_selection_list.pack(pady=5)
        # Button to select field with gauge
        self.select_field_btn = ttk.Button(self.user_selection_frame, text="Remove Field", command=self.remove_field)
        self.select_field_btn.pack(pady=10)

        self.speed_label = ttk.Label(self, text="Playback Speed:")
        self.speed_label.pack(pady=5)

        # Using radio buttons for playback speed options
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=5)

        self.playback_speed = tk.IntVar(value=1)  # default speed 1X
        self.speed_1x = ttk.Radiobutton(self.speed_frame, text="1X", variable=self.playback_speed, value=1,
                                        command=self.set_playback_speed)
        self.speed_1x.grid(row=0, column=0, padx=5, pady=2)
        self.speed_5x = ttk.Radiobutton(self.speed_frame, text="5X", variable=self.playback_speed, value=5,
                                        command=self.set_playback_speed)
        self.speed_5x.grid(row=1, column=0, padx=5, pady=2)
        self.speed_10x = ttk.Radiobutton(self.speed_frame, text="10X", variable=self.playback_speed, value=10,
                                         command=self.set_playback_speed)
        self.speed_10x.grid(row=2, column=0, padx=5, pady=2)
        self.speed_1x_backwards = ttk.Radiobutton(self.speed_frame, text="1X backwards", variable=self.playback_speed,
                                                  value=-1, command=self.set_playback_speed)
        self.speed_1x_backwards.grid(row=3, column=0, padx=5, pady=2)

    def swap_metric(self):
        global fields
        global rows
        global m_or_f
        """Check what metric is already in use and swap to the other one"""
        if m_or_f == 0:  # case for the units being in meters
            for row in rows:
                i = 0
                while i < len(row):
                    index = fields[i].find('[m')
                    if index != -1 and row[i] != '':
                        row[i] = str(float(row[i]) * 39.76)
                    i += 1
            # printing first 6 rows
            print('\nFirst 6 rows are:\n')
            for row in rows[:6]:
                # parsing each column of a row
                for col in row:
                    print("%10s" % col, end=" "),
                print('\n')
            m_or_f = 1
        else:
            for row in rows:
                i = 0
                while i < len(row):
                    index = fields[i].find('[m')
                    if index != -1 and row[i] != '':
                        row[i] = str(float(row[i]) / 39.76)
                    i += 1
            # printing first 6 rows
            print('\nFirst 6 rows are:\n')
            for row in rows[:6]:
                # parsing each column of a row
                for col in row:
                    print("%10s" % col, end=" "),
                print('\n')
            m_or_f = 0

        # Defines a frame for user selections to be placed into
        self.user_selection_frame = tk.Frame(self)
        self.user_selection_frame.pack(pady=5, side=tk.TOP)
        self.user_selection_list = tk.Listbox(self.user_selection_frame, selectmode=tk.SINGLE, height=5,
                                              exportselection=0, width=30)
        self.user_selection_list.pack(pady=5)
        # Button to select field with gauge
        self.select_field_btn = ttk.Button(self.user_selection_frame, text="Remove Field", command=self.remove_field)
        self.select_field_btn.pack(pady=10)

    def load_video(self):
        """Prompt the user to select a video file."""
        video_path = filedialog.askopenfilename(filetypes=[("MOV files", "*.mov"), ("MP4 files", "*.mp4"), ("All files", "*.*")], title="Select a Video File")
        if video_path:  # If a file is selected
            print(f"Video File Loaded: {video_path}")
            self.playback_panel.set_video_path(video_path)

    def load_csv(self):
        """Prompt the user to select a CSV file."""
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select a CSV File")
        if csv_path:  # If a file is selected
            print(f"CSV File Loaded: {csv_path}")

        if not csv_path:
            return

        self.data_manager.parse(csv_path)
        self.fieldnames_list = self.data_manager.load_fields(self.fieldnames_list, self.current_datatype_text)

    def show_gauges(self):
        """Show the user the gauges that are available to them"""
        selected_field = None
        self.gauge_types_list.delete(0, 'end')  # clear list before each call to update

        selected_field = [self.fieldnames_list.get(i) for i in self.fieldnames_list.curselection()]

        if selected_field:
            print(f"Selected Field: {', '.join(selected_field)}")
            # add the elements to the gauge_types listbox
            self.gauge_types_list.insert(0, *self.data_manager.identify_gauges(selected_field, self.datatype_combo))
            # Functionality to ask user about the type of the data probably in between identifying gauges and
            # updating the list

        else:
            print("Please select a field.")

    def remove_field(self):
        k = 0
        selected_field = [self.user_selection_list.get(i) for i in self.user_selection_list.curselection()]

        for j, element in enumerate(self.user_selection_list.curselection()):
            k = j

        if selected_field:
            print(f"Selected Gauge: {', '.join(selected_field)}")
            self.user_selection_list.delete(0, 'end')  # clear list before each call to update
            self.user_selection_list.insert(0, *self.data_manager.delete_selection(k))

        else:
            print("Please select a field to remove.")

    def select_field(self):
        """Will call functionality to send selected fields to function"""
        selected_gauge = [self.gauge_types_list.get(i) for i in self.gauge_types_list.curselection()]

        if selected_gauge:
            print(f"Selected Gauge: {', '.join(selected_gauge)}")
            self.user_selection_list.delete(0, 'end')  # clear list before each call to update
            gt_list = self.data_manager.confirm_selection(selected_gauge)
            if len(gt_list) <= 10:
                self.user_selection_list.insert(0, *gt_list)
                # Functionality to ask user about the type of the data probably in between identifying gauges and
                # updating the list
            else:
                print("You already have ten fields selected!")
                self.user_selection_list.insert(0, *gt_list)

        else:
            print("Please select a gauge.")

    def change_datatype(self):
        self.gauge_types_list.delete(0, 'end')
        self.gauge_types_list.insert(0, *self.data_manager.check_datatype(self.datatype_combo.get()))

    def set_playback_speed(self):
        speed = self.playback_speed.get()
        print(f"Setting playback speed to: {speed}X")
        if self.playback_panel.video_player:
            self.playback_panel.video_player.set_speed(speed)


class PlaybackPanel(ttk.Frame):
    """
    Panel for video and telemetry data playback.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Playback Panel")
        self.label.pack(pady=20)

        # Video Player (initialization postponed until a video is selected)
        self.video_player = None
        self.video_path = None

        self.current_time = 0
        
        self.is_seeking = False

        # Control panel
        control_panel = ttk.Frame(self)
        control_panel.pack(side="bottom", fill="x")

        # Current time label
        self.current_time_label = ttk.Label(control_panel, text="00:00")
        self.current_time_label.pack(side="left")

        # Seek bar
        self.seek_var = tk.DoubleVar()
        self.seek_bar = ttk.Scale(control_panel, variable=self.seek_var, from_=0, to=100, orient="horizontal",
                                  command=self.start_seek)
        self.seek_bar.pack(side="left", fill="x", expand=True)
        self.seek_bar.bind("<ButtonRelease-1>", self.stop_seek)

        # Total time label
        self.total_time_label = ttk.Label(control_panel, text="00:00")
        self.total_time_label.pack(side="right")

        # Play button
        self.play_button = ttk.Button(control_panel, text="Play", command=self.play_video)
        self.play_button.pack(side="left")

        # Pause button
        self.pause_button = ttk.Button(control_panel, text="Pause", command=self.pause_video)
        self.pause_button.pack(side="left")

        # Set initial state of control buttons
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

        self.update_ui()

    def set_video_path(self, video_path):
        self.video_path = video_path
        if self.video_path:  # if a file is selected
            # self.video_path = video_path
            if self.video_player is None:
                self.video_player = VideoPlayer(self, self.video_path)
                self.video_player.pack(fill="both", expand=True)
                # self.video_player.bind_event("second-changed", self.on_second_changed)
                # self.video_player.bind_event("duration-changed", self.on_duration_changed)
            else:
                self.video_player.set_video_path(self.video_path)

            # Enable control buttons now that a video is loaded
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)

    def play_video(self):
        if self.video_player:
            self.video_player.play()
            self.seek_bar["to"] = self.video_player.player.get_length() / 1000

    def pause_video(self):
        if self.video_player:
            self.video_player.pause()

    def start_seek(self, event):
        self.is_seeking = True

    def stop_seek(self, event):
        self.video_player.player.set_time(int(self.seek_var.get() * 1000))  # Seconds to milliseconds
        self.is_seeking = False

    def update_ui(self):
        """Update the UI every 500ms."""
        if self.video_player and self.video_player.player.is_playing():
            # Get the current and total time of the video
            current_time = self.video_player.player.get_time() / 1000  # Milliseconds to seconds
            total_time = self.video_player.player.get_length() / 1000  # Milliseconds to seconds

            # Set the total time once if it's not already set
            if self.seek_bar['to'] != total_time:
                self.seek_bar['to'] = total_time
                self.total_time_label['text'] = time.strftime('%H:%M:%S', time.gmtime(total_time))

            # Update the current time label
            self.current_time_label['text'] = time.strftime('%H:%M:%S', time.gmtime(current_time))

            # Update seek bar position only if the user is not seeking
            if not self.is_seeking:
                self.seek_var.set(current_time)

        # Schedule the update_ui method to be called after 500ms
        self.after(500, self.update_ui)


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
