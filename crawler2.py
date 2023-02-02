import urllib.request as req
import bs4
import json

url = "https://api.ra3battle.cn/api/server/status/detail"

request=req.Request(url)

with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
# print(data)

root=bs4.BeautifulSoup(data, "html.parser")
y = json.loads(data)

print(y["players"]['id'])
