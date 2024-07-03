import threading
import webbrowser
import zipfile
import customtkinter as ctk
import os
from tracker import Tracker
import requests
import json


class SearchBar(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, corner_radius=10, height=50, fg_color="transparent")
        self.parent = parent
        self.tracker = Tracker(parent)
        self.download_window = None
        self.local_map_path = r"C:\Users\mikel\AppData\Roaming\Red Alert 3\Maps"

        self.search_entry = ctk.CTkEntry(self, placeholder_text="")
        self.search_entry.grid(row=0, column=0, padx=(0, 0), sticky="nsew")
        self.columnconfigure(0, weight=1)

        self.btn_track = ctk.CTkButton(
            self,
            text="Track",
            fg_color="transparent",
            width=120,
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.toogle_tracking,
        )
        self.btn_track.grid(row=0, column=1, padx=(10, 5), sticky="nsew")

        self.btn_profile = ctk.CTkButton(
            self,
            text="Profile",
            fg_color="transparent",
            width=120,
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.redirect_to_profile,
        )
        self.btn_profile.grid(row=0, column=2, padx=(5, 5), sticky="nsew")

        self.btn_map = ctk.CTkButton(
            self,
            text="Map",
            fg_color="transparent",
            width=120,
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=lambda: self.download_map(self.search_entry.get()),
        )
        self.btn_map.grid(row=0, column=3, padx=(5, 5), sticky="nsew")

        self.btn_add = ctk.CTkButton(
            self,
            text="Add/Remove",
            fg_color="transparent",
            width=120,
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            # command=lambda: webbrowser.open(self.map_url + self.search_entry.get()),
        )
        self.btn_add.grid(row=0, column=4, padx=(5, 5), sticky="nsew")

    def redirect_to_profile(self):
        found = False
        target_player = self.search_entry.get()
        for player in self.parent.data["players"]:
            if player["name"] == target_player:
                found = True
                url = f"https://ra3battle.net/persona/{player['id']}"
                webbrowser.open(url)
                break
        if not found:
            self.search_entry.delete(0, "end")

    def download_map(self, target_map):
        # Return if the search entry is empty
        if not target_map:
            return

        pending_dict = {}

        # Fetch available map links
        with open("./map_downloader/map_dict.json", "r", encoding="utf-8") as f:
            map_dict = json.load(f)

        for map_name, map_url in map_dict.items():
            if target_map in map_name:
                pending_dict[map_name] = map_url

        # Filter already downloaded maps
        for map_name in list(pending_dict.keys()):
            map_path = os.path.join(self.local_map_path, map_name)
            if os.path.isdir(map_path):
                del pending_dict[map_name]

        # open download window
        if self.download_window is None or not self.download_window.winfo_exists():
            self.download_window = DLWindow(self, pending_dict)
        else:
            self.download_window.update_content(pending_dict)

        self.download_window.deiconify()

    def toogle_tracking(self):
        self.tracker.toogle_tracking()


class DLWindow(ctk.CTkToplevel):
    def __init__(self, parent, pending_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geometry("400x300")
        self.pending_dict = pending_dict

        self.map_url = "https://ra3.z31.xyz/?s="
        self.local_map_path = r"C:\Users\mikel\AppData\Roaming\Red Alert 3\Maps"

        self.combobox = ctk.CTkOptionMenu(
            self, values=list(pending_dict.keys()), width=300
        )
        self.combobox.grid(row=0, column=0, padx=(0, 0))

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0), weight=1)

        self.button = ctk.CTkButton(
            self, text="Download", command=self.start_download, width=120
        )
        self.button.grid(row=1, column=0, padx=(0, 0))

        self.label = ctk.CTkLabel(self, text="")
        self.label.grid(row=2, column=0, padx=(0, 0))

        self.update_content(pending_dict)

    def download_map(self):
        filename = self.combobox.get() + ".zip"
        self.label.configure(text=f"Downloading {filename}...")
        url = self.pending_dict.get(self.combobox.get(), None)

        if url:
            download_file = requests.get(url)

            if download_file.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(download_file.content)

                extract_path = os.path.join(self.local_map_path, filename)
                os.makedirs(extract_path, exist_ok=True)

                with zipfile.ZipFile(filename, "r") as zip_ref:
                    zip_ref.extractall(extract_path)

                os.remove(filename)
                self.label.configure(text=f"Downloaded {filename}")
            else:
                self.label.configure(text=f"Failed to download {filename}")

        else:
            self.label.configure(text=f"Failed to find {filename} link")

    def update_content(self, pending_dict):
        self.pending_dict = pending_dict
        if pending_dict:
            self.combobox.configure(values=list(pending_dict.keys()))

    def start_download(self):
        threading.Thread(target=self.download_map).start()
