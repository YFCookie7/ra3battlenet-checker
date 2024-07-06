import os
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
        self.geometry("960x680")
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
        # os.system("cls")
        request = req.Request(self.server_url)
        with req.urlopen(request) as response:
            App.data = response.read().decode("utf-8")
        App.data = json.loads(App.data)

        # Overall player count
        ra3_player_count = 0
        for i in App.data["games"]:
            if i["mod"] == "RA3":
                ra3_player_count += len(i["players"])
        self.sidebar_frame.lb_player_count.configure(
            text=f"{len(App.data['players'])}/{ra3_player_count}"
        )

        # Track player
        if Tracker.track_target:
            isOnline = False
            for player in App.data["players"]:
                if player["name"] == Tracker.track_target:
                    isOnline = True
                    break
            if isOnline:
                isPlaying = False
                for room in App.data["games"]:
                    for player in room["players"]:
                        if player["name"] == Tracker.track_target:
                            if room["gamemode"] == "closedplaying":
                                self.tracker.lb_status.configure(
                                    text=f"{Tracker.track_target}: In game",
                                    text_color="blue",
                                )
                            else:
                                self.tracker.lb_status.configure(
                                    text=f"{Tracker.track_target}: Waiting to start",
                                    text_color="yellow",
                                )

                            content = " ".join(room["hostname"].split()[1:]) + "\n\n"
                            for player in room["players"]:
                                content += player["name"] + "\n"
                            content += "\n"
                            content += os.path.basename(
                                os.path.normpath(room["mapname"])
                            )
                            self.tracker.lb_content.configure(text=content)
                            isPlaying = True
                            break
                if not isPlaying:
                    self.tracker.lb_status.configure(
                        text=f"{Tracker.track_target}: Idle", text_color="green"
                    )
                    self.tracker.lb_content.configure(text="")
            else:
                self.tracker.lb_status.configure(
                    text=f"{self.track_target}: Offline", text_color="red"
                )
                self.tracker.lb_content.configure(text=content)
        else:
            self.tracker.lb_status.configure(text="No target")

        # Update game room
        self.tabview.update_room()

        self.after(5000, self.fetch_data)


if __name__ == "__main__":
    app = App()
    app.mainloop()
