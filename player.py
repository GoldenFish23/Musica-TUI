from just_playback import Playback

class player(Playback):
    def __init__(self):
        super().__init__()
        self.audio_play_status = "None"
        self.audio_repeat_status = "None"

    def play(self):
        """Play or resume audio based on internal status."""
        if self.audio_play_status == "pause":
            super().resume()
        elif self.audio_play_status == "None":
            super().play()
        self.audio_play_status = "play"
        return self.audio_play_status
        
    def pause(self):
        """Pause audio if currently playing."""
        if self.audio_play_status == "play":
            super().pause()
            self.audio_play_status = "pause"
        return self.audio_play_status

    def repeat(self):
        """Toggle repeat mode."""
        if self.audio_repeat_status == "None":
            self.audio_repeat_status = "Single"
        elif self.audio_repeat_status == "Single":
            self.audio_repeat_status = "None"
        return self.audio_repeat_status
