import customtkinter
from PIL import Image
import time
import os
import urllib.request as req
import json
import webbrowser


class App(customtkinter.CTk):
    server_url = "https://api.ra3battle.cn/api/server/status/detail"
    data = []

    def __init__(self):
        super().__init__()

        # Configure window
        self.geometry("960x680")
        self.title("RA3 BattleNet")
        self.iconbitmap("favicon.ico")
        self.attributes("-topmost", False)
        customtkinter.set_appearance_mode(
            "System"
        )  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme(
            "blue"
        )  # Themes: "blue" (standard), "green", "dark-blue"

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # Sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=190, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="ns")

        self.sidebar_frame.grid_rowconfigure((2), weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="RA3 BattleNet",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 10))

        self.player_count_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="RA3 BattleNet",
            font=customtkinter.CTkFont(size=18),
        )
        self.player_count_label.grid(row=1, column=0, padx=20, pady=(40, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 20))

        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")

        # Main frame
        self.tabview = customtkinter.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.tabview.add("Lobby")
        self.tabview.add("In-Game")
        self.tabview.tab("Lobby").rowconfigure(0, weight=1)
        self.tabview.tab("Lobby").columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(self.tabview.tab("Lobby"))
        self.textbox.grid(row=0, column=0, sticky="nsew")

        self.textbox.insert(
            "0.0",
            "qwe",
        )

        # Player frame
        self.player_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.player_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Track frame
        self.track_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.track_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # Search frame
        self.search_frame = customtkinter.CTkFrame(
            self, corner_radius=10, height=50, fg_color="transparent"
        )
        self.search_frame.grid(
            row=2, column=1, columnspan=2, sticky="nsew", padx=10, pady=10
        )

        self.search_frame.columnconfigure(0, weight=1)
        self.entry = customtkinter.CTkEntry(
            self.search_frame, placeholder_text="CTkEntry"
        )
        self.entry.grid(row=2, column=0, padx=(0, 0), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(
            master=self.search_frame,
            text="Track",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
        )
        self.main_button_1.grid(row=2, column=1, padx=(15, 5), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(
            master=self.search_frame,
            text="Add/Remove Friend",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
        )
        self.main_button_2.grid(row=2, column=2, padx=(5, 5), sticky="nsew")

        self.main_button_3 = customtkinter.CTkButton(
            master=self.search_frame,
            text="Profile",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.redirect_to_profile,
        )
        self.main_button_3.grid(row=2, column=3, padx=(5, 5), sticky="nsew")

        # my_image = customtkinter.CTkImage(
        #     light_image=Image.open("icon.png"),
        #     dark_image=Image.open("icon.png"),
        #     size=(50, 50),
        # )

        # button = customtkinter.CTkButton(
        #     self, text="", image=my_image, width=50, height=50
        # )
        # button.grid(row=0, column=1)
        # button.grid()

        self.refresh_data()

    def refresh_data(self):
        global data
        os.system("cls")
        request = req.Request(App.server_url)
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        data = json.loads(data)

        ra3_player_count = 0
        for i in data["games"]:
            if i["mod"] == "RA3":
                ra3_player_count += len(i["players"])
        self.player_count_label.configure(
            text=f"{len(data['players'])}/{ra3_player_count}"
        )
        self.after(5000, self.refresh_data)

    def redirect_to_profile(self):
        global data
        for player in data["players"]:
            print(player["name"])
            if player["name"] == self.entry.get():
                url = f"https://ra3battle.net/persona/{player['id']}"
                webbrowser.open(url)
                break

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


app = App()
app.mainloop()
