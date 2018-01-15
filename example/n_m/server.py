import zmq


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://127.0.0.1:5560")

    while 1:
        message = socket.recv()
        print(message)
        socket.send(bytes("Hello, {}".format(message), encoding="utf-8"))
server()