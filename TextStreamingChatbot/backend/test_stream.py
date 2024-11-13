import json

import requests

url = "http://127.0.0.1:8000/stream_chat"
message = "write a essay of 200 words on elephant."
data = {"content": message}

headers = {"Content-type": "application/json"}

with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk)