import os
import zipfile

# ===== CONFIG =====
TARGET_DIR = r"D:\test"  # Change this to your directory
# ==================

def zip_folders_no_compression(directory):
    for item in os.listdir(directory):
        folder_path = os.path.join(directory, item)

        # Only process directories
        if os.path.isdir(folder_path):
            zip_path = os.path.join(directory, f"{item}.zip")

            # Create ZIP without compression
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=folder_path)
                        zipf.write(file_path, arcname)

            print(f"✅ Zipped {item} → {item}.zip (no compression)")

if __name__ == "__main__":
    zip_folders_no_compression(TARGET_DIR)
