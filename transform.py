import requests

BASE = "http://127.0.0.1:5000/"

var = {"video_key": 1}

response = requests.get(BASE + "video/")
rep = response.json()

data = rep['data']

for x in data:
    print()
    print(x)
    print()
    