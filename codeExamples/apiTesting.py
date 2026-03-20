import requests
keyTemp = "a74f2804-4ad8-4a1a-bbfd-2b317b5964a4"

url = "https://api.hypixel.net/v2/resources/skyblock/items"

data = requests.get(url)

info = data.json()
for item in info["items"]:
    if item["material"] == "EMERALD":
        print(item["name"], item["id"])

