import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"

today = date.today().strftime("%Y-%m-%d")
response = requests.get(BASE + "warehouse/date/", {'date': today})
print(response.json())