import os
import tkinter as tk
import vlc
from src.config.gauges import GaugeCreator

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

        self.playing_backward = False
        self.paused_backward = False
        self.backward_timer_running = False

        self.do_backwards = False

        self.last_duration = None

        # Add play button
        # self.play_button = tk.Button(self.master, text="Play", command=self.play)
        # self.play_button.pack(side=tk.BOTTOM)

    def play(self):
        """Method to play the video."""
        if self.do_backwards:
            self.play_backward()
            return

        if not self.player.is_playing():
            self.player.play()
            #self.play_button.configure(text="Pause")
            self.start_time_update_timer()  # Start the timer when the video starts
        else:
            self.player.pause()
            #self.play_button.configure(text="Play")
            self.stop_time_update_timer()  # Stop the timer when the video is paused

    def play_backward(self):
        """Method to start or resume backward playback."""
        if not self.playing_backward:
            # If we aren't already playing backward
            self.playing_backward = True
            self.pause()  # Pause regular playback
            if not self.paused_backward:
                # If not resuming from a paused state, seek to the end
                end_time = self.player.get_length() // 1000  # Get video length in seconds
                self.seek(end_time - 1)  # Seek to the end of the video
            self.paused_backward = False  # Reset this flag as we are no longer paused
            self.initialize_rendering()
            # if not self.backward_timer_running:
            #     self.seek_backward_by_second()  # Start the backward playback
        else:
            # If already playing backward, then pause it
            self.pause_backward()

    def initialize_rendering(self):
        """Method to play the video forward briefly to initialize rendering."""
        self.player.play()
        self.master.after(100, self.play_backward)  # After a short delay, call `play_backward`

    def pause_backward(self):
        """Method to pause backward playback."""
        if self.playing_backward:
            self.paused_backward = True  # Set the paused state flag
            self.playing_backward = False  # Indicate that we're not actively playing backward
            self.backward_timer_running = False  # Indicate the backward timer is not running

    def stop_backward_playback(self):
        """Method to stop backward playback."""
        self.playing_backward = False

    def seek_backward_by_second(self):
        """Decrement video time by one second."""
        if self.playing_backward:
            self.backward_timer_running = True  # Indicate the backward timer is running
            current_time = self.player.get_time() // 1000  # Convert to seconds
            if current_time > 0:  # If not reached the start of the video
                self.seek(current_time - 1)  # Decrement by one second
                self.master.after(1000, self.seek_backward_by_second)  # Repeat after 1 second

    def start_time_update_timer(self):
        """Starts a timer to periodically check for time updates."""
        if not self.timer_running:
            self.timer_running = True
            self.check_time_update()
            self.check_duration_update()

    def stop_time_update_timer(self):
        """Stops the timer that checks for time updates."""
        self.timer_running = False

    def check_time_update(self):
        """Check if the video time has been updated."""
        if self.playing_backward:
            # If playing backward, just check the current time without triggering events
            current_time = self.player.get_time()  # Get current video time in milliseconds
            if current_time is not None:  # Could be None if the video hasn't started yet
                current_time = current_time // 1000  # Convert to seconds
                self.last_time = current_time
            return  # Exit early if playing backward

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

    def check_duration_update(self):
        """Check if the video duration has been updated."""
        current_duration = self.player.get_length()  # Get current video duration in milliseconds
        print(current_duration)
        if current_duration != self.last_duration:  # Check if the duration has changed
            self.trigger_event("duration-changed", current_duration // 1000)  # Convert to seconds and trigger event
            self.last_duration = current_duration  # Update last known duration

        # If the video is playing, continue to check the duration
        if self.player.is_playing():
            self.master.after(1000, self.check_duration_update)  # Check again after 1 second

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
        if self.do_backwards:
            self.pause_backward()
            return

        self.player.pause()

    def seek(self, seconds):
        """Method to seek through the video."""
        self.player.set_time(int(seconds * 1000))  # VLC uses milliseconds

    def set_video_path(self, video_path):
        """Method to set the video path and load the video in the player."""
        self.video_path = video_path
        self.media = self.instance.media_new(self.video_path)
        self.player.set_media(self.media)
        self.check_duration_update()

    def set_speed(self, speed_multiplier):
        """Method to adjust the video playback speed."""
        # set_rate() accepts a float for the speed multiplier.
        # 1.0 is normal speed, less than 1.0 is slower, greater than 1.0 is faster.
        if speed_multiplier == -1:
            self.do_backwards = True
            return
        else:
            self.do_backwards = False

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
