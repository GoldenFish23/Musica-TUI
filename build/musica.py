import os, math, random, time, json
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Label, Static
from textual.containers import Vertical, Horizontal, Container
from textual.binding import Binding
from textual.reactive import reactive
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from player import player
from UI import UI
from themes import THEMES



class Logo(Static):
    """
    This class is for building logo.
    """
    border_style = reactive("cyan")

    def __init__(self):
        super().__init__()
        self.ui = UI()
        self.logo = self.ui.get_logo()
        self.descriptor = self.ui.get_descriptor()

    def render(self):
        return Panel(
            Align.center(self.logo, vertical="middle"),
            subtitle=self.descriptor,
            subtitle_align="center",
            border_style=self.border_style,
        )

class TrackItem(ListItem):
    """
    This class represents a track item.
    """
    def __init__(self, track_name: str, full_path: str):
        super().__init__(Label(track_name))
        self.track_name = track_name
        self.full_path = full_path

class TrackManager:
    """
    This class manages the tracks.
    """
    def __init__(self):
        self.tracks = [] 

    def scan_tracks(self):
        """
        Scanning all folders mentioned in settings.json
        """
        self.tracks = [] # Reset tracks
        try:
            # Get path relative to the script location
            base_path = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(base_path, "settings.json")
            
            with open(settings_path, "r") as f:
                settings = json.load(f)
            paths = settings["settings"]["scan_paths"]
            for path in paths:
                if os.path.exists(path) and os.path.isdir(path):
                    # Append new tracks found in this path (Case-insensitive check)
                    new_tracks = [
                        TrackItem(f, os.path.join(path, f)) 
                        for f in os.listdir(path) if f.lower().endswith(".mp3")
                    ]
                    self.tracks.extend(new_tracks)
                else:
                    print(f"Warning: Scan path '{path}' is not a valid directory.")
        except Exception as e:
            print(f"Error scanning tracks: {e}")
        return self.tracks  


class Visualizer(Static):
    """A visualizer widget with Wave mode."""
    
    mode = reactive("wave")  # wave, off
    is_playing = reactive(False)
    accent_color = reactive("cyan")
    
    def on_mount(self) -> None:
        self.set_interval(0.1, self.update_visualizer)
        self.time_offset = 0.0

    def update_visualizer(self) -> None:
        if not self.display:
            return
            
        if not self.is_playing:
            self.update(Panel(Align.center("[dim]Paused[/dim]", vertical="middle"), 
                            # title="[bold dim]Visualizer[/]", border_style="dim"
                            ))
            return

        self.time_offset += 0.2
        
        if self.mode == "wave":
            self.render_wave()
        else:
            self.update("")

    def render_wave(self) -> None:
        """Mode 1: Wave (Oscilloscope style)"""
        width = 40
        height = 10
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        for x in range(width):
            # Combine sine waves for organic look
            y_float = math.sin(x * 0.3 + self.time_offset) * 2.5 + \
                      math.sin(x * 0.8 - self.time_offset * 1.5) * 1.0
            
            y = int(height // 2 + y_float)
            
            if 0 <= y < height:
                grid[y][x] = f"[{self.accent_color}]•[/]"
                
        art = "\n".join("".join(row) for row in grid)
        self.update(Panel(Align.center(art, vertical="middle"), 
                          border_style=self.accent_color))

class MusicApp(App):
    CSS = """
    Logo {
        height: auto;
        dock: top;
        margin-bottom: 1;
    }
    #main-container {
        height: 1fr;
    }
    ListView {
        width: 30%;
        height: 100%;
        border: solid cyan;
    }
    .full-width {
        width: 100%;
    }
    Visualizer {
        width: 70%;
        height: 100%;
        padding: 0;
        border: solid cyan;
    }
    #track-list {
        border: solid cyan;
    }
    #viz {
        border: solid cyan;
    }
    """
    
    current_theme_name = reactive("default")
    visualizer_enabled = reactive(True)
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("s", "scan", "Scan"),
        Binding("space", "play_pause", "Play/Pause"),
        Binding("r", "toggle_repeat", "Repeat"),
        Binding("t", "toggle_theme", "Theme"),
        Binding("v", "toggle_viz_mode", "Viz Mode"),
        Binding("b", "toggle_viz_display", "Toggle Viz"),
    ]

    def __init__(self):
        super().__init__()
        self.track_manager = TrackManager()
        self.player = player()
        self.load_settings()

    def load_settings(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(base_path, "settings.json")
            with open(settings_path, "r") as f:
                settings = json.load(f)
            self.current_theme_name = settings["settings"].get("theme", "default")
            self.visualizer_enabled = settings["settings"].get("visualizer") != "disabled"
        except Exception:
            self.current_theme_name = "default"
            self.visualizer_enabled = True

    def save_settings(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(base_path, "settings.json")
            with open(settings_path, "r") as f:
                settings = json.load(f)
            settings["settings"]["theme"] = self.current_theme_name
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            self.notify(f"Error saving settings: {e}", severity="error")

    def on_mount(self) -> None:
        self.set_interval(0.5, self.check_playback_status)
        self.apply_theme()
        # Ensure initial state matches settings
        self.call_after_refresh(self.watch_visualizer_enabled, self.visualizer_enabled)

    def compose(self) -> ComposeResult:
        """
        Composing the UI.
        """
        yield Header()
        yield Logo()
        with Horizontal(id="main-container"):
            lv = ListView(id="track-list")
            lv.border_title = "Playlist"
            lv.border_title_align = "left"
            yield lv
            
            viz = Visualizer(id="viz")
            viz.border_title = "Visualizer"
            viz.border_title_align = "right"
            yield viz

        yield Footer()

    def action_scan(self) -> None:
        track_list_widget = self.query_one("#track-list", ListView)
        track_list_widget.clear()
        
        # Scan returns list of TrackItems now
        track_items = self.track_manager.scan_tracks()
        for item in track_items:
            track_list_widget.append(item)
        
        self.notify(f"Found {len(track_items)} tracks!")

    def on_list_view_selected(self, event: ListView.Selected):
        # Retrieve full path from the selected TrackItem
        track_name = event.item.track_name
        file_path = event.item.full_path
        
        try:
            self.player.load_file(file_path)
            self.player.play()
            if self.visualizer_enabled:
                viz = self.query_one(Visualizer)
                viz.is_playing = True
            self.notify(f"Playing: {track_name}")
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")

    def action_play_pause(self) -> None:
        if self.player.audio_play_status == "play":
            self.player.pause()
            if self.visualizer_enabled:
                viz = self.query_one(Visualizer)
                viz.is_playing = False
        else:
            self.player.play()
            if self.visualizer_enabled:
                viz = self.query_one(Visualizer)
                viz.is_playing = True

    def action_toggle_viz_mode(self) -> None:
        """Switch visualizer modes."""
        if not self.visualizer_enabled:
            self.notify("Visualizer is hidden. Press 'b' to show it.", severity="warning")
            return
        viz = self.query_one(Visualizer)
        modes = ["wave", "off"]
        current_idx = modes.index(viz.mode)
        next_mode = modes[(current_idx + 1) % len(modes)]
        viz.mode = next_mode
        self.notify(f"Mode: {next_mode.title()}")

    def action_toggle_viz_display(self) -> None:
        """Toggle visualizer visibility."""
        self.visualizer_enabled = not self.visualizer_enabled
        self.save_settings_visualizer()
        status = "Shown" if self.visualizer_enabled else "Hidden"
        self.notify(f"Visualizer: {status}")

    def watch_visualizer_enabled(self, enabled: bool) -> None:
        """Update layout when visualizer is toggled."""
        try:
            lv = self.query_one("#track-list")
            viz = self.query_one("#viz")
            if enabled:
                lv.remove_class("full-width")
                viz.display = True
            else:
                lv.add_class("full-width")
                viz.display = False
        except Exception:
            pass

    def save_settings_visualizer(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            settings_path = os.path.join(base_path, "settings.json")
            with open(settings_path, "r") as f:
                settings = json.load(f)
            settings["settings"]["visualizer"] = "enabled" if self.visualizer_enabled else "disabled"
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception:
            pass

    def action_toggle_theme(self) -> None:
        """Cycle through themes."""
        theme_keys = list(THEMES.keys())
        current_idx = theme_keys.index(self.current_theme_name)
        next_idx = (current_idx + 1) % len(theme_keys)
        self.current_theme_name = theme_keys[next_idx]
        self.apply_theme()
        self.save_settings()
        self.notify(f"Theme: {THEMES[self.current_theme_name]['name']}")

    def apply_theme(self) -> None:
        """Apply current theme colors to UI components."""
        theme = THEMES.get(self.current_theme_name, THEMES["default"])
        accent = theme["accent"]
        
        # Update Logo
        logo = self.query_one(Logo)
        logo.border_style = accent
        
        # Update ListView
        lv = self.query_one("#track-list")
        lv.styles.border = ("solid", accent)
        lv.border_style = accent
        
        # Update Visualizer
        if self.visualizer_enabled:
            viz = self.query_one(Visualizer)
            viz.styles.border = ("solid", accent)
            viz.border_style = accent
            viz.accent_color = accent
        
        # Force refresh
        self.refresh()

    def action_toggle_repeat(self) -> None:
        """Toggle repeat mode."""
        mode = self.player.repeat_toggle()
        self.notify(f"Repeat: {mode}")

    def check_playback_status(self) -> None:
        """Check if track has finished and handle repeat logic."""
        if self.player.audio_play_status == "play":
            # just_playback's active property is False when nothing is playing or finished
            if not self.player.active:
                if self.player.audio_repeat_status == "Single":
                    self.player.play()
                    self.notify("Looping track...")
                else:
                    self.player.audio_play_status = "None"
                    if self.visualizer_enabled:
                        viz = self.query_one(Visualizer)
                        viz.is_playing = False
                    self.notify("Playback finished.")

if __name__ == "__main__":
    app = MusicApp()
    app.run()