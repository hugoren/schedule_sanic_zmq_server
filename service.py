import asyncio
import zmq
import time


async def server_reply():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    count = 0

    while 1:
        message = socket.recv()
        count += 1
        print("Received request: ", message, count)
        time.sleep(1)
        socket.send(bytes('{}--{}'.format(time.strftime("%Y%m%d%H%M%S"), "word"), encoding='utf-8'))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server_reply())
