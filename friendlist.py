import customtkinter as ctk


class FriendList(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            label_text="Friend List",
            label_font=ctk.CTkFont(size=16),
            corner_radius=10,
        )

        # label = ctk.CTkLabel(self, text="Frame 1")
        # label.pack(pady=10, padx=10)

        # button = ctk.CTkButton(self, text="Frame 1")
        # button.pack(pady=10, padx=10)
