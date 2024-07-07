import customtkinter as ctk


class FriendList(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            label_text="Friend List",
            label_font=ctk.CTkFont(size=16),
            corner_radius=10,
        )
        self.friend_list = []

        # Init friend list
        try:
            with open("./friendlist.txt", "r", encoding="utf-8") as file:
                self.friend_list = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            with open("./friendlist.txt", "w", encoding="utf-8") as file:
                pass

        self.columnconfigure(0, weight=1)

        self.radio_var_player_status = ctk.StringVar(value="idle")

        self.radiobutton_1 = ctk.CTkRadioButton(
            self,
            text="CTkRadioButton 1",
            variable=self.radio_var_player_status,
            value="idle",
        )
        self.radiobutton_2 = ctk.CTkRadioButton(
            self,
            text="CTkRadioButton 2",
            variable=self.radio_var_player_status,
            value="option2",
        )
        self.radiobutton_3 = ctk.CTkRadioButton(
            self, text="CTkRadioButton 3", value=0, state="disabled"
        )
        self.radiobutton_1.grid(row=0, column=0, padx=10, pady=10)
        self.radiobutton_2.grid(row=1, column=0, padx=10, pady=10)
        self.radiobutton_3.grid(row=2, column=0, padx=10, pady=10)
