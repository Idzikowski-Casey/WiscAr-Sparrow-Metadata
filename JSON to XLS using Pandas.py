import requests
import json
r = requests.get('https://sparrow-data.org/labs/wiscar/api/v1/sample?all=1')
online_metadata = r.json()
with open('online_metadata.json','w') as f:
    json.dump(online_metadata, f)
import pandas as pd
df = pd.read_json('online_metadata.json').to_excel('online_metadata.xls')

dfjson = pd.read_json('online_metadata.json')

