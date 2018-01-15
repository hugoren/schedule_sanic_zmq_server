import zmq


def sub():
    context = zmq.Context()
    print("Connecting to hello world server...")
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")
    # socket.setsockopt(zmq.SUBSCRIBE, b'10001')
    socket.setsockopt_string(zmq.SUBSCRIBE, 'sub')
    while 1:
        # message = socket.recv()
        message = socket.recv_multipart()
        print(message)

sub()