import requests
import time
import json

url = "https://ra3.z31.xyz/v1/maps/?format=json"

map_dict = {}

while url != None:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        url = data["next"]
        print("Next URL:", url)

        for result in data["results"]:
            if "PVE" in result["tags"]:
                print(result["name"], result["zip_file"])
                map_dict[result["name"]] = result["zip_file"]

    else:
        print(f"Failed to retrieve {url}: {response.status_code}")
        url = None

    time.sleep(1)

with open("map_dict.json", "w", encoding="utf-8") as f:
    json.dump(map_dict, f, ensure_ascii=False, indent=4)
