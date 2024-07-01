import json
import requests
import time

with open("qwe.json", "r", encoding="utf-8") as f:
    map_dict = json.load(f)

for map_name, map_url in map_dict.items():
    filename = map_name + ".zip"
    download_file = requests.get(map_url)

    if download_file.status_code == 200:
        with open(filename, "wb") as file:
            file.write(download_file.content)
        print(f"File downloaded successfully as {filename}.")
    else:
        print(f"Failed to download: {download_file.status_code}")
    time.sleep(5)
