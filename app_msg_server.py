import zmq
import json
from utils import Redis


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://127.0.0.1:14507")

    while 1:
        message = socket.recv()
        data = json.loads(eval(message))
        socket.send(bytes("{0} message , received".format(data.get("jid")), encoding="utf-8"))
        Redis().set(data.get('jid'), message)


if __name__ == '__main__':
    server()