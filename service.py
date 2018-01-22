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
                data = {"jid": jid, "target": target, "file_name": file_name, "command": "file_sync", "content": file_content}
                await redis_producer('task', '{}'.format(data))
            else:
                Redis(1).set(key=jid, value='{}'.format({"retcode": 1, "stderr": "{} 客户端断开".format(target)}))
        else:
            Redis(1).set(key=jid, value='{}'.format({"retcode": 1, "stderr": "{} 文件不存在".format(file_name)}))
    else:
        Redis(1).set(key=jid, value='{}'.format({"retcode": 1, "stderr": "{} 目录不存在".format(SYNC_DIR)}))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync(target="127.0.0.1", file_name="tests.py"))
