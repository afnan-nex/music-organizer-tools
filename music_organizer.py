import os
import re
import shutil
import zipfile
from collections import defaultdict
from mutagen import File

# ===== CONFIG =====
# Supported audio file extensions
SUPPORTED_EXTS = {'.mp3', '.ogg', '.mp4', '.m4a', '.wav', '.flac', '.aac', '.wma'}
# ==================

def clean_path(path):
    """Removes surrounding quotes and extra spaces from the user's input."""
    # .strip() removes leading/trailing spaces
    # .strip('"') removes double quotes
    # .strip("'") removes single quotes
    return path.strip().strip('"').strip("'")

def get_target_directory():
    """Prompts the user for a folder path and ensures it is valid."""
    while True:
        user_input = input("Enter the target music folder path: ")
        clean_dir = clean_path(user_input)
        
        # Check if the directory actually exists
        if os.path.isdir(clean_dir):
            print(f"✅ Target directory set to: {clean_dir}\n")
            return clean_dir
        else:
            print(f"❌ Error: The folder '{clean_dir}' does not exist or is invalid.")
            print("Please check the path and try again.\n")

def safe_folder_name(name):
    """Make sure folder names are safe for Windows by removing bad characters."""
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', ' ', name)
    return name

def get_album_name(filepath):
    """Extract album name from audio file metadata (tags)."""
    try:
        audio = File(filepath, easy=True)
        if audio and 'album' in audio:
            return audio['album'][0].strip()
    except Exception:
        pass
    return None

def sort_music_into_folders(target_dir):
    """Option 1: Scans music files and moves them into Album folders."""
    print("\n🔄 Scanning and sorting music files...")
    album_tracks = defaultdict(list)

    # 1. Scan only the main directory (no subfolders)
    for file in os.listdir(target_dir):
        filepath = os.path.join(target_dir, file)
        if os.path.isfile(filepath):
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTS:
                album = get_album_name(filepath)
                if album:
                    album_tracks[album].append(filepath)

    # 2. Move tracks with the same album name (2 or more tracks)
    folders_created = 0
    for album, tracks in album_tracks.items():
        if len(tracks) >= 2: 
            safe_name = safe_folder_name(album)
            album_folder = os.path.join(target_dir, safe_name)

            try:
                os.makedirs(album_folder, exist_ok=True)
            except Exception as e:
                print(f"❌ Error creating folder '{album_folder}': {e}")
                continue

            for track in tracks:
                dest_path = os.path.join(album_folder, os.path.basename(track))
                try:
                    shutil.move(track, dest_path)
                except Exception as e:
                    print(f"❌ Error moving {track}: {e}")
            
            folders_created += 1

    print(f"✅ Sorting complete! Created {folders_created} album folders.")

def zip_folders_no_compression(target_dir):
    """Option 2: Zips all folders in the directory without compressing the data."""
    print("\n🔄 Zipping folders...")
    zipped_count = 0

    for item in os.listdir(target_dir):
        folder_path = os.path.join(target_dir, item)

        # Only process directories (folders)
        if os.path.isdir(folder_path):
            zip_path = os.path.join(target_dir, f"{item}.zip")

            # Create ZIP without compression (ZIP_STORED)
            try:
                with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
                    for root, _, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=folder_path)
                            zipf.write(file_path, arcname)
                
                print(f"✅ Zipped {item} → {item}.zip")
                zipped_count += 1
            except Exception as e:
                print(f"❌ Error zipping {item}: {e}")

    print(f"✅ Zipping complete! Created {zipped_count} zip files.")

def main_menu():
    """Displays the menu and handles user choices."""
    # Ask for the directory right when the script starts
    target_dir = get_target_directory()
    
    while True:
        print("="*50)
        print("          🎵 MUSIC FOLDER MANAGER 🎵")
        print("="*50)
        print(f"📂 Current Target: {target_dir}")
        print("-" * 50)
        print(" 1. Sort music files into Album folders")
        print(" 2. Zip existing folders (No compression)")
        print(" 3. Change Target Directory")
        print(" 4. Exit")
        print("-" * 50)
        
        choice = input("Enter your choice (1, 2, 3, or 4): ").strip()

        if choice == '1':
            sort_music_into_folders(target_dir)
            # Automatically loops back
            
        elif choice == '2':
            zip_folders_no_compression(target_dir)
            # Automatically loops back
            
        elif choice == '3':
            print("\n--- Changing Target Directory ---")
            target_dir = get_target_directory()
            
        elif choice == '4':
            print("👋 Exiting the program. Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main_menu()