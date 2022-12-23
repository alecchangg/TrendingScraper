import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"

today = date.today()

response = requests.get(BASE + "video/staging/out/")
data = response.json()["data"]

pd.set_option("display.max_columns", None)
df = pd.DataFrame(data, columns = ['rank', 'name', 'views', 'likes', 'channel', 'subscribers'])

channel_df = pd.DataFrame().assign(name = df['channel'], subscribers = df['subscribers'])




