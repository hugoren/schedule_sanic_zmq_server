import requests
import json


def file_sync():
    token = 'Schedule0350c8c75ddcd9fafdaA9738df4c9346bec48dc9c4915'
    url = 'http://127.0.0.1:10011/api/v1/schedule/file_sync/'
    data = {"target": "127.0.0.1", "file_name": "tests.py"}
    r = requests.get(url, data=json.dumps(data),
                 headers={'Content-Type': 'application/json', 'token': token}).json()
    print(r)

file_sync()




