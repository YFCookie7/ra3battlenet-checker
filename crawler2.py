import urllib.request as req
import bs4
import json
import os
import tkinter

url = "https://api.ra3battle.cn/api/server/status/detail"
fav_map = ["诞生于黄土高原的中华民族（抢地图）.map", "200w苦战无人岛困难版.map", "小岛登陆战.map", 
"小岛登陆战2.0.map", "苦战无人岛路人版.map", "解放战争正式版.map"]
fav_mode = ["塔防", ""]

window = tkinter.Tk()
window.title('RA3 Battlenet')
window.geometry('550x300')
window.iconbitmap('favicon.ico')


def getJson():
    request=req.Request(url)
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    # root=bs4.BeautifulSoup(data, "html.parser")
    data = json.loads(data)
    return data

def print_data():
    data = getJson()
    for i in data["games"]:
        if (i['mod'] == "RA3" and i['gamemode'] == "openstaging"):
            # Room name
            x = i['hostname'].split()
            print("Room: " + x[1] )

            #Player name
            print("Player: ", end='')
            for j in i['players']:
                print(j['name'] + " ", end='')
            print()

            # Map name
            map = os.path.basename(os.path.normpath(i['mapname']))
            print(map)
            print()

def main():
    print_data()
    
    # window["background"] = "#C9C9C9"
    window.mainloop()
        

if __name__ == "__main__":
    main()
