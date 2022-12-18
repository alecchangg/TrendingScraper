import requests

BASE = "http://127.0.0.1:5000/"

data = [
        {"name": "Car Thieves vs the Final GlitterBomb 5.0",  "likes": 352000, "views": 4900000 },
        {"name": "Worlds's Hardest Challenge!", "likes": 219000, "views": 3700000},
        {"name": "Barbie | Teaser Trailer", "likes": 93000, "views": 3200000}    
    ]

for i in range(len(data)):
    response = requests.put(BASE + "video/", data[i])
    print(response)

    