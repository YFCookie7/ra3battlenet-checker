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

        self.map_url = "https://ra3.z31.xyz/?s="
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
            command=lambda: webbrowser.open(self.map_url + self.search_entry.get()),
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

        with open("./map_downloader/map_dict.json", "r", encoding="utf-8") as f:
            map_dict = json.load(f)

        # Fetch available map links
        for map_name, map_url in map_dict.items():
            if target_map in map_name:
                pending_dict[map_name] = map_url

        # Filter already downloaded maps
        for map_name in list(pending_dict.keys()):
            map_path = os.path.join(self.local_map_path, map_name)
            if os.path.isdir(map_path):
                del pending_dict[map_name]

        download_result = True

        if len(pending_dict) <= 40 and len(pending_dict) != 0:
            for map_name, map_url in pending_dict.items():
                filename = map_name + ".zip"
                download_file = requests.get(map_url)

                if download_file.status_code == 200:
                    with open(filename, "wb") as file:
                        file.write(download_file.content)

                    extract_path = os.path.join(self.local_map_path, map_name)
                    os.makedirs(extract_path, exist_ok=True)

                    with zipfile.ZipFile(filename, "r") as zip_ref:
                        zip_ref.extractall(extract_path)

                    os.remove(filename)
                else:
                    download_result = False
        else:
            download_result = False

        self.open_dlwindow(download_result, pending_dict)

    def toogle_tracking(self):
        self.tracker.toogle_tracking()

    def open_dlwindow(self, download_result, pending_dict):
        if self.download_window is None or not self.download_window.winfo_exists():
            self.download_window = DLWindow(self, download_result, pending_dict)
        else:
            self.download_window.update_content(download_result, pending_dict)

        self.download_window.deiconify()


class DLWindow(ctk.CTkToplevel):
    def __init__(self, parent, download_result, pending_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geometry("400x300")
        self.label = ctk.CTkLabel(self, text="")
        self.label.pack(padx=20, pady=20)
        self.update_content(download_result, pending_dict)

    def update_content(self, download_result, pending_dict):
        content = ""
        if download_result:
            content = "Download successful\n\n"
            for map_name in pending_dict:
                content += f"{map_name}\n"
        else:
            content = "Download failed\n\n"
            if len(pending_dict) == 0:
                content += "No maps found\n\n"
            elif len(pending_dict) > 2:
                content += f"Too many maps found({len(pending_dict)})\n\n"
                for i, map_name in enumerate(pending_dict):
                    if i >= 10:
                        break
                    content += f"{map_name}\n"

        self.label.configure(text=content)
