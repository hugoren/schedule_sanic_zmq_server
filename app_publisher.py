import zmq
import asyncio
import json
from zmq.utils.strtypes import asbytes
from threading import Event
from utils import redis_consumer
from config import PUB_PORT


async def pub():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:{}".format(PUB_PORT))
    while 1:
        msg_queue = await redis_consumer('task')
        if msg_queue:
            msg_queue = eval(msg_queue)
            topic = msg_queue.get('target')
            socket.send_multipart([bytes(topic, encoding="utf-8"), asbytes(json.dumps(msg_queue))])
        Event().wait(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pub())
