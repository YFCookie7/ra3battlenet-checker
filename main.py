import customtkinter as ctk
import json
import urllib.request as req
from sidebar import SideBar
from tabview import TabView
from friendlist import FriendList
from tracker import Tracker
from searchbar import SearchBar


class App(ctk.CTk):

    data = []

    def __init__(self):
        super().__init__()
        self.server_url = "https://api.ra3battle.cn/api/server/status/detail"

        # Configure window
        self.title("RA3 BattleNet")
        self.iconbitmap("favicon.ico")
        self.geometry("1000x700")
        self.attributes("-topmost", False)
        ctk.set_appearance_mode("System")  # Mode: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme(
            "blue"
        )  # Theme: "blue" (standard), "green", "dark-blue"

        # Layout
        self.sidebar_frame = SideBar(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="ns")
        self.grid_rowconfigure(0, weight=1)

        self.tabview = TabView(self)
        self.tabview.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.grid_columnconfigure(1, weight=1)

        self.friend = FriendList(self)
        self.friend.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)

        self.tracker = Tracker(self)
        self.tracker.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)

        self.searchbar = SearchBar(self)
        self.searchbar.grid(
            row=2, column=1, columnspan=2, sticky="nsew", padx=10, pady=10
        )

        self.fetch_data()

    def fetch_data(self):
        # Fetch data
        request = req.Request(self.server_url)
        with req.urlopen(request) as response:
            App.data = response.read().decode("utf-8")
        App.data = json.loads(App.data)

        # Update player count
        self.sidebar_frame.update_player_count()

        # Update friend list
        self.friend.update_friend_list()

        # Update tracking target status
        self.tracker.update_status()

        # Update game room
        self.tabview.update_room()

        self.after(5000, self.fetch_data)


if __name__ == "__main__":
    app = App()
    app.mainloop()
