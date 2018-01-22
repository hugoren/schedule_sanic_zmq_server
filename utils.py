import logging
import aioredis
import asyncio
import redis
import json as simplejson
from collections import deque
from sanic.response import json
from functools import wraps
from threading import Event
from config import TOKEN
from logging.handlers import RotatingFileHandler
from config import REDIS, REDIS_PORT


def log(level, message):

    logger = logging.getLogger('app')

    #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        log_name = 'app.log'
        log_count = 2
        log_format = '%(asctime)s %(levelname)s %(module)s %(funcName)s-[%(lineno)d] %(message)s'
        log_level = logging.INFO
        max_bytes = 10 * 1024 * 1024
        handler = RotatingFileHandler(log_name, mode='a', maxBytes=max_bytes, backupCount=log_count)
        handler.setFormatter(logging.Formatter(log_format))
        logger.setLevel(log_level)
        logger.addHandler(handler)

    if level == 'info':
        logger.info(message)
    if level == 'error':
        logger.error(message)


def auth(token):
    def wrapper(func):
        @wraps(func)
        async def auth_token(req, *arg, **kwargs):
            try:
                value = req.headers.get(token)
                if value and TOKEN == value:
                    r = await func(req, *arg, **kwargs)
                    if isinstance(r, dict):
                        return json(r)
                    if isinstance(r, str):
                        return json({"retcode": 0, "stdout": r})
                    else:
                        return json({"retcode": 0, "stdout": r})
                else:
                    return json({'retcode': 1, 'stderr': 'status{}'.format(403)})
            except Exception as e:
                log('error', str(e))
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
    def __init__(self, db):
        self.db = db
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self.db)
        self.r = redis.Redis(connection_pool=self.pool)

    def get(self, key):
        v = self.r.get(key)
        if self.db == 1 and v:
            v = simplejson.loads(str(v, encoding='utf-8'))
            v = eval(v)
        return v

    def set(self, key, value):
        v = self.r.set(key, value)
        return v

    def delete(self, key):
        self.r.delete(key)


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