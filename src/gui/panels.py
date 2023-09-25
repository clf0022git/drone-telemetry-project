import tkinter as tk
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

        # Playback Controls
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x")  # fill in x direction

        self.play_button = ttk.Button(control_frame, text="Play", command=self.video_player.play)
        self.play_button.pack(side="left", padx=5)  # pack to the left side with some padding

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.video_player.pause)
        self.pause_button.pack(side="left", padx=5)  # pack to the left side with some padding

        self.set_video_button = ttk.Button(control_frame, text="Set Video", command=self.getVideoPath)
        self.set_video_button.pack(side="left", padx=5)  # pack to the left side with some padding

    def getVideoPath(self):
        video_path = filedialog.askopenfilename(
            filetypes=[("MP4 files", "*.mp4")],
            title="Select a Video File"
        )
        if not video_path:  # if no file is selected, return
            return
        self.video_player.setVideoPath(video_path)


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

