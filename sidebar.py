import customtkinter as ctk


class SideBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=190, corner_radius=0, fg_color="#CA2B2F")
        self.parent = parent
        self.grid_rowconfigure(1, weight=1)

        self.lb_logo = ctk.CTkLabel(
            self,
            text="RA3 BattleNet",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
        )
        self.lb_logo.grid(row=0, column=0, padx=20, pady=(40, 10), sticky="n")

        self.lb_player_count = ctk.CTkLabel(
            self,
            text="##/##",
            font=ctk.CTkFont(size=18),
            text_color="white",
        )
        self.lb_player_count.grid(row=1, column=0, padx=20, pady=(40, 10), sticky="n")

        self.lb_theme = ctk.CTkLabel(
            self,
            text="Theme:",
            text_color="white",
        )
        self.lb_theme.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="s")

        self.menu_theme = ctk.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=lambda theme: ctk.set_appearance_mode(theme),
        )
        self.menu_theme.set("Light")
        self.menu_theme.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="s")

        self.lb_scaling = ctk.CTkLabel(
            self,
            text="UI Scaling:",
            text_color="white",
        )
        self.lb_scaling.grid(row=4, column=0, padx=20, pady=(20, 0), sticky="s")

        self.menu_scaling = ctk.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=lambda scaling: ctk.set_widget_scaling(
                (int(scaling.replace("%", "")) / 100)
            ),
        )
        self.menu_scaling.set("100%")
        self.menu_scaling.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="s")

    def update_player_count(self):
        ra3_player_count = 0
        for i in self.parent.data["games"]:
            if i["mod"] == "RA3":
                ra3_player_count += len(i["players"])
        self.lb_player_count.configure(
            text=f"{len(self.parent.data['players'])}/{ra3_player_count}"
        )
