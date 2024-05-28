import asyncio
import urllib.request as req
import json
import os
import threading
import time

url = "https://api.ra3battle.cn/api/server/status/detail"


def getJson():
    request = req.Request(url)
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    data = json.loads(data)
    return data


prev = getJson()
prev_time = time.time()
curr_time = prev_time
time.sleep(1)

while True:
    curr = getJson()
    if prev != curr:
        curr_time = time.time()

        print(f"time difference {curr_time - prev_time}")
        prev_time = curr_time
        print("Changed")
    else:
        print("Not changed")
    prev = curr
    time.sleep(1)
