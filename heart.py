import time
import numpy
import zmq
from zmq import devices


def heart(name=None, heart_server_add=None):

    dev = devices.ThreadDevice(zmq.FORWARDER, zmq.SUB, zmq.DEALER)
    dev.setsockopt_in(zmq.SUBSCRIBE, b"")
    dev.connect_in('tcp://{0}:14508'.format(heart_server_add))
    dev.connect_out('tcp://{0}:14509'.format(heart_server_add))
    dev.setsockopt_out(zmq.IDENTITY, bytes(name, encoding='utf-8'))
    dev.start()

    time.sleep(1)

    A = numpy.random.random((2**11, 2**11))
    while True:
        tic = time.time()
        numpy.dot(A, A.transpose())
        print("blocked for %.3f s"%(time.time()-tic))


heart(name='sub_1', heart_server_add='127.0.0.1')