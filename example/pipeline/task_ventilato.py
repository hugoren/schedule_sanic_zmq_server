import zmq
import random
import time


def task_ventilato():
    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://127.0.0.1:5557")

    # Socket with direct access to the sink: used to syncronize start of batch
    sink = context.socket(zmq.PUSH)
    sink.connect("tcp://127.0.0.1:5558")

    print("Sending tasks to workers…")

    # The first message is "0" and signals start of batch
    sink.send(b'0')

    # Initialize random number generator
    random.seed()

    # Send 100 tasks
    total_msec = 0
    for task_nbr in range(100):

        workload = random.randint(1, 100)
        total_msec += workload
        message = "task "+str(task_nbr)+"_"+str(workload)
        sender.send_string(u'%s' % message)

        print("Total expected cost: %s msec" % total_msec)

        # Give 0MQ time to deliver
        time.sleep(1)

task_ventilato()

