import urllib.request as req
import bs4
import json
import os

url = "https://api.ra3battle.cn/api/server/status/detail"


def getJson():
    request=req.Request(url)
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    # root=bs4.BeautifulSoup(data, "html.parser")
    data = json.loads(data)
    return data



def main():
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
            print()


    

if __name__ == "__main__":
    main()
