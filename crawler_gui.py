import urllib.request as req
import json
import os
from time import sleep
import tkinter as tk
import threading
from playsound import playsound

url = "https://api.ra3battle.cn/api/server/status/detail"
keyword = ["200w苦战无人岛困难版.map", "小岛登陆战.map", 
"小岛登陆战2.0.map", "苦战无人岛路人版.map", "解放战争正式版.map", "塔防", "pve", "电脑", "人机"]
sound=True

# Create Tkinter GUI
window = tk.Tk()
window.title("RA3 BattleNet")
window.geometry("350x850")
window.iconbitmap("favicon.ico")

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

def btn_sound_onClick():
    global sound
    if (sound==True):
        print(str(sound))
        btn_sound['text'] = 'Sound: OFF'
        sound=False
        return
    elif (sound==False):
        print(str(sound))
        btn_sound['text'] = 'Sound: ON'
        sound=True
        return

def play_sound():
    if (sound==True):
        playsound('beep-01.mp3')

    

# Main loop to update result
def print_data():
    color = 0
    while(True):
        # os.system('cls')
        data = getJson()
        result = ""
        print("Refreshed")
        
        # Check all game room one by one
        for i in data["games"]:
            # Filiter to RA3 waiting room
            if (i['mod'] == "RA3" and i['gamemode'] == "openstaging"):

                # x[1]=room name, map=map name
                x = i['hostname'].split()
                x[1]=x[1].lower()
                map = os.path.basename(os.path.normpath(i['mapname']))

                # Compare room/map name with keyword
                found=False
                for index in range(len(keyword)):
                    if (check_word(x[1], keyword[index]) or check_word(map, keyword[index])):
                        found=True
                        # print("Found")
                        # playsound('beep-01.mp3')
                if (found==True):
                    color+=1

                    if(color%2==1):
                        window.configure(bg='red')
                    elif(color%2==0):
                        window.configure(bg='green')
                    
                    thread = threading.Thread(target=play_sound)
                    thread.start()
                    thread.join()

                else:
                    window.configure(bg='#F0F0F0')
                    
                
                    
                # Room name
                # print("Room: " + x[1] )
                result = result + "Room: " + x[1] + "\n"
                
                #Player name
                # print("Player: ", end='')
                for j in i['players']:
                    # print(j['name'] + " ", end='')
                    result = result + j['name'] + "\n"
                # print()

                # Map name
                # print(map)
                result = result + map + "\n\n\n"
                # print()

        lbl_result["text"] = result
        sleep(3)
        


btn_sound = tk.Button(window, text='Sound: ON', command=btn_sound_onClick)
btn_sound.grid(row=0,column=1)
btn_sound.grid()


lbl_result = tk.Label(window, text="")
lbl_result.grid(row=1, column=1, sticky="NSEW")
lbl_result.config(font=("Courier", 11))



# 建立一個子執行緒
t = threading.Thread(target = print_data)
# 執行該子執行緒
t.start()





window.mainloop()
