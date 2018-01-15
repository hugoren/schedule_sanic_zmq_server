import zmq
import time
from zmq.utils.strtypes import asbytes


def publisher():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5555")
    topic = b'sub'
    while 1:
        message = "Publish Message: {}".format(time.strftime("%Y%m%d%H%M%S"))
        time.sleep(1)
        data = {"10001": 10001, "hugo": "boss"}
        # socket.send(bytes(message, encoding="utf-8"))
        # socket.send_json(json.dumps(data))
        # socket.send_string('fafa', flags=1)
        socket.send_multipart([topic, asbytes(message)])
        print(message)


publisher()
