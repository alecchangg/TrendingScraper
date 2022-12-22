import requests
import pandas as pd

pd.set_option('display.max_columns', None)

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "video/")
rep = response.json()

data = rep['data']

df = pd.DataFrame(data, columns = ['rank', 'name', 'views', 'likes', 'channel', 'subscribers'])
conversions = {'K': 1000, 'M': 1000000, 'B': 1000000000}

for index, row in df.iterrows():
    views = row['views']
    views = views[:-6]
    multiplier = views[-1]
    views = views[:-1]
    row['views'] = int(float(views) * conversions[multiplier])
    

    likes = row['likes']
    multiplier = likes[-1]
    likes = likes[:-1]
    row['likes'] = int(float(likes) * conversions[multiplier])


    subscribers = row['subscribers']
    subscribers = subscribers[:-12]
    multiplier = subscribers[-1]
    subscribers = subscribers[:-1]
    row['subscribers'] = int(float(subscribers) * conversions[multiplier])


    row['rank'] = int(row['rank'])


print(df)







    