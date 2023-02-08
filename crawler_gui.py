import urllib.request as req
import json
import os
from time import sleep
import tkinter as tk
import threading

url = "https://api.ra3battle.cn/api/server/status/detail"
keyword = ["200w苦战无人岛困难版.map", "小岛登陆战.map", 
"小岛登陆战2.0.map", "苦战无人岛路人版.map", "解放战争正式版.map", "塔防", "pve", "电脑", "人机"]

# Create Tkinter GUI
window = tk.Tk()
window.title("RA3 BattleNet")
window.geometry("400x550")

# Check room name contains keyword
def check_word(string, word):
    return string.find(word) != -1

# Obtain Json data
def getJson():
    request=req.Request(url)
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    data = json.loads(data)
    return data

# Main loop to update result
def print_data():
    while(True):
        found = False
        os.system('cls')
        data = getJson()
        result = ""
        window.configure(bg='#F0F0F0')
        
        # Check all game room one by one
        for i in data["games"]:
            # Filiter to RA3 waiting room
            if (i['mod'] == "RA3" and i['gamemode'] == "openstaging"):
                # x[1]=room name, map=map name
                x = i['hostname'].split()
                x[1]=x[1].lower()
                map = os.path.basename(os.path.normpath(i['mapname']))

                # Compare room/map name with keyword
                for index in range(len(keyword)):
                    if (check_word(x[1], keyword[index]) or check_word(map, keyword[index])):
                        #Set background to red if found
                        window.configure(bg='red')
                    
                # Room name
                print("Room: " + x[1] )
                result = result + "Room: " + x[1] + "\n"
                
                #Player name
                print("Player: ", end='')
                for j in i['players']:
                    print(j['name'] + " ", end='')
                    result = result + j['name'] + "\n"
                print()

                # Map name
                print(map)
                result = result + map + "\n\n\n"
                print()


        lbl_result["text"] = result
        sleep(3)
         

# 建立一個子執行緒
t = threading.Thread(target = print_data)
# 執行該子執行緒
t.start()

lbl_result = tk.Label(window, text="")
lbl_result.grid(row=3, column=0, columnspan=2)

window.mainloop()
