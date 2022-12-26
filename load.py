import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"

#adds/updates the date dimension for today's date
today = date.today().strftime("%Y-%m-%d")
response = requests.get(BASE + "warehouse/date/", {'date': today})
if response.json()['data'] == []:
    response = requests.put(BASE + "warehouse/date/", {'date': today})
today_key = response.json()['data'][0][0]

#get request to staging area for new data and converts JSON serializable object to pandas dataframes
response = requests.get(BASE + "staging/out/")
data = response.json()["data"]
pd.set_option("display.max_columns", None)
df = pd.DataFrame(data, columns = ['rank', 'name', 'views', 'likes', 'channel', 'subscribers'])
channel_df = pd.DataFrame().assign(name = df['channel'], subscribers = df['subscribers'])


#iterate through each row and adds/updates dimension and fact tables
for index, row in df.iterrows():

    #adds/updates channel info for current row
    response = requests.get(BASE + "warehouse/channel/", {'name': row['channel']})
    if response.json()['data'] == []:
        jsonData = {}
        jsonData['name'] = row['channel']
        jsonData['subscribers'] = row['subscribers']
        response = requests.put(BASE + "warehouse/channel/", jsonData)
    else:
        channel_key = response.json()['data'][0][0]
        subscribers = row['subscribers']
        response = requests.patch(BASE + "warehouse/channel/", {'key': channel_key, 'subscribers': subscribers})