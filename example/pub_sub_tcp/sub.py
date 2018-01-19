import zmq
import json


def sub():
    agent_id = '127.0.0.1'
    context = zmq.Context()
    print("{0} Connecting to server".format(agent_id))
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:14505")
    socket.setsockopt_string(zmq.SUBSCRIBE, agent_id)
    while 1:
        # message = socket.recv()
        message = socket.recv_multipart()
        msg = eval(message[1])
        if msg.get('command') == "file_sync":
            with open('{0}'.format(msg.get('file_name')), 'w') as f:
                f.writelines(msg.get('content'))

        print(msg)

sub()