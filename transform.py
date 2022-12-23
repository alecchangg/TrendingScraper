import requests
import pandas as pd

BASE = "http://127.0.0.1:5000/"

#get request API for data in StagingAreaIN
response = requests.get(BASE + "staging/in/")
rep = response.json()
data = rep['data']

#converts returned JSON data into pandas dataframe
pd.set_option('display.max_columns', None)
df = pd.DataFrame(data, columns = ['rank', 'name', 'views', 'likes', 'channel', 'subscribers'])
conversions = {'K': 1000, 'M': 1000000, 'B': 1000000000}

#iterates through each row of the dataframe
for index, row in df.iterrows():
    #reformat views column
    views = row['views']
    views = views[:-6]
    multiplier = views[-1]
    views = views[:-1]
    row['views'] = int(float(views) * conversions[multiplier])
    
    #reformat likes column
    likes = row['likes']
    multiplier = likes[-1]
    likes = likes[:-1]
    row['likes'] = int(float(likes) * conversions[multiplier])

    #reformat subscriber column
    subscribers = row['subscribers']
    subscribers = subscribers[:-12]
    multiplier = subscribers[-1]
    subscribers = subscribers[:-1]
    row['subscribers'] = int(float(subscribers) * conversions[multiplier])

    #reformat rank column
    row['rank'] = int(row['rank'])

    #converts dataframe row into JSON format
    jsonData = {}
    jsonData['name'] = row['name']
    jsonData['views'] = row['views']
    jsonData['likes'] = row['likes']
    jsonData['channel'] = row['channel']
    jsonData['subscribers'] = row['subscribers']

    #put request to API to load into StagingAreaOUT 
    response = requests.put(BASE + "staging/out/", jsonData)

print(df)   