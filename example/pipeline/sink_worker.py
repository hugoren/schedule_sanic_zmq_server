import sys
import time
import zmq

def sink_worker():
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://127.0.0.1:5558")

    # Wait for start of batch
    s = receiver.recv()

    # Start our clock now
    tstart = time.time()

    # Process 100 confirmations
    total_msec = 0
    while True:
        s = receiver.recv()
        print(s)
        # Calculate and report duration of batch
        tend = time.time()
        print("Total elapsed time: %d msec" % ((tend-tstart)*1000))

sink_worker()