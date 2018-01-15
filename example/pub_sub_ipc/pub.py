import zmq, time


def zmq_p():
    try:
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.connect("ipc://test")
        while 1:
            publisher.send(b'hello world')
    except Exception as e:
        print(e)

zmq_p()