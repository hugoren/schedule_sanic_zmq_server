import asyncio
from utils import redis_producer


async def sync(jid, target, file_name):
    with open(file_name, 'r') as f:
            file_content = f.readlines()

    data = {"jid": jid, "target": target, "file_name": file_name, "command": "file_sync", "content": file_content}
    await redis_producer('task', '{}'.format(data))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync(target="127.0.0.1", file_name="tests.py"))
