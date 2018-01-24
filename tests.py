import requests
import json


def file_sync(target, file_name):
    token = 'Schedule0350c8c75ddcd9fafdaA9738df4c9346bec48dc9c4915'
    url = 'http://127.0.0.1:10011/api/v1/schedule/file_sync/'
    data = {"target": target, "file_name": file_name}
    r = requests.get(url, data=json.dumps(data),
                 headers={'Content-Type': 'application/json', 'token': token}).json()
    print(r)



def remote_command():
    target = '127.0.0.1'
    command = 'command'
    script_name = 'tests'
    args = ('a', 'b')
    kwargs = {"a": "a"}
    token = 'Schedule0350c8c75ddcd9fafdaA9738df4c9346bec48dc9c4915'
    url = 'http://127.0.0.1:10011/api/v1/schedule/command/'
    data = {"fun_name": 'func', "command": command, "target": target, "script_name": script_name,
            "args": args
            }
    r = requests.get(url, data=json.dumps(data),
                 headers={'Content-Type': 'application/json', 'token': token}).json()
    print(r)


if __name__ == '__main__':
    # remote_command()

    file_sync(target="127.0.0.1", file_name="tests.py")

