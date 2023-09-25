import tkinter as tk
import datetime
from tkinter import ttk, filedialog
from src.playback.video import VideoPlayer

class ConfigurationPanel(ttk.Frame):
    """
    Panel for configuration settings like selecting telemetry data fields,
    specifying display gauges, etc.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Configuration Panel")
        self.label.pack(pady=20)

        # TODO: Add more widgets and functionality for configuration

class PlaybackPanel(ttk.Frame):
    """
    Panel for video and telemetry data playback.
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Playback Panel")
        self.label.pack(pady=20)


        # TODO: Add widgets for video playback, gauges, playback controls, etc.

        # Prompt user for video file
        # video_path = filedialog.askopenfilename(
        #     filetypes=[("MP4 files", "*.mp4")],
        #     title="Select a Video File"
        # )
        # if not video_path:  # if no file is selected, return
        #     return

        # Video Player
        self.video_player = VideoPlayer(self, None)
        self.video_player.pack(fill="both", expand=True)

        # Seek Bar
        #self.seek_bar = ttk.Scale(self, orient="horizontal", command=self.on_seek)
        #self.seek_bar.pack(fill="x")
        #self.update_seek_bar()  # Start updating the seek bar

        # Playback Controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x")  # fill in x direction

        self.start_time = tk.Label(control_frame, text=str(datetime.timedelta(seconds=0)))
        self.start_time.pack(side="left")

        self.end_time = ttk.Label(control_frame, text=str(datetime.timedelta(seconds=0)))
        self.end_time.pack(side="right")

        self.progress_value = tk.IntVar(control_frame)
        self.progress_slider = tk.Scale(control_frame, variable=self.progress_value, from_=0, to=0, orient="horizontal", command=self.video_player.seek)
        self.progress_slider.pack(side="left", fill="x", expand=True)  # pack to the left side with some padding

        self.play_button = ttk.Button(control_frame, text="Play", command=self.video_player.play)
        self.play_button.pack(side="left", padx=5)  # pack to the left side with some padding

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.video_player.pause)
        self.pause_button.pack(side="left", padx=5)  # pack to the left side with some padding

        self.set_video_button = ttk.Button(control_frame, text="Set Video", command=self.getVideoPath)
        self.set_video_button.pack(side="left", padx=5)  # pack to the left side with some padding

        self.video_player.tk_video.bind("<<Duration>>", self.on_duration_changed)
        self.video_player.tk_video.bind("<<SecondChanged>>", self.on_second_changed)

    def on_duration_changed(self, event):
        """Update the seek bar when the video duration changes."""
        duration = self.video_player.tk_video.video_info()["duration"]
        self.end_time["text"] = str(datetime.timedelta(seconds=duration))
        self.progress_slider["to"] = duration
        #self.seek_bar.configure(to=duration)

    def on_second_changed(self, event):
        """Update the seek bar when the video time changes."""
        self.progress_value.set(self.video_player.tk_video.current_duration())

    def getVideoPath(self):
        video_path = filedialog.askopenfilename(
            filetypes=[("MP4 files", "*.mp4")],
            title="Select a Video File"
        )
        if not video_path:  # if no file is selected, return
            return
        self.video_player.setVideoPath(video_path)

    def on_seek(self, value):
        """Seek the video to the specified value."""
        self.video_player.seek(float(value))

    def update_seek_bar(self):
        """Update the seek bar based on the current video time."""
        current_time = self.video_player.get_time()
        self.seek_bar.set(current_time)
        self.after(100, self.update_seek_bar)  # Update every 100ms


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

