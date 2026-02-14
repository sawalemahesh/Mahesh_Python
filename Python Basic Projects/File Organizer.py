import os
import shutil
from tkinter import Tk, filedialog

class FileOrganizer:

    def __init__(self):
        self.categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
            "Videos": [".mp4", ".mkv", ".avi"],
            "Audio": [".mp3", ".wav"],
            "Code": [".py", ".java", ".js", ".html", ".css"]
        }

    def choose_folder(self):
        root = Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select Folder to Organize")
        return folder_path

    def organize(self):
        folder_path = self.choose_folder()

        if not folder_path:
            print("❌ No folder selected")
            return

        print("📁 Organizing:", folder_path)

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                _, ext = os.path.splitext(item)
                ext = ext.lower()

                moved = False
                for category, extensions in self.categories.items():
                    if ext in extensions:
                        self.move_file(folder_path, item, category)
                        moved = True
                        break

                if not moved:
                    self.move_file(folder_path, item, "Others")

        print("✅ File organization completed successfully!")

    def move_file(self, base_path, filename, folder_name):
        destination = os.path.join(base_path, folder_name)

        if not os.path.exists(destination):
            os.mkdir(destination)

        shutil.move(
            os.path.join(base_path, filename),
            os.path.join(destination, filename)
        )


if __name__ == "__main__":
    FileOrganizer().organize()
