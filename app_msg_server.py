import zmq
import json
from utils import Redis
from config import MSG_BACKEND_PORT


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://127.0.0.1:{}".format(MSG_BACKEND_PORT))

    while 1:
        message = socket.recv()
        data = json.loads(eval(message))
        socket.send(bytes("message , received", encoding="utf-8"))
        Redis(1).set(data.get('jid'), message)


if __name__ == '__main__':
    server()