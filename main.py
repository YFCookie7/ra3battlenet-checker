import customtkinter as ctk
from sidebar import sidebar
from tabview import tabview
from friend import friend
from tracker import tracker
from searchbar import searchbar


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

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
        self.sidebar_frame = sidebar(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="ns")
        self.grid_rowconfigure(0, weight=1)

        self.tabview = tabview(self)
        self.tabview.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.grid_columnconfigure(1, weight=1)

        self.friend = friend(self)
        self.friend.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)

        self.tracker = tracker(self)
        self.tracker.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)

        self.searchbar = searchbar(self)
        self.searchbar.grid(
            row=2, column=1, columnspan=2, sticky="nsew", padx=10, pady=10
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
