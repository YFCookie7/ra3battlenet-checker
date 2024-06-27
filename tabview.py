import customtkinter as ctk


class tabview(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.add("Lobby")
        self.add("In-Game")
