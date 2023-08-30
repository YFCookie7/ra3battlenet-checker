import asyncio
import urllib.request as req
import json
import os
import tkinter as tk
import threading
import winsound

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
]
sound = True
appear = True


# Create Tkinter GUI
window = tk.Tk()
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

    # Check all game room one by one
    for i in data["games"]:
        roomname = i["hostname"].split()
        roomname = roomname[1].lower()
        map = os.path.basename(os.path.normpath(i["mapname"]))
        # Filiter to RA3 waiting room
        if i["mod"] == "RA3" and i["gamemode"] == "openstaging":
            # roomname=room name, map=map name
            print("Room: " + roomname)
            print("Player: " + str(len(i["players"])))
            print("Map: " + map)
            print("\n")
            # winsound.Beep(1000, 500)

            # Compare room/map name with keyword
            for index in range(len(keyword)):
                if check_word(roomname, keyword[index]) or check_word(
                    map, keyword[index]
                ):
                    found = True
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

    if found and appear:
        window.attributes("-topmost", True)
    else:
        window.attributes("-topmost", False)
    window.configure(bg="red") if found else window.configure(bg="white")
    lbl_result["text"] = result


btn_sound = tk.Button(window, text="Sound: ON", command=btn_sound_onClick)
btn_sound.grid(row=0, column=1)
btn_sound.grid()

btn_appear = tk.Button(window, text="Appear on top: ON", command=btn_appear_onClick)
btn_appear.grid(row=0, column=2)
btn_appear.grid()

lbl_result = tk.Label(window, text="")
lbl_result.grid(row=1, column=1, sticky="NSEW")
lbl_result.config(font=("Courier", 11))


set_interval(refresh_data, 5)
window.mainloop()
