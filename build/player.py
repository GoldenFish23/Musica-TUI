"""
This module contains the player class to control audio playback.
"""
from just_playback import Playback

class player(Playback):
    """A class to control audio playback."""
    def __init__(self):
        """Initialize the player.

            Args:
            super() : The parent class 'Playback'.
            self.audio_play_status : The current play status.
            self.audio_repeat_status : The current repeat status.
        """
        super().__init__()
        self.audio_play_status = "None"
        self.audio_repeat_status = "None"

    def load_file(self, file_path: str) -> None:
        """Load a file.
        
        Args:
            file_path (str): The path to the file to load.
        """
        super().load_file(file_path)
        self.audio_play_status = "None"
        print("File loaded successfully.")
        print(file_path)

    def play(self):
        """Play the audio. And toggle the play status."""
        if self.audio_play_status == "pause":
            super().resume()
            self.audio_play_status = "play"
        else:
            super().play()
            self.audio_play_status = "play"
        print(self.audio_play_status)
        
    def pause(self):
        """Pause the audio. And toggle the play status."""
        if self.audio_play_status == "play":
            super().pause()
            self.audio_play_status = "pause"
        print(self.audio_play_status)
        return self.audio_play_status

    def stop(self):
        """Stop the audio."""
        super().stop()
        self.audio_play_status = "None"
        print("Playback stopped")

    def repeat_toggle(self):
        """Toggle repeat mode."""
        if self.audio_repeat_status == "None":
            self.audio_repeat_status = "Single"
        elif self.audio_repeat_status == "Single":
            self.audio_repeat_status = "None"
        print(f"Repeat Mode: {self.audio_repeat_status}")
        return self.audio_repeat_status