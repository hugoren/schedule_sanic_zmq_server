import zmq


def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5559")

    #  Do 10 requests, waiting each time for a response
    for request in range(1, 10000):
        socket.send(b"hugo")
        message = socket.recv()
        print("Received reply %s [%s]" % (request, message))


client()