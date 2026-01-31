# automusic.pyw - Run without console (VERSION SIMPLE QUE FUNCIONA)
import sys
import os

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Import and run main
from main import AutoMusic

if __name__ == "__main__":
    app = AutoMusic()
    app.run()