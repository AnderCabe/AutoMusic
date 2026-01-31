import os
import yt_dlp
import shutil
from config import SONGS_DIR, TEMP_DIR, MAX_FILE_SIZE_MB

class YouTubeDownloader:
    def __init__(self):
        self.max_file_size_mb = 25
        
        # Asegurar que existen las carpetas
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(SONGS_DIR, exist_ok=True)
    
    def download_song(self, artist: str, title: str):
        """Descarga en TEMP, convierte a MP3, mueve a SONGS, limpia TEMP."""
        safe_artist = self._safe_filename(artist)
        safe_title = self._safe_filename(title)
        
        mp3_filename = f"{safe_artist} - {safe_title}.mp3"
        mp3_path = os.path.join(SONGS_DIR, mp3_filename)
        
        # Si ya existe en SONGS_DIR
        if os.path.exists(mp3_path):
            print(f"[Downloader] ✓ Ya existe")
            return mp3_path
        
        print(f"[Downloader] Buscando: {artist} - {title}")
        
        query = f"{artist} {title} audio"
        
        # TEMPLATE para archivo temporal en TEMP folder
        temp_template = os.path.join(TEMP_DIR, f"{safe_artist} - {safe_title}.%(ext)s")
        
        # Configuración para TEMP folder
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_template,  # Guardar en TEMP
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'keepvideo': False,      # No guardar video
            'quiet': True,
            'no_warnings': True,
            'no_color': True,
            'noplaylist': True,
            'ignoreerrors': False,
            'nooverwrites': False,
            'noprogress': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Primero check rápido de duración
                try:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)
                    if info and 'entries' in info and info['entries']:
                        video = info['entries'][0]
                        duration = video.get('duration', 0)
                        
                        if duration > 900:  # 15 min
                            print(f"[Downloader] ✗ Muy largo")
                            return None
                except:
                    pass  # Si falla el check, seguir igual
                
                # Descargar en TEMP folder
                print(f"[Downloader] Descargando...")
                ydl.download([f"ytsearch:{query}"])
            
            # Buscar el archivo MP3 en TEMP folder
            temp_mp3 = None
            for file in os.listdir(TEMP_DIR):
                filepath = os.path.join(TEMP_DIR, file)
                
                # Buscar por nombre y extensión .mp3
                if (safe_artist in file and safe_title in file and 
                    file.lower().endswith('.mp3')):
                    temp_mp3 = filepath
                    break
            
            # Si no encuentra .mp3, buscar el archivo más reciente en TEMP
            if not temp_mp3:
                files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) 
                        if os.path.isfile(os.path.join(TEMP_DIR, f))]
                if files:
                    temp_mp3 = max(files, key=os.path.getctime)
            
            if temp_mp3 and os.path.exists(temp_mp3):
                # Check tamaño
                size_mb = os.path.getsize(temp_mp3) / 1024 / 1024
                
                if size_mb > self.max_file_size_mb:
                    print(f"[Downloader] ✗ Muy grande ({size_mb:.1f} MB)")
                    os.remove(temp_mp3)
                    return None
                
                # Mover de TEMP a SONGS folder
                shutil.move(temp_mp3, mp3_path)
                print(f"[Downloader] ✓ Descargado ({size_mb:.1f} MB)")
                
                # Limpiar TEMP folder (por si hay otros archivos)
                self._clean_temp_folder()
                
                return mp3_path
        
        except Exception as e:
            # Error limpio
            error_msg = str(e)
            if "already exists" in error_msg.lower():
                print(f"[Downloader] ✓ Ya existe")
                return mp3_path
            elif "Unsupported URL" in error_msg:
                print(f"[Downloader] ✗ URL no soportada")
            else:
                print(f"[Downloader] ✗ Error")
            
            # Limpiar TEMP si hay error
            self._clean_temp_folder()
        
        return None
    
    def _clean_temp_folder(self):
        """Limpia todos los archivos en TEMP folder."""
        try:
            for file in os.listdir(TEMP_DIR):
                filepath = os.path.join(TEMP_DIR, file)
                try:
                    os.remove(filepath)
                except:
                    pass
        except:
            pass
    
    def _safe_filename(self, text: str) -> str:
        """Nombre seguro para Windows."""
        invalid = '<>:"/\\|?*'
        for char in invalid:
            text = text.replace(char, '_')
        text = text.replace('|', '_').replace(':', '_')
        return text.strip()[:100]