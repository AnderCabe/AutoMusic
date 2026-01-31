import time
import psutil
import pygetwindow as gw
import win32gui
import win32process
from utils.parser import parse_spotify_title

class SpotifyMonitor:
    def __init__(self, on_detected_callback, check_interval=3):
        self.callback = on_detected_callback
        self.check_interval = check_interval
        self.last_title = ""
        self.running = False
        self.spotify_pids = []
    
    def find_spotify_processes(self):
        """Find all Spotify process IDs."""
        spotify_pids = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if 'spotify' in proc.info['name'].lower():
                    spotify_pids.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return spotify_pids
    
    def get_spotify_window_titles(self):
        """Get ALL window titles from Spotify processes."""
        titles = []
        self.spotify_pids = self.find_spotify_processes()
        
        if not self.spotify_pids:
            return titles
        
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid in self.spotify_pids:
                    title = win32gui.GetWindowText(hwnd)
                    if title and title.strip():
                        hwnds.append(title)
            return True
        
        win32gui.EnumWindows(callback, titles)
        return titles
    
    def get_current_song_title(self):
        """Extract song title from Spotify windows."""
        titles = self.get_spotify_window_titles()
        
        if not titles:
            return None
        
        # Debug: Show all Spotify window titles
        if len(titles) > 1:
            print(f"[Spotify Debug] {len(titles)} windows: {titles}")
        
        # Look for the music window (usually the one with " - " pattern)
        for title in titles:
            title = title.strip()
            
            # Skip empty or very short
            if not title or len(title) < 5:
                continue
            
            # Skip obvious non-music windows
            if any(phrase in title for phrase in [
                'Advertisement', 'Spotify Premium', 'Upgrade', 
                'Paused', 'Loading', 'Search'
            ]):
                continue
            
            # Look for "Artist - Song" pattern
            if " - " in title:
                # Additional check: not a browser/editor
                if not any(x in title.lower() for x in [
                    'youtube', 'opera', 'chrome', 'explorer'
                ]):
                    return title
        
        # If no clear pattern, return the first non-empty title
        for title in titles:
            if title and title.strip():
                return title.strip()
        
        return None
    
    def start(self):
        """Start monitoring."""
        self.running = True
        print("[Spotify Monitor] Started (process-based detection)")
        
        while self.running:
            try:
                title = self.get_current_song_title()
                
                if title and title != self.last_title:
                    print(f"[Spotify] Window title: '{title}'")
                    
                    artist, song = parse_spotify_title(title)
                    if artist and song:
                        print(f"[Spotify] Playing: {artist} - {song}")
                        self.callback(artist, song, "spotify")
                    else:
                        print(f"[Spotify] Could not parse title")
                    
                    self.last_title = title
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[Spotify Monitor] Error: {e}")
                time.sleep(self.check_interval)
    
    def stop(self):
        self.running = False