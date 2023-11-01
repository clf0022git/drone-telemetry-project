import os
import tkinter as tk
import vlc


class VideoPlayer(tk.Frame):
    def __init__(self, master, video_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.video_path = video_path

        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Creating new tkinter window with frame
        self.video_frame = tk.Frame(self.master)
        self.video_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.video_frame)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # Set the media player into the frame
        self.player.set_hwnd(self.canvas.winfo_id())
        self.media = self.instance.media_new(self.video_path)
        self.player.set_media(self.media)

        # Variables to manage time update event
        self.last_time = None
        self.timer_running = False
        self.event_handlers = {"second-changed": [], "duration-changed": []}  # Custom event handlers

        self.video_length = self.player.get_length()

        # Add play button
        # self.play_button = tk.Button(self.master, text="Play", command=self.play)
        # self.play_button.pack(side=tk.BOTTOM)

    def play(self):
        """Method to play the video."""
        if not self.player.is_playing():
            self.player.play()
            #self.play_button.configure(text="Pause")
            self.start_time_update_timer()  # Start the timer when the video starts
        else:
            self.player.pause()
            #self.play_button.configure(text="Play")
            self.stop_time_update_timer()  # Stop the timer when the video is paused

    def start_time_update_timer(self):
        """Starts a timer to periodically check for time updates."""
        if not self.timer_running:
            self.timer_running = True
            self.check_time_update()

    def stop_time_update_timer(self):
        """Stops the timer that checks for time updates."""
        self.timer_running = False

    def check_time_update(self):
        """Check if the video time has been updated."""
        if self.timer_running:
            current_time = self.player.get_time()  # Get current video time in milliseconds
            if current_time is not None:  # Could be None if the video hasn't started yet
                current_time = current_time // 1000  # Convert to seconds

                # If the time has changed since the last check and it's not the same second
                if self.last_time is not None and current_time != self.last_time:
                    self.trigger_event("second-changed", current_time)

                self.last_time = current_time

            # Check again after 200 milliseconds
            self.master.after(200, self.check_time_update)

    def bind_event(self, event, handler):
        """Bind an event to a handler function."""
        if event in self.event_handlers:
            self.event_handlers[event].append(handler)
        else:
            print(f"Unknown event: {event}")

    def trigger_event(self, event, *args):
        """Trigger all handlers for an event."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                handler(*args)

    def pause(self):
        """Method to pause the video."""
        self.player.pause()

    def seek(self, seconds):
        """Method to seek through the video."""
        self.player.set_time(int(seconds * 1000))  # VLC uses milliseconds

    def set_video_path(self, video_path):
        """Method to set the video path and load the video in the player."""
        self.video_path = video_path
        self.media = self.instance.media_new(self.video_path)
        self.player.set_media(self.media)

    def set_speed(self, speed_multiplier):
        """Method to adjust the video playback speed."""
        # set_rate() accepts a float for the speed multiplier.
        # 1.0 is normal speed, less than 1.0 is slower, greater than 1.0 is faster.
        self.player.set_rate(speed_multiplier)


# Example usage
if __name__ == "__main__":
    def on_second_changed(current_time):
        """Custom event handler function."""
        print(f"Second changed: {current_time}")

    root = tk.Tk()
    root.geometry("800x600")  # Set the size of the app to be 800x600
    player = VideoPlayer(root, "DJI_0001.MOV")
    player.pack(fill=tk.BOTH, expand=1)
    player.bind_event("second-changed", on_second_changed)  # Bind custom event handler
    player.play()
    player.set_speed(1)
    root.mainloop()
