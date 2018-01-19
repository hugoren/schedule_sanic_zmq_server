import zmq


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://127.0.0.1:14507")

    while 1:
        message = socket.recv()
        socket.send(bytes("Hello, {}".format('ff'), encoding="utf-8"))
        print(message)


if __name__ == '__main__':
    server()