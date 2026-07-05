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
    return path.strip().strip('"').strip("'")

def get_target_directory():
    """Prompts the user for a folder path and ensures it is valid."""
    while True:
        user_input = input("Enter the target music folder path: ")
        clean_dir = clean_path(user_input)
        
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

def get_artist_name(filepath):
    """Extract artist name from audio file metadata (tags)."""
    try:
        audio = File(filepath, easy=True)
        if audio and 'artist' in audio:
            return audio['artist'][0].strip()
    except Exception:
        pass
    return None

def get_main_artist_name(artist_string):
    """Extracts the primary artist from a collaboration string."""
    if not artist_string:
        return None
    # Split by &, /, comma, or featuring/feat/ft/vs
    parts = re.split(r'\s*[&,/]\s*|\s*(?:feat\.?|ft\.?|vs\.?|featuring)\b\s*', artist_string, flags=re.IGNORECASE)
    if parts:
        return parts[0].strip()
    return artist_string.strip()

def sort_music_into_folders(target_dir):
    """Option 1: Scans music files and moves them into Album folders (3+ tracks)."""
    print("\n🔄 Scanning and sorting music files by Album (3+ tracks)...")
    album_tracks = defaultdict(list)

    for file in os.listdir(target_dir):
        filepath = os.path.join(target_dir, file)
        if os.path.isfile(filepath):
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTS:
                album = get_album_name(filepath)
                if album:
                    album_tracks[album].append(filepath)

    folders_created = 0
    for album, tracks in album_tracks.items():
        if len(tracks) >= 3:  # Only make a folder if there are 3 or more tracks
            safe_name = safe_folder_name(album)
            album_folder = os.path.join(target_dir, safe_name)

            try:
                os.makedirs(album_folder, exist_ok=True)
            except Exception as e:
                print(f"❌ Error creating folder '{album_folder}': {e}")
                continue

            for track in tracks:
                dest_path = os.path.join(album_folder, os.path.basename(track))
                
                # Prevent overwriting files with the same name
                base, ext = os.path.splitext(track)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(album_folder, f"{os.path.basename(base)}_{counter}{ext}")
                    counter += 1
                    
                try:
                    shutil.move(track, dest_path)
                except Exception as e:
                    print(f"❌ Error moving {track}: {e}")
            
            folders_created += 1

    print(f"✅ Sorting complete! Created {folders_created} album folders.")

def sort_by_artist(target_dir):
    """Option 2: Scans music files and moves them into Artist folders, skipping full albums."""
    print("\n🔄 Scanning and sorting music files by Artist (Skipping albums with 3+ tracks)...")
    
    # Step 1: Scan all loose files and group them by Album to count tracks per album
    album_groups = defaultdict(list)
    
    for file in os.listdir(target_dir):
        filepath = os.path.join(target_dir, file)
        if os.path.isfile(filepath):
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTS:
                album = get_album_name(filepath)
                artist_tag = get_artist_name(filepath)
                main_artist = get_main_artist_name(artist_tag)
                
                track_info = {'filepath': filepath, 'artist': main_artist}
                
                # Group by album. If no album tag, treat it as a unique 1-track album
                if album:
                    album_groups[album].append(track_info)
                else:
                    album_groups[f"__no_album__{filepath}"].append(track_info)

    # Step 2: Filter out tracks that belong to albums with 3 or more tracks
    eligible_tracks = []
    for album, tracks in album_groups.items():
        if len(tracks) < 3:
            eligible_tracks.extend(tracks)

    # Step 3: Group the remaining eligible tracks by Artist
    artist_tracks = defaultdict(list)
    for track_info in eligible_tracks:
        if track_info['artist']:
            artist_tracks[track_info['artist']].append(track_info['filepath'])

    # Step 4: Create folders and move the files
    folders_created = 0
    for artist, tracks in artist_tracks.items():
        if len(tracks) >= 1:  
            safe_name = safe_folder_name(artist)
            artist_folder = os.path.join(target_dir, safe_name)

            try:
                os.makedirs(artist_folder, exist_ok=True)
            except Exception as e:
                print(f"❌ Error creating folder '{artist_folder}': {e}")
                continue

            for track in tracks:
                dest_path = os.path.join(artist_folder, os.path.basename(track))
                base, ext = os.path.splitext(track)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(artist_folder, f"{os.path.basename(base)}_{counter}{ext}")
                    counter += 1
                    
                try:
                    shutil.move(track, dest_path)
                except Exception as e:
                    print(f"❌ Error moving {track}: {e}")
            
            folders_created += 1

    print(f"✅ Sorting complete! Created {folders_created} artist folders.")

def zip_folders_no_compression(target_dir):
    """Option 3: Zips all folders in the directory without compressing the data."""
    print("\n🔄 Zipping folders...")
    zipped_count = 0

    for item in os.listdir(target_dir):
        folder_path = os.path.join(target_dir, item)

        if os.path.isdir(folder_path):
            zip_path = os.path.join(target_dir, f"{item}.zip")

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

def unmerge_all_folders(target_dir):
    """Option 4: Moves all files out of subfolders back to the root and deletes the folders."""
    print("\n🔄 Unmerging all folders...")
    unmerged_count = 0

    for item in os.listdir(target_dir):
        folder_path = os.path.join(target_dir, item)

        if os.path.isdir(folder_path):
            # Move all files to the root directory
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    dest_path = os.path.join(target_dir, file)
                    
                    # Prevent overwriting files with the same name
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                        counter += 1
                        
                    try:
                        shutil.move(file_path, dest_path)
                    except Exception as e:
                        print(f"❌ Error moving {file_path}: {e}")
            
            # Delete the empty folder
            try:
                shutil.rmtree(folder_path)
                unmerged_count += 1
            except Exception as e:
                print(f"❌ Error deleting folder {folder_path}: {e}")

    print(f"✅ Unmerging complete! Restored files from {unmerged_count} folders.")

def main_menu():
    """Displays the menu and handles user choices."""
    target_dir = get_target_directory()
    
    while True:
        print("="*60)
        print("             🎵 MUSIC FOLDER MANAGER 🎵")
        print("="*60)
        print(f"📂 Current Target: {target_dir}")
        print("-" * 60)
        print(" 1. Sort by Album (Makes folders for 3+ tracks)")
        print(" 2. Sort by Artist (Skips albums with 3+ tracks)")
        print(" 3. Zip existing folders (No compression)")
        print(" 4. Unmerge all folders (Move files out & delete folders)")
        print(" 5. Change Target Directory")
        print(" 6. Exit")
        print("-" * 60)
        
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            sort_music_into_folders(target_dir)
        elif choice == '2':
            sort_by_artist(target_dir)
        elif choice == '3':
            zip_folders_no_compression(target_dir)
        elif choice == '4':
            unmerge_all_folders(target_dir)
        elif choice == '5':
            print("\n--- Changing Target Directory ---")
            target_dir = get_target_directory()
        elif choice == '6':
            print("👋 Exiting the program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main_menu()