import zmq
from config import MSG_CLIENT_PORT, MSG_BACKEND_PORT


def broker():
    context = zmq.Context()
    client = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    client.bind("tcp://127.0.0.1:{}".format(MSG_CLIENT_PORT))
    backend.bind("tcp://127.0.0.1:{}".format(MSG_BACKEND_PORT))

    poller = zmq.Poller()
    poller.register(client, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    # Switch messages between sockets
    while 1:
        socks = dict(poller.poll())
        if socks.get(client) == zmq.POLLIN:
            message = client.recv_multipart()
            backend.send_multipart(message)

        if socks.get(backend) == zmq.POLLIN:
            message = backend.recv_multipart()
            client.send_multipart(message)


if __name__ == '__main__':
    broker()