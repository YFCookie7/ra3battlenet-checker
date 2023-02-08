import urllib.request as req
import json
import os
from time import sleep
import tkinter as tk
import threading

url = "https://api.ra3battle.cn/api/server/status/detail"
keyword = ["200w苦战无人岛困难版.map", "小岛登陆战.map", 
"小岛登陆战2.0.map", "苦战无人岛路人版.map", "解放战争正式版.map", "塔防", "pve", "电脑"]

window = tk.Tk()
window.title("RA3 BattleNet")
window.geometry("500x250")

def check_word(string, word):
    return string.find(word) != -1

def getJson():
    request=req.Request(url)
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    # root=bs4.BeautifulSoup(data, "html.parser")
    data = json.loads(data)
    return data

def print_data():
    while(True):
        found = False
        os.system('cls')
        data = getJson()
        result = ""
        window.configure(bg='#F0F0F0')
        
        

        # Check all existing room one by one

        for i in data["games"]:
            # Filiter waiting room
            if (i['mod'] == "RA3" and i['gamemode'] == "openstaging"):
                x = i['hostname'].split()
                map = os.path.basename(os.path.normpath(i['mapname']))

                for index in range(len(keyword)):
                    x[1]=x[1].lower()
                    if (check_word(x[1], keyword[index])):
                        window.configure(bg='red')

                # if (x[1]==keyword[0] or map==keyword[0] or map==keyword[1] or map==keyword[2] or map==keyword[3] or map==keyword[4] or map==keyword[5]):
                #     found=True
                #     window.configure(bg='SystemButtonFace')
                    
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

        # if (found==True):
        #     for i in range(1, 50):
        #         print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF") 

        lbl_result["text"] = result
        sleep(3)

            

                
# def main():

# 建立一個子執行緒
t = threading.Thread(target = print_data)

# 執行該子執行緒
t.start()

print("Opearting")

lbl_result = tk.Label(window, text="")
lbl_result.grid(row=3, column=0, columnspan=2)


# while(True):
#     print_data()
#     sleep(3)
window.mainloop()
        

# if __name__ == "__main__":
#     main()
