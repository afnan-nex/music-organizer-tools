# **Music Organizer Tools**

A set of Python utilities to organize music files by album metadata and archive folders into ZIP files without compression.

## **Overview**

This repository contains two Python scripts designed to help manage your music collection:

1.  `album_sorter.py`: Organizes music files in a specified directory by moving tracks with the same album metadata into dedicated album folders.
2.  `folder_zipper.py`: Archives folders into ZIP files without compression for efficient storage or transfer.

## **Features**

*   **Album Sorting**:
    *   Reads metadata from audio files (supports .mp3, .ogg, .mp4, .m4a, .wav, .flac, .aac, .wma).
    *   Groups tracks by album name (requires at least 2 tracks per album to create a folder).
    *   Creates safe folder names compatible with Windows file systems.
*   **Folder Zipping**:
    *   Archives folders into ZIP files using no compression (ZIP_STORED method).
    *   Preserves folder structure within the ZIP files.

## **Requirements**

*   Python 3.6 or higher
*   Required Python packages:
    *   mutagen (for reading audio metadata)
    *   shutil (for file operations)
    *   zipfile (for creating ZIP archives)
    *   os and re (standard Python libraries)

Install the required package using:
```
*   pip install mutagen
```
## **Usage**

### **1. Album Sorter (album_sorter.py)**

This script organizes music files in a specified directory by their album metadata.

#### **Configuration**

*   Set the MUSIC_DIR variable in album_sorter.py to the path of your music directory:  
    MUSIC_DIR = r"`D:\\Music`" # Change to your music directory
*   The script supports the following audio file extensions by default:  
    SUPPORTED_EXTS = {'.mp3', '.ogg', '.mp4', '.m4a', '.wav', '.flac', '.aac', '.wma'}

#### **Running the Script**

1.  Ensure the mutagen package is installed.
2.  Update the MUSIC_DIR path in the script.

*   Run the script:  
```
    python album_sorter.py
```
1.  The script will:
    *   Scan the specified directory (not subfolders).
    *   Group audio files by album metadata.
    *   Create a folder for each album (if it has 2 or more tracks).
    *   Move the tracks into their respective album folders.

#### **Notes**

*   Folder names are sanitized to be Windows-compatible (removes invalid characters like \<, >, :, etc.).
*   If an album has fewer than 2 tracks, it will not be moved (configurable in the script).
*   Errors during folder creation or file moving are logged to the console.

### **2. Folder Zipper (folder_zipper.py)**

This script archives folders in a specified directory into ZIP files without compression.

#### **Configuration**

*   Set the TARGET_DIR variable in folder_zipper.py to the path of the directory containing the folders to zip:  
    TARGET_DIR = r"`D:\\Music`" # Change to your directory

#### **Running the Script**

1.  Update the TARGET_DIR path in the script.

*   Run the script:
```
python folder_zipper.py
```

1.  The script will:
    *   Scan the specified directory for subfolders.
    *   Create a ZIP file for each folder (e.g., AlbumName.zip for a folder named AlbumName).
    *   Store files in the ZIP without compression.

#### **Notes**

*   The ZIP files maintain the folder structure relative to the input folder.
*   Only directories (not individual files) in the target directory are processed.

## **Example Workflow**

1.  Run album_sorter.py to organize your music files into album folders:
    *   Input: A flat directory with music files (e.g., D:\Music\song1.mp3, D:\Music\song2.mp3).
    *   Output: Organized folders (e.g., D:\Music\Album1\song1.mp3, D:\Music\\Album2\song2.mp3).
2.  Run folder_zipper.py to archive the album folders:
    *   Input: Album folders (e.g., D:\Music\Album1, D:\Music\Album2).
    *   Output: ZIP files (e.g., D:\Music\Album1.zip, D:\Music\Album2.zip).

## **License**

This project is licensed under the MIT License. See the [LICENSE](https://github.com/afnan-nex/music-organizer-tools/blob/main/LICENSE) file for details.

## **Contributing**

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, improvements, or new features.

## **Contact**

For questions or feedback, please open an issue on this repository.
