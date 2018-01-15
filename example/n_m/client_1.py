import zmq
import time
import json

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5559")

    for request in range(1, 10000):

        data = {"test": "bossdfasfafasdfdsafaafdsafasfasfsafa土大木土工fdsafasfa"
                         "gfdsgdsgsdfgsdkjgsdjfgj我是中国人gfdsgdsgsdfgsdkjgsdjfgj我是中国人"
                         "gfdsgdsgsdfgsdkjgsdjfgj我是中国人gfdsgdsgsdfgsdkjgsdjfgj我是中国人"
                         "gfdsgdsgsdfgsdkjgsdjfgj我是中国人"
                          }
        socket.send_json(json.dumps(data))
        message = socket.recv()
        print(message)


client()