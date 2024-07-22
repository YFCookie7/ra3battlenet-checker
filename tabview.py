import os
import customtkinter as ctk


class TabView(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.add("Lobby")
        self.add("In-Game")

        self.lobby_frame = ctk.CTkScrollableFrame(self.tab("Lobby"))
        self.lobby_frame.grid(row=0, column=0, sticky="nsew")
        self.lobby_frame.grid_columnconfigure(0, weight=1)
        self.ingame_frame = ctk.CTkScrollableFrame(self.tab("In-Game"))
        self.ingame_frame.grid(row=0, column=0, sticky="nsew")
        self.ingame_frame.grid_columnconfigure(0, weight=1)
        self.tab("Lobby").grid_rowconfigure(0, weight=1)
        self.tab("Lobby").grid_columnconfigure(0, weight=1)
        self.tab("In-Game").grid_rowconfigure(0, weight=1)
        self.tab("In-Game").grid_columnconfigure(0, weight=1)

        self.openstaging_rooms = []
        self.closedplaying_rooms = []
        self.prev_data = None

        self.tafang_keyword = [
            "塔防",
            "tafang",
            "tf",
            "pve",
            "电脑",
            "空战",
            "美国小镇",
        ]

    def update_room(self):
        curr_data = self.parent.data["games"]

        # dont update tabview if data is the same
        if curr_data == self.prev_data:
            return
        self.prev_data = curr_data

        for room in self.openstaging_rooms:
            room.destroy()
        for room in self.closedplaying_rooms:
            room.destroy()
        self.openstaging_rooms = []
        self.closedplaying_rooms = []

        for room in self.parent.data["games"]:
            if room["mod"] == "RA3":
                player_names = ""
                for player in room["players"]:
                    player_names += player["name"] + "    "

                room_name = ("".join(room["hostname"].split()[1:])).strip()
                map_name = os.path.basename(os.path.normpath(room["mapname"]))

                if map_name.startswith("camp_"):
                    continue

                tafang = False
                for keyword in self.tafang_keyword:
                    if keyword.lower() in room_name.lower() or (
                        keyword.lower() in map_name.lower() and keyword.lower() != "tf"
                    ):
                        tafang = True
                        break

                if room["gamemode"] == "openstaging":
                    game_room = GameRoom(
                        self.lobby_frame,
                        room_name,
                        map_name,
                        player_names,
                        tafang,
                    )
                    self.openstaging_rooms.append(game_room)
                elif room["gamemode"] == "closedplaying":
                    game_room = GameRoom(
                        self.ingame_frame,
                        room_name,
                        map_name,
                        player_names,
                        tafang,
                    )
                    self.closedplaying_rooms.append(game_room)
        sorted_openstaging_rooms = sorted(
            self.openstaging_rooms, key=lambda gr: not gr.tafang
        )
        sorted_closedplaying_rooms = sorted(
            self.closedplaying_rooms, key=lambda gr: not gr.tafang
        )
        for i, room in enumerate(sorted_openstaging_rooms):
            room.grid(row=i, column=0, sticky="nsew", padx=(5), pady=5)
        for i, room in enumerate(sorted_closedplaying_rooms):
            room.grid(row=i, column=0, sticky="nsew", padx=(5), pady=5)


class GameRoom(ctk.CTkFrame):
    def __init__(self, parent, room_name, map_name, player_names, tafang):
        super().__init__(parent, fg_color="white")
        self.tafang = tafang

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Room label
        self.lb_room = ctk.CTkLabel(
            self, text=room_name, font=("Arial", 18), width=130, anchor="w"
        )
        self.lb_room.grid(row=0, column=0, padx=15, pady=2, sticky="w")

        # Map label
        self.lb_map = ctk.CTkLabel(self, text=map_name, font=("Arial", 18), anchor="w")
        self.lb_map.grid(row=0, column=1, padx=15, pady=2, sticky="w")

        # Player label
        self.lb_player = ctk.CTkLabel(self, text=player_names, anchor="w")
        self.lb_player.grid(row=1, column=0, columnspan=2, padx=15, pady=2, sticky="w")

        # Banner frame
        self.banner_frame = ctk.CTkFrame(self, width=50, height=10)
        self.banner_frame.grid(row=0, column=2, rowspan=2, sticky="nse")
        if tafang:
            self.banner_frame.configure(fg_color="green")
        else:
            self.banner_frame.configure(fg_color="transparent")
