import urllib.request as req
import bs4
import json

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
    for i in data["players"]:
        print(i['name'])

    

if __name__ == "__main__":
    main()
