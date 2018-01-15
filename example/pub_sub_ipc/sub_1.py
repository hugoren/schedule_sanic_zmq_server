import zmq


def zmq_s():
    try:
        print('s')
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.bind("ipc://test")
        subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        while 1:
            print(subscriber.recv())
    except Exception as e:
        print(e)

zmq_s()