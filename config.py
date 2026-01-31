import os
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
SONGS_DIR = r"C:\Users\user\Music\Songs"  # Final MP3s here
TEMP_DIR = os.path.join(tempfile.gettempdir(), "AutoMusic")  # Temporary downloads
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Detection intervals (seconds)
SPOTIFY_CHECK_INTERVAL = 3
YOUTUBE_CHECK_INTERVAL = 3

# Download settings
DOWNLOAD_QUALITY = "192"  # kbps: 128, 192, 256, 320
MAX_FILE_SIZE_MB = 25     # Approx 15 minutes of audio

# File naming
SONG_FORMAT = "{artist} - {title}.mp3"

# Logging
LOG_FILE = os.path.join(LOGS_DIR, "automusic.log")

# Blacklist (skip these)
BLACKLISTED_PHRASES = [
    "Advertisement",
    "Commercial",
    "Paused",
    "Loading",
    "Spotify Premium",
]

# Ensure directories exist
for dir_path in [SONGS_DIR, TEMP_DIR, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)