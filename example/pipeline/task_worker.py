import sys
import time
import zmq
import os


def task_worker():
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://127.0.0.1:5557")

    # Socket to send messages to
    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://127.0.0.1:5558")

    # Process tasks forever
    while True:
        s = receiver.recv()

        # Do the work
        time.sleep(1)
        # Send results to sink
        sender.send_string(str(s))

task_worker()