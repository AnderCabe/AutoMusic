import time
import pygetwindow as gw
from utils.parser import parse_youtube_title

class YouTubeMonitor:
    def __init__(self, on_detected_callback, check_interval=3):
        self.callback = on_detected_callback
        self.check_interval = check_interval
        self.last_title = ""
        self.running = False
    
    def get_youtube_window(self):
        """Find YouTube window by ' - YouTube' pattern."""
        try:
            all_windows = gw.getAllWindows()
            
            for window in all_windows:
                if not window.title or not window.visible:
                    continue
                
                title = window.title.strip()
                
                # Look for YouTube pattern
                if " - YouTube" in title:
                    return title
            
            return None
        except Exception as e:
            print(f"[YouTube Monitor] Error: {e}")
            return None
    
    def start(self):
        """Start monitoring."""
        self.running = True
        print("[YouTube Monitor] Started")
        
        while self.running:
            try:
                title = self.get_youtube_window()
                
                if title and title != self.last_title:
                    print(f"[YouTube] Detected: {title}")
                    
                    artist, song = parse_youtube_title(title)
                    if artist and song:
                        print(f"[YouTube] Parsed: {artist} - {song}")
                        self.callback(artist, song, "youtube")
                    
                    self.last_title = title
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[YouTube Monitor] Loop error: {e}")
                time.sleep(self.check_interval)
    
    def stop(self):
        self.running = False