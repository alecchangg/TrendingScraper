import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"

video_key = 1
channel_key = 1
today_key = 5

response = requests.delete(BASE + "warehouse/trending/")
print(response)
