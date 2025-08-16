import os
import re
import shutil
from collections import defaultdict
from mutagen import File

# ===== CONFIG =====
MUSIC_DIR = r"D:\test"  # Change to your main music directory
SUPPORTED_EXTS = {'.mp3', '.ogg', '.mp4', '.m4a', '.wav', '.flac', '.aac', '.wma'}
# ==================

def safe_folder_name(name):
    """Make sure folder names are safe for Windows."""
    name = name.strip()  # remove leading/trailing spaces
    name = re.sub(r'[<>:"/\\|?*]', '_', name)  # replace invalid characters
    name = re.sub(r'\s+', ' ', name)  # normalize spaces
    return name

def get_album_name(filepath):
    """Extract album name from audio file metadata."""
    try:
        audio = File(filepath, easy=True)
        if audio and 'album' in audio:
            return audio['album'][0].strip()
    except Exception:
        pass
    return None

def main():
    album_tracks = defaultdict(list)

    # 1. Scan only the main directory (no subfolders)
    for file in os.listdir(MUSIC_DIR):
        filepath = os.path.join(MUSIC_DIR, file)
        if os.path.isfile(filepath):
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTS:
                album = get_album_name(filepath)
                if album:
                    album_tracks[album].append(filepath)

    # 2. Move tracks with same album name (≥ 2 tracks)
    for album, tracks in album_tracks.items():
        if len(tracks) >= 2:
            safe_name = safe_folder_name(album)
            album_folder = os.path.join(MUSIC_DIR, safe_name)

            try:
                os.makedirs(album_folder, exist_ok=True)
            except Exception as e:
                print(f"Error creating folder '{album_folder}': {e}")
                continue

            for track in tracks:
                dest_path = os.path.join(album_folder, os.path.basename(track))
                try:
                    shutil.move(track, dest_path)
                except Exception as e:
                    print(f"Error moving {track}: {e}")

    print("✅ Sorting complete.")

if __name__ == "__main__":
    main()
