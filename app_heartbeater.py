import time
import zmq
from zmq.eventloop import ioloop, zmqstream
from utils import Redis
from config import HEART_PUB_PORT, HEART_ROUTER_PORT


class HeartBeater:

    def __init__(self, loop, pingstream, pongstream, period=1000):
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
        """
        客户端心跳判断,
        1.pong, 存于redis 设计有效期
           设置key有效期，是为了防止心跳客户端down掉情况
        2.不pong, 从redis删除
        """
        client_beat_time = float(msg[1])
        if client_beat_time == self.lifetime:
            print(msg[0])
            Redis(2).set(key=msg[0], value="exist", ex=10)
        else:
            Redis(2).delete(key=msg[0])


def heartbeat_run():
    loop = ioloop.IOLoop()
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.bind('tcp://0.0.0.0:{}'.format(HEART_PUB_PORT))
    router = context.socket(zmq.ROUTER)
    router.bind('tcp://0.0.0.0:{}'.format(HEART_ROUTER_PORT))
    outstream = zmqstream.ZMQStream(pub, loop)
    instream = zmqstream.ZMQStream(router, loop)
    hb = HeartBeater(loop, outstream, instream)
    loop.start()


if __name__ == '__main__':
    heartbeat_run()