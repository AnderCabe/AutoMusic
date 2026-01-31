# Main application - Hidden window
import sys
import os
import threading
import time
from datetime import datetime

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Import our modules
from config import LOGS_DIR
from utils.tracker import DownloadTracker
from downloader.ytdl import YouTubeDownloader
from monitor.spotify import SpotifyMonitor
from monitor.youtube import YouTubeMonitor

class AutoMusic:
    def __init__(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] AutoMusic starting...")
        
        # Initialize components
        self.tracker = DownloadTracker()
        self.downloader = YouTubeDownloader()
        
        # Stats
        self.stats = self.tracker.get_stats()
        print(f"[Stats] Previously downloaded: {self.stats['total']} songs")
        
        # Start monitors
        self._start_monitors()
    
    def on_song_detected(self, artist: str, title: str, source: str):
        """Called when a new song is detected."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🎵 Detected: {source.upper()}")
        print(f"   Artist: {artist}")
        print(f"   Title: {title}")
        
        # Check if already downloaded
        if self.tracker.is_downloaded(artist, title, source):
            print("   ⏩ Already downloaded, skipping")
            return
        
        # Download
        print("   ⬇️ Downloading...")
        mp3_path = self.downloader.download_song(artist, title)
        
        if mp3_path:
            # Check if file actually exists
            if os.path.exists(mp3_path):
                # Mark as downloaded
                self.tracker.mark_downloaded(artist, title, source, mp3_path)
                
                # Update stats
                self.stats = self.tracker.get_stats()
                
                print(f"   ✅ Download complete!")
                print(f"      MP3: {os.path.basename(mp3_path)}")
                print(f"   [Total: {self.stats['total']} songs]")
            else:
                print("   ❌ MP3 file not created")
        else:
            print("   ❌ Download failed")
    
    def _start_monitors(self):
        """Start Spotify and YouTube monitors in separate threads."""
        # Create monitor instances
        spotify_monitor = SpotifyMonitor(
            on_detected_callback=self.on_song_detected,
            check_interval=3
        )
        
        youtube_monitor = YouTubeMonitor(
            on_detected_callback=self.on_song_detected,
            check_interval=3
        )
        
        # Start in threads
        self.spotify_thread = threading.Thread(
            target=spotify_monitor.start,
            daemon=True
        )
        
        self.youtube_thread = threading.Thread(
            target=youtube_monitor.start,
            daemon=True
        )
        
        self.spotify_thread.start()
        self.youtube_thread.start()
        
        print("[System] Monitors started")
        print("[System] Running in background...")
        print("[System] Press Ctrl+C in terminal to stop\n")
    
    def run(self):
        """Main loop - keep program alive."""
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[System] Shutting down...")
            sys.exit(0)

if __name__ == "__main__":
    # Create log directory
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Log startup
    with open(os.path.join(LOGS_DIR, "system.log"), 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().isoformat()}] AutoMusic started\n")
    
    # Run application
    app = AutoMusic()
    app.run()