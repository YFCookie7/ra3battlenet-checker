import threading
import webbrowser
import zipfile
import customtkinter as ctk
import os
from friendlist import FriendList
from tracker import Tracker
import requests
import json


class SearchBar(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=10,
            height=50,
            fg_color="transparent",
        )
        self.tracker = Tracker(parent)
        self.parent = parent
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
            command=lambda: self.tracker.track_player(self.search_entry.get()),
        )
        self.btn_track.grid(row=0, column=1, padx=(10, 5), sticky="nsew")

        self.btn_profile = ctk.CTkButton(
            self,
            text="Profile",
            fg_color="transparent",
            width=120,
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=lambda: ProfileWindow(self, self.search_entry.get()),
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
            command=lambda: FriendWindow(self, self.search_entry.get()),
        )
        self.btn_add.grid(row=0, column=4, padx=(5, 5), sticky="nsew")

    def download_map(self, target_map):
        # Return if the search entry is empty
        if not target_map:
            return

        url = "https://ra3.z31.xyz/v1/maps/?ordering=-id&s=20&search="

        response = requests.get(url + target_map)

        if response.status_code == 200:
            map_query_result = response.json()
            # open download window
            if self.download_window is None or not self.download_window.winfo_exists():
                self.download_window = DLWindow(self, map_query_result)
            else:
                self.download_window.update_content(map_query_result)

            self.download_window.deiconify()


class DLWindow(ctk.CTkToplevel):
    def __init__(self, parent, map_query_result, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geometry("400x300")
        self.map_query_result = map_query_result
        self.pending_dict = {}
        self.local_map_path = r"C:\Users\mikel\AppData\Roaming\Red Alert 3\Maps"

        self.map_url = "https://ra3.z31.xyz/?s="

        self.combobox = ctk.CTkOptionMenu(
            self, values=list(self.pending_dict.keys()), width=300
        )
        self.combobox.grid(row=0, column=0, columnspan=2, padx=(0, 0))

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0), weight=1)

        self.button = ctk.CTkButton(
            self, text="Download", command=self.start_download, width=120
        )
        self.button.grid(row=1, column=0, padx=(0, 0))

        self.button2 = ctk.CTkButton(
            self,
            text="Browse",
            command=lambda: self.browse_map(self.combobox.get()),
            width=120,
        )
        self.button2.grid(row=1, column=1, padx=(0, 0))

        self.label = ctk.CTkLabel(self, text="")
        self.label.grid(row=2, column=0, padx=(0, 0))
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        self.update_content(map_query_result)

    def download_map(self):
        filename = self.combobox.get()
        self.label.configure(text=f"Downloading {filename}...")
        url = self.pending_dict.get(self.combobox.get(), None)

        if url:

            for dir in os.listdir(self.local_map_path):
                if filename in dir:
                    self.label.configure(text=f"{filename} already exists")
                    return

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

    def browse_map(self, map_name):
        url = "https://ra3.z31.xyz/v1/maps/?ordering=-id&s=20&search="
        response = requests.get(url + map_name)

        if response.status_code == 200:
            map_query_result = response.json()
            for result in map_query_result["results"]:
                if result["name"] == map_name or result["chinese_name"] == map_name:
                    webbrowser.open("https://ra3.z31.xyz/" + str(result["id"]))
                    return

    def update_content(self, map_query_result):
        self.map_query_result = map_query_result
        for maps in self.map_query_result["results"]:
            self.pending_dict[maps["name"]] = maps["zip_file"]
        if self.map_query_result:
            self.combobox.configure(values=list(self.pending_dict.keys()))

    def start_download(self):
        threading.Thread(target=self.download_map).start()


class FriendWindow(ctk.CTkToplevel):
    def __init__(self, parent, keyword, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geometry("400x300")
        self.title("Add/Remove friend")
        self.parent = parent
        self.friend_list = []

        try:
            with open("./friendlist.txt", "r", encoding="utf-8") as file:
                self.friend_list = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            with open("./friendlist.txt", "w", encoding="utf-8") as file:
                pass

        matching_name = []
        for player in self.parent.parent.data["players"]:
            if keyword in player["name"]:
                matching_name.append(player["name"])

        self.combobox = ctk.CTkOptionMenu(self, values=matching_name, width=200)
        self.combobox.grid(row=0, column=0, columnspan=2, padx=(0, 0))

        self.btn_add = ctk.CTkButton(
            self, text="Add", command=self.add_friend, width=50
        )
        self.btn_add.grid(row=1, column=0, padx=10)

        self.btn_remove = ctk.CTkButton(
            self, text="Remove", command=self.remove_friend, width=50
        )
        self.btn_remove.grid(row=1, column=1, padx=10)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

    def add_friend(self):
        if self.combobox.get() not in self.friend_list:
            self.friend_list.append(self.combobox.get())
            try:
                with open("./friendlist.txt", "a", encoding="utf-8") as file:
                    file.write(self.combobox.get() + "\n")
            except FileNotFoundError:
                with open("./friendlist.txt", "w", encoding="utf-8") as file:
                    pass
        FriendList.refresh_friend_list(self)
        self.destroy()

    def remove_friend(self):
        if self.combobox.get() in self.friend_list:
            self.friend_list.remove(self.combobox.get())
            with open("./friendlist.txt", "w", encoding="utf-8") as file:
                for friend in self.friend_list:
                    file.write(friend + "\n")
        FriendList.refresh_friend_list(self)
        self.destroy()


class ProfileWindow(ctk.CTkToplevel):
    def __init__(self, parent, query_name, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geometry("400x300")
        self.query_name = query_name
        self.player_list = parent.parent.data["players"]
        self.pending_dict = {}

        self.combobox = ctk.CTkOptionMenu(
            self, values=list(self.pending_dict.keys()), width=300
        )
        self.combobox.grid(row=0, column=0, padx=(0, 0))

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0), weight=1)

        self.button = ctk.CTkButton(
            self, text="Open profile", command=self.redirect_to_profile, width=120
        )
        self.button.grid(row=1, column=0, padx=(0, 0))

        self.label = ctk.CTkLabel(self, text="")
        self.label.grid(row=2, column=0, padx=(0, 0))

        self.update_content()

    def update_content(self):
        for player in self.player_list:
            if self.query_name.lower() in player["name"].lower():
                self.pending_dict[player["name"]] = player["id"]
        self.combobox.configure(values=list(self.pending_dict.keys()))

    def redirect_to_profile(self):
        player_id = self.pending_dict.get(self.combobox.get(), None)
        if player_id:
            url = f"https://ra3battle.net/persona/{player_id}"
            webbrowser.open(url)
