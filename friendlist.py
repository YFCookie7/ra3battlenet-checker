import customtkinter as ctk
from tracker import Tracker


class FriendList(ctk.CTkScrollableFrame):
    friend_list = []

    def __init__(self, parent):
        super().__init__(
            parent,
            label_text="Friend List",
            label_font=ctk.CTkFont(size=16),
            corner_radius=10,
            fg_color="transparent",
        )
        self.tracker = Tracker(parent)
        self.parent = parent
        self.friend_radio = []
        self.prev_data = None

        # Init friend list
        self.refresh_friend_list()

        self.columnconfigure(0, weight=1)

        self.update_friend_list()

        # idle: full green, offline: disabled, staging: full yellow, in-game: full blue

    def update_friend_list(self):
        curr_data = self.parent.data
        # dont update if data is the same

        if curr_data == self.prev_data:
            return
        self.prev_data = curr_data

        if curr_data == []:
            return

        for radio in self.friend_radio:
            radio.destroy()

        idle_friend = []
        staging_friend = []
        in_game_friend = []
        offline_friend = []

        for friend in FriendList.friend_list:
            isOnline = False
            for player in curr_data["players"]:
                if friend == player["name"]:
                    isOnline = True
                    break
            if not isOnline:
                offline_friend.append(friend)
            else:
                isPlaying = False
                for room in curr_data["games"]:
                    for player in room["players"]:
                        if player["name"] == friend:
                            if room["gamemode"] == "openstaging":
                                staging_friend.append(friend)
                            else:
                                in_game_friend.append(friend)
                            isPlaying = True
                if not isPlaying:
                    idle_friend.append(friend)

        i = 0
        for friend in idle_friend:
            radio = FriendRadio(self, friend, "idle", self.tracker)
            radio.grid(row=i, column=0, padx=5, pady=5)
            self.friend_radio.append(radio)
            i += 1
        for friend in staging_friend:
            radio = FriendRadio(self, friend, "staging", self.tracker)
            radio.grid(row=i, column=0, padx=5, pady=5)
            self.friend_radio.append(radio)
            i += 1
        for friend in in_game_friend:
            radio = FriendRadio(self, friend, "in-game", self.tracker)
            radio.grid(row=i, column=0, padx=5, pady=5)
            self.friend_radio.append(radio)
            i += 1
        for friend in offline_friend:
            radio = FriendRadio(self, friend, "offline", self.tracker)
            radio.grid(row=i, column=0, padx=5, pady=5)
            self.friend_radio.append(radio)
            i += 1

    def refresh_friend_list(self):
        try:
            with open("./friendlist.txt", "r", encoding="utf-8") as file:
                FriendList.friend_list = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            with open("./friendlist.txt", "w", encoding="utf-8") as file:
                pass


class FriendRadio(ctk.CTkRadioButton):

    def __init__(self, parent, friend_name, friend_status, tracker):
        super().__init__(
            parent,
            text=friend_name,
            value="true",
            font=ctk.CTkFont(size=14),
            command=lambda: tracker.track_player(friend_name),
        )
        self.tracker = tracker
        self.configure(border_width_unchecked=5)
        if friend_status == "idle":
            self.configure(border_color="#1eb300")
        elif friend_status == "staging":
            self.configure(border_color="#a0c400")
        elif friend_status == "in-game":
            self.configure(border_color="#09a0ba")
        elif friend_status == "offline":
            self.configure(state="disabled")
