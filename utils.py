import logging
import aioredis
import asyncio
from functools import wraps
from sanic.response import json
from config import TOKEN
from logging.handlers import RotatingFileHandler
from config import REDIS, REDIS_PORT

FILENAME = 'schedule.log'
BACKUP_COUNT = 5
FORMAT = '%(asctime)s %(levelname)s %(module)s %(funcName)s-[%(lineno)d] %(message)s'
LOG_LEVEL = logging.INFO
MAX_BYTES = 10 * 1024 * 1024
HANDLER = RotatingFileHandler(FILENAME, mode='a', maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
FORMATTER = logging.Formatter(FORMAT)
HANDLER.setFormatter(FORMATTER)
logger = logging.getLogger('schedule')
logger.setLevel(LOG_LEVEL)
logger.addHandler(HANDLER)


def auth(token):
    def wrapper(func):
        @wraps(func)
        async def auth_token(req, *arg, **kwargs):
            try:
                value = req.headers.get(token)
                if value and TOKEN == value:
                    r = await func(req, *arg, **kwargs)
                    return json({'retcode': 0, 'stdout': r})
                else:
                    return json({'retcode': 1, 'stderr': 'status{}'.format(403)})
            except Exception as e:
                logger.error(str(e))
                return json({'retcode': 1, 'stderr': str(e)})
        return auth_token
    return wrapper


async def redis_set(key, expire=10):
    redis = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), loop=asyncio.get_event_loop())
    await redis.set(key=key, value='success', expire=expire)
    print(key)
    redis.close()
    await redis.wait_closed()


async def redis_del(key):
    redis = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), loop=asyncio.get_event_loop())
    await redis.delete(key=key)
    redis.close()
    await redis.wait_closed()


async def redis_get(key):
    redis = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), loop=asyncio.get_event_loop())
    r = await redis.get(key=key)
    redis.close()
    await redis.wait_closed()
    return r
