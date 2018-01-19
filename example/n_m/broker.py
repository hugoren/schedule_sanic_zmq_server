import zmq


def broker():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend.bind("tcp://127.0.0.1:5559")
    backend.bind("tcp://127.0.0.1:5560")

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    # Switch messages between sockets
    while 1:
        socks = dict(poller.poll())
        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv_multipart()
            backend.send_multipart(message)

        if socks.get(backend) == zmq.POLLIN:
            message = backend.recv_multipart()
            frontend.send_multipart(message)

broker()