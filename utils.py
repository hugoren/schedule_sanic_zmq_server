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


def try_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(args, kwargs)
        except Exception as e:
            log('error', str(e))
            return str(e)
    return wrapper()


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
                    elif isinstance(r, str):
                        return json({"retcode": 0, "stdout": r})
                    else:
                        return json({"retcode": 0, "stdout": r})
                else:
                    return json({"retcode": 1, "stderr": "status{}".format(403)})
            except Exception as e:
                log('error', str(e))
                return json({'retcode': 1, 'stderr': str(e)})
        return auth_token
    return wrapper


def retry_wait(retry_count=0, interval_wait=0):
    def wrap(f):
        @wraps(f)
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if retry_count == 0:
                    return str(e)
                if str(e) == "retry":
                    if retry_count >= 1:
                        count = retry_count
                        while 1:
                            Event().wait(interval_wait)
                            try:
                                count = count - 1
                                print(count)
                                return f(*args, **kwargs)
                            except Exception as e:
                                print(e)
                                if count == 0:
                                    return str(e)
                                continue
                log('error', '函数{0}异常,{1}'.format(f.__name__, str(e)))
                return str(e)
        return func
    return wrap


async def redis_producer(key, value):
    r = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), db=0, loop=asyncio.get_event_loop())
    await r.rpush(key=key, value=value)
    r.close()
    await r.wait_closed()
    return


async def redis_consumer(key):
    r = await aioredis.create_redis_pool(
        (REDIS, REDIS_PORT), db=0, loop=asyncio.get_event_loop())
    result = await r.lpop(key=key)
    r.close()
    await r.wait_closed()
    return result


class Redis:
    def __init__(self, db):
        self.db = db
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self.db)
        self.r = redis.Redis(connection_pool=self.pool)

    def get(self, key):
        try:
            v = self.r.get(key)
            if self.db == 1 and v:
                v = eval(v)
                if isinstance(v, str):
                    v = eval(v)
            return v
        except Exception as e:
            log('error', str(e))

    def set(self, key, value, ex=None):
        if ex:
            v = self.r.set(key, value, ex=ex)
        else:
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
