from tkinter import Frame, Tk
from tkVideoPlayer import TkinterVideo

class VideoPlayer(Frame):
    def __init__(self, master, video_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.video_path = video_path

        self.tk_video = TkinterVideo(master=self, scaled=True)
        self.tk_video.load(r"{}".format(self.video_path))
        self.tk_video.pack(expand=True, fill="both")
        self.tk_video.set_size((640, 480))

    def play(self):
        if self.video_path:
            self.tk_video.play()

    def pause(self):
        if self.video_path:
            self.tk_video.pause()

    def seek(self, seconds):
        if self.video_path:
            self.tk_video.seek(seconds * 1000)  # converting seconds to milliseconds

    def setVideoPath(self, video_path):
        self.video_path = video_path
        self.tk_video.load(r"{}".format(self.video_path))
