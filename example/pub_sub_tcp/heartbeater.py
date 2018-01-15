import time
import zmq
from zmq.eventloop import ioloop, zmqstream


class HeartBeater:

    def __init__(self, loop, pingstream, pongstream, period=3000):
        self.loop = loop
        self.period = period

        self.pingstream = pingstream
        self.pongstream = pongstream
        self.pongstream.on_recv(self.handle_pong)

        self.hearts = set()
        self.responses = set()
        self.lifetime = 0
        self.tic = time.time()

        self.caller = ioloop.PeriodicCallback(self.beat, period, self.loop)
        self.caller.start()

    def beat(self):
        toc = time.time()
        self.lifetime += toc-self.tic
        self.tic = toc
        goodhearts = self.hearts.intersection(self.responses)
        heartfailures = self.hearts.difference(goodhearts)
        newhearts = self.responses.difference(goodhearts)
        map(self.handle_new_heart, newhearts)
        map(self.handle_heart_failure, heartfailures)
        self.responses = set()
        self.pingstream.send(bytes(str(self.lifetime), encoding='utf-8'))

    def handle_new_heart(self, heart):
        self.hearts.add(heart)

    def handle_heart_failure(self, heart):
        self.hearts.remove(heart)

    def handle_pong(self, msg):
        client_beat_time = float(msg[1])
        if client_beat_time == self.lifetime:
            # self.responses.add(msg[0])
            print(msg)
        else:
            print("got bad heartbeat (possibly old?): %s"%msg[1])


def run():
    loop = ioloop.IOLoop()
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.bind('tcp://0.0.0.0:15555')
    router = context.socket(zmq.ROUTER)
    router.bind('tcp://0.0.0.0:15556')
    outstream = zmqstream.ZMQStream(pub, loop)
    instream = zmqstream.ZMQStream(router, loop)
    hb = HeartBeater(loop, outstream, instream)
    loop.start()


if __name__ == '__main__':
    run()