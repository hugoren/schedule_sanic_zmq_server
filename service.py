import asyncio
import pathlib
from utils import redis_producer
from utils import Redis
from config import SYNC_DIR


async def sync(jid, target, file_name):
    dir_exist = pathlib.Path(SYNC_DIR).exists()
    if dir_exist:
        file_exist = pathlib.Path('{}/{}'.format(SYNC_DIR, file_name))
        if file_exist.is_file():
            target_exist = Redis(2).get(target)
            if target_exist:
                with open(file_name, 'r') as f:
                        file_content = f.readlines()
                data = {"jid": jid, "target": target, "file_name": file_name, "command": "sync", "content": file_content}
                await redis_producer("task", "{}".format(data))
            else:
                Redis(1).set(key=jid, value="{}".format({"retcode": 1, "stderr": "{} client disconnects.".format(target)}))
        else:
            Redis(1).set(key=jid, value="{}".format({"retcode": 1, "stderr": "{} file does not exist".format(file_name)}))
    else:
        Redis(1).set(key=jid, value="{}".format({"retcode": 1, "stderr": "{} directory does not exist".format(SYNC_DIR)}))


async def remote_command(data):
    await redis_producer('task', '{}'.format(data))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync(target="127.0.0.1", file_name="tests.py"))
