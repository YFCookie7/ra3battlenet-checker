import customtkinter
from PIL import Image
import time
import os
import urllib.request as req
import json


class App(customtkinter.CTk):
    server_url = "https://api.ra3battle.cn/api/server/status/detail"

    def __init__(self):
        super().__init__()

        # Configure window
        self.geometry("640x480")
        self.title("RA3 BattleNet")
        self.iconbitmap("favicon.ico")
        self.attributes("-topmost", False)
        customtkinter.set_appearance_mode(
            "System"
        )  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme(
            "green"
        )  # Themes: "blue" (standard), "green", "dark-blue"

        my_image = customtkinter.CTkImage(
            light_image=Image.open("icon.png"),
            dark_image=Image.open("icon.png"),
            size=(50, 50),
        )

        button = customtkinter.CTkButton(
            self, text="", image=my_image, width=50, height=50
        )
        button.grid(row=0, column=1)
        button.grid()

        # Data related
        # self.refresh_data()

    def refresh_data(self):
        os.system("cls")
        request = req.Request(App.server_url)
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        data = json.loads(data)
        print(data)
        self.after(5000, self.refresh_data)


app = App()
app.mainloop()
