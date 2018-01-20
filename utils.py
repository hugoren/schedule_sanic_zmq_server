import logging
import aioredis
import asyncio
import redis
from collections import deque
from sanic.response import json
from functools import wraps
from threading import Event
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


async def redis_producer(key, value):
    redis = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), db=0, loop=asyncio.get_event_loop())
    await redis.rpush(key=key, value=value)
    redis.close()
    await redis.wait_closed()
    return


async def redis_consumer(key):
    redis = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), db=0, loop=asyncio.get_event_loop())
    r = await redis.lpop(key=key)
    redis.close()
    await redis.wait_closed()
    return r


class Redis:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
        self.r = redis.Redis(connection_pool=self.pool)

    def get(self, key):
        v = self.r.get(key)
        return v

    def set(self, key, value):
        v = self.r.set(key, value)
        return v


class TaskQueue:
    def __init__(self):
        self.q = deque()

    def insert(self, data):
        self.q.append(data)

    def get(self):
        if self.q:
            r = self.q.pop()
            return r


def retry_wait(retry_count=0, interval_wait=0):
    def wrap(f):
        @wraps(f)
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if retry_count == 0:
                    return str(e)
                if retry_count >= 1:
                    count = retry_count
                    while 1:
                        Event().wait(interval_wait)
                        try:
                            count = count - 1
                            return f(*args, **kwargs)
                        except Exception as e:
                            if count == 0:
                                return str(e)
                            continue
        return func
    return wrap