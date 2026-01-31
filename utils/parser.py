import re
from config import BLACKLISTED_PHRASES

def parse_spotify_title(window_title: str):
    """
    Parse Spotify window title: "Artist - Song"
    Returns: (artist, song) or (None, None)
    """
    try:
        if not window_title or not isinstance(window_title, str):
            return None, None
        
        # Skip blacklisted
        if any(phrase in window_title for phrase in BLACKLISTED_PHRASES):
            return None, None
        
        # Spotify format: "Artist - Song"
        if " - " in window_title:
            parts = window_title.split(" - ", 1)  # Split only once
            if len(parts) == 2:
                artist = parts[0].strip()
                song = parts[1].strip()
                
                # Basic validation
                if artist and song:
                    return artist, song
        
        return None, None
    except Exception:
        return None, None  # Always return a tuple

def parse_youtube_title(window_title: str):
    """
    Parse YouTube window title: "Artist - Song - YouTube - Opera"
    Returns: (artist, song) or (None, None)
    """
    try:
        if not window_title or not isinstance(window_title, str):
            return None, None
        
        # Must contain YouTube
        if " - YouTube" not in window_title:
            return None, None
        
        # Skip blacklisted
        if any(phrase in window_title for phrase in BLACKLISTED_PHRASES):
            return None, None
        
        # Remove browser suffix
        title = window_title.replace(" - Opera", "").replace(" - Brave", "").replace(" - Chrome", "")
        
        # Remove YouTube suffix
        if " - YouTube" in title:
            title = title.replace(" - YouTube", "")
            
            # Parse artist - song
            if " - " in title:
                parts = title.split(" - ", 1)
                if len(parts) == 2:
                    artist = parts[0].strip()
                    song = parts[1].strip()
                    
                    # Basic validation
                    if artist and song:
                        return artist, song
        
        return None, None
    except Exception:
        return None, None

def is_valid_music_title(title: str):
    """Check if title looks like music (not a file path, etc)."""
    if not title:
        return False
    
    invalid_patterns = [
        r'\\', r'/', r'\.py$', r'\.exe$', r'\.txt$',
        r'Visual Studio', r'Explorer', r'Discord',
        r'Command Prompt', r'PowerShell', r'Terminal'
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            return False
    
    return True