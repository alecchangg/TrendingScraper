import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"

today = date.today().strftime("%Y-%m-%d")
#response = requests.put(BASE + "warehouse/date/", {'date': today})
#print(response)
response = requests.get(BASE + "warehouse/date/", {'date': today})
today_key = response.json()['data'][0][0]
channel_key = 46

response = requests.patch(BASE + "warehouse/video/", {'key': 1, 'views': 1, 'likes': 1, 'trending_end_date': 5})
print(response)
