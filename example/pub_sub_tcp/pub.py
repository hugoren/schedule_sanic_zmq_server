import zmq
import time
from zmq.utils.strtypes import asbytes


class Publisher:

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5555")

    def send(self, data):
        self.pub(data)

    def pub(self, data=None):
        print(data)
        topic = b'sub'
        while 1:
            if data:
                message = "Publish Message: {}".format(time.strftime("%Y%m%d%H%M%S"))
                time.sleep(1)
                data = {"10001": 10001, "hugo": "boss"}
                # socket.send(bytes(message, encoding="utf-8"))
                # socket.send_json(json.dumps(data))
                # socket.send_string('fafa', flags=1)
                self.socket.send_multipart([topic, asbytes(message)])
                print(message)


Publisher().pub()
