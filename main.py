import http
import customtkinter as ctk
import json
import urllib.request as req
from sidebar import SideBar
from tabview import TabView
from friendlist import FriendList
from tracker import Tracker
from searchbar import SearchBar
from PIL import Image, ImageTk


class App(ctk.CTk):

    data = []

    def __init__(self):
        super().__init__()
        self.server_url = "https://api.ra3battle.cn/api/server/status/detail"

        # Configure window
        self.title("RA3 BattleNet")
        self.iconbitmap("favicon.ico")
        self.geometry("1000x700")
        self.attributes("-topmost", False)
        ctk.set_appearance_mode("System")  # Mode: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme(
            "blue"
        )  # Theme: "blue" (standard), "green", "dark-blue"

        # Background image
        background_image = Image.open("background.png")
        photo = ImageTk.PhotoImage(background_image)
        canvas = ctk.CTkCanvas(self, highlightthickness=0)
        canvas.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo

        # Layout
        self.sidebar_frame = SideBar(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="ns")
        self.grid_rowconfigure(0, weight=1)

        self.tabview = TabView(self)
        self.tabview.grid(
            row=0, column=1, rowspan=2, sticky="nsew", padx=(15, 10), pady=(15, 5)
        )
        self.grid_columnconfigure(1, weight=1)

        self.friend = FriendList(self)
        self.friend.grid(row=0, column=2, sticky="nsew", padx=(5, 15), pady=(15, 7))
        self.grid_rowconfigure(0, weight=1)

        self.tracker = Tracker(self)
        self.tracker.grid(row=1, column=2, sticky="nsew", padx=(5, 15), pady=(8, 5))
        self.grid_rowconfigure(1, weight=1)

        self.searchbar = SearchBar(self)
        self.searchbar.grid(
            row=2, column=1, columnspan=2, sticky="nsew", padx=15, pady=(5, 10)
        )

        self.fetch_data()

    def fetch_data(self):
        try:
            # Fetch data
            request = req.Request(self.server_url)
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")
            App.data = json.loads(data)

            # Update player count
            self.sidebar_frame.update_player_count()

            # Update friend list
            self.friend.update_friend_list()

            # Update tracking target status
            self.tracker.update_status()

            # Update game room
            self.tabview.update_room()

        except http.client.IncompleteRead as e:
            print("Incomplete read occurred:", e)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            self.after(5000, self.fetch_data)


if __name__ == "__main__":
    app = App()
    app.mainloop()
