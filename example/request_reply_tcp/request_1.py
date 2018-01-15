import zmq


def req():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")

    for i in range(10, 20):
        socket.send(bytes('Hello', encoding='utf-8'))
        message = socket.recv()
        print(message)


req()