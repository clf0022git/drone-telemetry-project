import tkinter as tk
import datetime
from tkinter import ttk, filedialog
from src.playback.video import VideoPlayer

import tkinter as tk
from tkinter import ttk, filedialog


class ConfigurationPanel(ttk.Frame):
    """
    Panel for configuration settings like selecting telemetry data fields,
    specifying display gauges, etc.
    """

    def __init__(self, parent, playback_panel):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Configuration Panel")
        self.label.pack(pady=10)
        self.playback_panel = playback_panel

        # Button to load video file
        self.load_video_btn = ttk.Button(self, text="Load Video", command=self.load_video)
        self.load_video_btn.pack(pady=5)

        # Button to load CSV file
        self.load_csv_btn = ttk.Button(self, text="Load CSV", command=self.load_csv)
        self.load_csv_btn.pack(pady=5)

        # Listbox to select multiple gauge types
        self.gauge_label = ttk.Label(self, text="Select Gauge Types:")
        self.gauge_label.pack(pady=5)
        self.gauge_list = tk.Listbox(self, selectmode=tk.MULTIPLE, height=5, exportselection=0)
        self.gauge_list.pack(pady=5)
        self.gauges = ["Circle - 90°", "Circle - 180°", "Circle - 270°", "Circle - 360°", "Bar", "X-Plot", "X-by-Y-plot", "Character Display", "Text Display", "Clock", "Stopwatch", "Running Time", "On/off light"]
        for gauge in self.gauges:
            self.gauge_list.insert(tk.END, gauge)

        # Button to confirm configuration
        self.confirm_btn = ttk.Button(self, text="Confirm Configuration", command=self.confirm_config)
        self.confirm_btn.pack(pady=10)

        self.speed_label = ttk.Label(self, text="Playback Speed:")
        self.speed_label.pack(pady=5)

        # Using radio buttons for playback speed options
        self.playback_speed = tk.IntVar(value=1)  # default speed 1X
        self.speed_1x = ttk.Radiobutton(self, text="1X", variable=self.playback_speed, value=1,
                                        command=self.set_playback_speed)
        self.speed_1x.pack(anchor='w', padx=20)
        self.speed_5x = ttk.Radiobutton(self, text="5X", variable=self.playback_speed, value=5,
                                        command=self.set_playback_speed)
        self.speed_5x.pack(anchor='w', padx=20)
        self.speed_10x = ttk.Radiobutton(self, text="10X", variable=self.playback_speed, value=10,
                                         command=self.set_playback_speed)
        self.speed_10x.pack(anchor='w', padx=20)

    def load_video(self):
        """Prompt the user to select a video file."""
        video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")], title="Select a Video File")
        if video_path:  # If a file is selected
            print(f"Video File Loaded: {video_path}")
            self.playback_panel.set_video_path(video_path)

    def load_csv(self):
        """Prompt the user to select a CSV file."""
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select a CSV File")
        if csv_path:  # If a file is selected
            print(f"CSV File Loaded: {csv_path}")

    def confirm_config(self):
        """Confirm the selected configuration settings."""
        selected_gauges = [self.gauge_list.get(i) for i in self.gauge_list.curselection()]
        if selected_gauges:
            print(f"Selected Gauge Types: {', '.join(selected_gauges)}")
        else:
            print("No gauge type selected.")

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

        # Playback Controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x")  # fill in the x direction

        self.start_time = ttk.Label(control_frame, text=str(datetime.timedelta(seconds=0)))
        self.start_time.pack(side="left")

        self.end_time = ttk.Label(control_frame, text=str(datetime.timedelta(seconds=0)))
        self.end_time.pack(side="right")

        self.progress_value = tk.IntVar(control_frame)
        self.progress_slider = tk.Scale(control_frame, variable=self.progress_value, from_=0, to=0, orient="horizontal")
        self.progress_slider.pack(side="left", fill="x", expand=True)

        self.play_button = ttk.Button(control_frame, text="Play", command=self.play_video)
        self.play_button.pack(side="left", padx=5)

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.pause_video)
        self.pause_button.pack(side="left", padx=5)

        #self.set_video_button = ttk.Button(control_frame, text="Set Video", command=self.set_video_path)
        #self.set_video_button.pack(side="left", padx=5)

        # Set initial state of control buttons
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

    def set_video_path(self, video_path):
        self.video_path = video_path
        if self.video_path:  # if a file is selected
            #self.video_path = video_path
            if self.video_player is None:
                self.video_player = VideoPlayer(self, self.video_path)
                self.video_player.pack(fill="both", expand=True)
                self.video_player.bind_event("second-changed", self.on_second_changed)
                self.video_player.bind_event("duration-changed", self.on_duration_changed)
            else:
                self.video_player.set_video_path(self.video_path)

            # Enable control buttons now that a video is loaded
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)

            #self.update_progress_slider()

    def play_video(self):
        if self.video_player:
            self.video_player.play()

    def pause_video(self):
        if self.video_player:
            self.video_player.pause()

    def on_duration_changed(self, duration):
        """Update the UI when the video duration is available."""
        self.end_time["text"] = str(datetime.timedelta(milliseconds=duration))
        self.progress_slider["to"] = duration / 1000  # converting ms to s

    def on_second_changed(self, current_time):
        """Update the UI when the video time changes."""
        #self.progress_value.set(datetime.timedelta(seconds=current_time))
        self.start_time["text"] = str(datetime.timedelta(seconds=current_time))
        self.update_progress_slider(current_time)

    def update_progress_slider(self, current_time):
        """Update the progress slider based on the current video time."""
        if self.video_player:
            #current_time = self.video_player.get_current_time()  # Retrieve current time from the video player
            self.progress_slider.set(current_time)  # Update slider position

            # Schedule the `update_progress_slider` to run again after 1000ms (1 second)
            #self.after(1000, self.update_progress_slider)


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

