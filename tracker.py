import os
import customtkinter as ctk


class Tracker(ctk.CTkScrollableFrame):

    track_target = None

    def __init__(self, parent):
        super().__init__(
            parent,
            label_text="Tracker",
            label_font=ctk.CTkFont(size=16),
            corner_radius=10,
        )
        self.parent = parent
        self.tracker_window = None

        self.lb_status = ctk.CTkLabel(self, text="No target", font=ctk.CTkFont(size=16))
        self.lb_status.grid(row=0, column=0, pady=(5, 5))

        self.lb_content = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.lb_content.grid(row=1, column=0, pady=(5, 5))

        self.columnconfigure((0), weight=1)

    def track_player(self, player_name):
        if player_name == "":
            Tracker.track_target = None
        else:
            if self.tracker_window is None or not self.tracker_window.winfo_exists():
                self.tracker_window = TrackerWindow(self, player_name)
            else:
                self.tracker_window.update_content(player_name)

            self.tracker_window.deiconify()

    def update_status(self):
        # Track player
        if Tracker.track_target:
            isOnline = False
            for player in self.parent.data["players"]:
                if player["name"] == Tracker.track_target:
                    isOnline = True
                    break
            if isOnline:
                isPlaying = False
                for room in self.parent.data["games"]:
                    for player in room["players"]:
                        if player["name"] == Tracker.track_target:
                            if room["gamemode"] == "closedplaying":
                                self.lb_status.configure(
                                    text=f"{Tracker.track_target}: In game",
                                    text_color="blue",
                                )
                            else:
                                self.lb_status.configure(
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
                            self.lb_content.configure(text=content)
                            isPlaying = True
                            break
                if not isPlaying:
                    self.lb_status.configure(
                        text=f"{Tracker.track_target}: Idle", text_color="green"
                    )
                    self.lb_content.configure(text="")
            else:
                self.lb_status.configure(
                    text=f"{Tracker.track_target}: Offline", text_color="red"
                )
                self.lb_content.configure(text="")
        else:
            self.lb_status.configure(text="No target")


class TrackerWindow(ctk.CTkToplevel):
    def __init__(self, parent, player_name, *args, **kwargs):
        super().__init__(
            parent,
            *args,
            **kwargs,
        )
        self.parent = parent
        self.geometry("400x300")
        self.title("Track Player")

        players = self.parent.parent.data["players"]
        matching_names = []
        for player in players:
            if player_name in player["name"]:
                matching_names.append(player["name"])

        self.combobox = ctk.CTkOptionMenu(self, values=matching_names, width=300)
        self.combobox.grid(row=0, column=0, padx=(0, 0))

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0), weight=1)

        self.button = ctk.CTkButton(
            self, text="Track", command=self.track_player, width=120
        )
        self.button.grid(row=1, column=0, padx=(0, 0))

        self.update_content(player_name)

    def update_content(self, player_name):
        players = self.parent.parent.data["players"]
        matching_names = []
        for player in players:
            if player_name in player["name"]:
                matching_names.append(player["name"])
        self.combobox.configure(values=matching_names)

    def track_player(self):
        Tracker.track_target = self.combobox.get()
        self.parent.parent.fetch_data()
        self.destroy()
