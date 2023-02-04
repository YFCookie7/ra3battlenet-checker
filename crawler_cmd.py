import urllib.request as req
import bs4
import json
import os
from time import sleep

url = "https://api.ra3battle.cn/api/server/status/detail"
fav_map = ["200w苦战无人岛困难版.map", "小岛登陆战.map", 
"小岛登陆战2.0.map", "苦战无人岛路人版.map", "解放战争正式版.map"]
fav_mode = ["塔防", ""]


def getJson():
    request=req.Request(url)
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    # root=bs4.BeautifulSoup(data, "html.parser")
    data = json.loads(data)
    return data

def print_data():
    os.system('cls')
    data = getJson()
    for i in data["games"]:
        if (i['mod'] == "RA3" and i['gamemode'] == "openstaging"):
            x = i['hostname'].split()
            map = os.path.basename(os.path.normpath(i['mapname']))

            if (x[1]==fav_mode[0] or map==fav_map[0] or map==fav_map[1] or map==fav_map[2] or map==fav_map[3] or map==fav_map[4]):
                print(x[1])
                print("Player: ", end='')
                for j in i['players']:
                    print(j['name'] + " ", end='')
                print()
                return
            else:
                # Room name
                
                print("Room: " + x[1] )


                #Player name
                print("Player: ", end='')
                for j in i['players']:
                    print(j['name'] + " ", end='')
                print()

                # Map name
                
                print(map)
                print()
            

                
def main():
    
    print("Opearting")
    while(1):
        print_data()
        sleep(3)
        

if __name__ == "__main__":
    main()
