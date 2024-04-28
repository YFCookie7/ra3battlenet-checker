import asyncio
import urllib.request as req
import json
import os
import threading
from playsound import playsound
import customtkinter as tk

url = "https://api.ra3battle.cn/api/server/status/detail"
keyword = [
    "200w苦战无人岛困难版.map",
    "小岛登陆战.map",
    "战役",
    "tafang",
    "大家好" "小岛登陆战2.0.map",
    "苦战无人岛路人版.map",
    "解放战争正式版.map",
    "防",
    "pve",
    "电脑",
    "人机",
    "tf",
]
sound = True
appear = True


# Create Tkinter GUI
window = tk.CTk()
window.title("RA3 BattleNet")
window.geometry("350x850")
window.iconbitmap("favicon.ico")
window.attributes("-topmost", False)


# Check room name contains keyword
def check_word(string, word):
    return string.find(word) != -1


# Obtain Json data
def getJson():
    request = req.Request(url)
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    data = json.loads(data)
    return data


# Toggle sound when button is pressed
def btn_sound_onClick():
    global sound
    btn_sound["text"] = "Sound: OFF" if sound else "Sound: ON"
    sound = not sound
    return


# Toggle appear when button is pressed
def btn_appear_onClick():
    global appear
    if appear:
        btn_appear["text"] = "Appear: OFF"
        window.attributes("-topmost", False)
    else:
        btn_appear["text"] = "Appear: ON"
    appear = not appear

    return


# Play sound if sound is ON
def play_sound():
    if sound == True:
        pass
        # playsound('beep-01.mp3')


# Looper function
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


# Main loop to update result
def refresh_data():
    os.system("cls")
    data = getJson()
    result = ""
    found = False
    target = tb_wait_player.get("0.0", "end")
    target_still_playing = None

    # Check all game room one by one
    for i in data["games"]:
        roomname = i["hostname"].split()
        if len(roomname) >= 2:
            roomname = roomname[1].lower()
        else:
            roomname = ""
        map = os.path.basename(os.path.normpath(i["mapname"]))
        # Filiter to RA3 waiting room
        if i["mod"] == "RA3" and i["gamemode"] == "openstaging":
            # roomname=room name, map=map name
            # print("Room: " + roomname)
            # print("Player: " + str(len(i["players"])))
            # print("Map: " + map)
            # print("\n")
            # winsound.Beep(1000, 500)

            # Compare room/map name with keyword
            for index in range(len(keyword)):
                if check_word(roomname, keyword[index]) or check_word(
                    map, keyword[index]
                ):
                    found = True
                    print(roomname)
                    # print("Found")
                    # playsound('beep-01.mp3')

            # Room name
            # print("Room: " + x[1] )
            if not check_word(map, "camp_"):
                result = result + "Room: " + roomname + "\n"

                # Player name
                # print("Player: ", end='')
                for j in i["players"]:
                    # print(j['name'] + " ", end='')
                    result = result + j["name"] + "\n"
                # print()

                # Map name
                # print(map)
                result = result + map + "\n\n\n"

            # print()

        if target.strip() != "":
            if i["mod"] == "RA3" and i["gamemode"] == "closedplaying":
                if i["players"][0]["name"] == target.strip():
                    target_still_playing = True
    if target.strip() != "" and not target_still_playing:
        print(len(target.strip()))
        print(target_still_playing)
        playsound("beep.mp3")

    if found and appear:
        window.attributes("-topmost", True)
    else:
        window.attributes("-topmost", False)
    # window.configure(bg="red") if found else window.configure(bg="red")
    window.configure(fg_color="red") if found else window.configure(fg_color="white")
    lbl_result.configure(text=result)


btn_sound = tk.CTkButton(window, text="Sound: ON", command=btn_sound_onClick)
btn_sound.grid(row=0, column=1)
btn_sound.grid()

btn_appear = tk.CTkButton(window, text="Appear on top: ON", command=btn_appear_onClick)
btn_appear.grid(row=0, column=2)
btn_appear.grid()

lbl_result = tk.CTkLabel(window, text="")
lbl_result.grid(row=1, column=1, sticky="NSEW")
lbl_result.configure(font=("Courier", 14), fg_color="white")

tb_wait_player = tk.CTkTextbox(window, height=10)
tb_wait_player.grid(row=2, column=1, sticky="NSEW")


set_interval(refresh_data, 5)
window.mainloop()
