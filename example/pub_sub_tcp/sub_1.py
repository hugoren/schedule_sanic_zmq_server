import zmq


def sub():
    context = zmq.Context()
    print("Connecting to hello world server...")
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5556")
    socket.setsockopt(zmq.SUBSCRIBE, b'whoda')

    while 1:
        message = socket.recv()
        print(message)

sub()