import os
import json
from datetime import datetime
from config import LOGS_DIR, SONGS_DIR

class DownloadTracker:
    def __init__(self):
        self.tracked_file = os.path.join(LOGS_DIR, "downloaded.json")
        self.downloaded = self._load_tracked()
    
    def _load_tracked(self):
        """Load previously downloaded songs."""
        if os.path.exists(self.tracked_file):
            try:
                with open(self.tracked_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_tracked(self):
        """Save downloaded songs to file."""
        with open(self.tracked_file, 'w', encoding='utf-8') as f:
            json.dump(self.downloaded, f, indent=2)
    
    def is_downloaded(self, artist: str, title: str, source: str):
        """Check if song was already downloaded."""
        key = f"{artist.lower()}_{title.lower()}_{source}"
        is_downloaded = key in self.downloaded
        
        if is_downloaded:
            # Log that we're skipping
            log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            log_entry += f"SKIP {source.upper()}: {artist} - {title}\n"
            
            log_file = os.path.join(LOGS_DIR, "download_history.txt")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        
        return is_downloaded
    
    def mark_downloaded(self, artist: str, title: str, source: str, mp3_path: str = None):
        """Mark song as downloaded."""
        key = f"{artist.lower()}_{title.lower()}_{source}"
        
        self.downloaded[key] = {
            'artist': artist,
            'title': title,
            'source': source,
            'mp3_path': mp3_path,
            'downloaded_at': datetime.now().isoformat()
        }
        
        self._save_tracked()
        self._log_download(artist, title, source)
    
    def _log_download(self, artist: str, title: str, source: str):
        """Log download to text file."""
        log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        log_entry += f"{source.upper()}: {artist} - {title}\n"
        
        log_file = os.path.join(LOGS_DIR, "download_history.txt")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def get_stats(self):
        """Get download statistics."""
        total = len(self.downloaded)
        by_source = {}
        
        for data in self.downloaded.values():
            source = data.get('source', 'unknown')
            by_source[source] = by_source.get(source, 0) + 1
        
        return {
            'total': total,
            'by_source': by_source
        }