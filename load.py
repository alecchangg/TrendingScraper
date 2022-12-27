import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"

#resets current trending fact table in data warehouse
response = requests.delete(BASE + "warehouse/trending/")

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
    response = requests.get(BASE + "warehouse/channel/", {'name': row['channel']})
    channel_key = response.json()['data'][0][0]

    #adds/updates video info for current row
    response = requests.get(BASE + "warehouse/video/", {'name': row['name']})
    if response.json()['data'] == []:
        jsonData = {}
        jsonData['name'] = row['name']
        jsonData['views'] = row['views']
        jsonData['likes'] = row['likes']
        jsonData['channel'] = channel_key
        jsonData['trending_start_date'] = today_key
        jsonData['trending_end_date'] = today_key
        response = requests.put(BASE + "warehouse/video/", jsonData)
    else:
        video_key = response.json()['data'][0][0]
        response = requests.patch(BASE + "warehouse/video/", {'key': video_key, 'views': row['views'], 'likes': row['likes'], 'trending_end_date': today_key})
    response = requests.get(BASE + "warehouse/video/", {'name': row['name']})
    video_key = response.json()['data'][0][0]

    #updates current trending fact table
    response = requests.put(BASE + "warehouse/trending/", {'video': video_key, 'channel': channel_key, 'date': today_key})

    
    