import json
import logging
import asyncio
import time
from functools import wraps

from json.decoder import JSONDecodeError
from zope.interface import Interface, implementer
import aioredis
import logging
from core.consistant import *
from core.exceptions import RedisError, RedisSystemError

import sys

logger = logger = logging.getLogger(__name__)


def redis_exception_handler(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        inst = args[0]
        if isinstance(inst, AbstractRedisClient):
            try:
                f = await func(*args, **kwargs)
                return f
            except Exception:
                import traceback
                raise RedisError(description=str(traceback.format_exc()))
        return None

    return wrapped



AIO_REDIS_POOL = None


class IRedisClient(Interface):
    async def rpop(self, key):
        pass

    async def get(self, key):
        pass

    async def set(self, key, item):
        pass

    async def lpush(self, key, item):
        pass

    async def llen(self, key):
        pass

    async def expire(self, key, seconds):
        pass

    async def delete(self, key):
        pass


@implementer(IRedisClient)
class AbstractRedisClient():

    def __init__(self, **config):
        self.config = config
        self.host = config.get(RedisConfigParams.REDIS_HOST.value) or 'localhost'
        self.port = config.get(RedisConfigParams.REDIS_PORT.value) or '6379'
        self.db = config.get(RedisConfigParams.REDIS_DB.value) or 0
        self.pwd = config.get(RedisConfigParams.REDIS_PWD.value) or None

    async def __aenter__(self):
        global AIO_REDIS_POOL
        if AIO_REDIS_POOL: return AIO_REDIS_POOL
        AIO_REDIS_POOL = await aioredis.create_pool((self.host, self.port), db=self.db, password=self.pwd)
        return AIO_REDIS_POOL

    @redis_exception_handler
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @redis_exception_handler
    async def rpop(self, key):
        async with self as redis:
            return await redis.execute('rpop', key)

    @redis_exception_handler
    async def get(self, key):
        async with self as redis:
            return await redis.execute('get', key)

    @redis_exception_handler
    async def set(self, key, item):
        async with self as redis:
            await redis.execute('set', key, item)

    @redis_exception_handler
    async def lpush(self, key, item):
        async with self as redis:
            await redis.execute('lpush', key, item)

    @redis_exception_handler
    async def llen(self, key):
        async with self as redis:
            return await redis.execute('llen', key)

    @redis_exception_handler
    async def delete(self, key):
        async with self as redis:
            await redis.execute('del', key)

    @redis_exception_handler
    async def lpush_expire(self, key, item, sec=None):
        async with self as redis:
            await redis.execute('lpush', key, item)
            await redis.execute('expire', key, sec or self.config[CeleryQueue.STATUS_KEY_EXPIRE.value])

    @redis_exception_handler
    async def set_expire(self, key, item, sec=None):
        async with self as redis:
            await redis.execute('set', key, item)
            await redis.execute('expire', key, sec or self.config[CeleryQueue.STATUS_KEY_EXPIRE.value])

    @redis_exception_handler
    async def exists(self, key):
        async with self as redis:
            return await redis.execute('exists', key)

    @redis_exception_handler
    async def zadd(self, key, member, value):
        async with self as redis:
            # result = await redis.execute('zrank', key, member)
            # if result is None:
            await redis.execute('zadd', key, value, member)

    @redis_exception_handler
    async def zrem(self, key, member):
        async with self as redis:
            await redis.execute('zrem', key, member)

    @redis_exception_handler
    async def zremrangebyscore(self, key, min, max):
        async with self as redis:
            try:
                rem_result = await redis.execute('zrangebyscore', key, min, max)
                rest_result = await redis.execute('zrangebyscore', key, max + 1, '+inf')
                await redis.execute('zremrangebyscore', key, min, max)
                return rem_result, rest_result
            except:
                import traceback
                print(traceback.format_exc())


class RedisClient(AbstractRedisClient):
    @redis_exception_handler
    async def check_version(self, version):
        cur_version = await self.get(self.config.get(RedisConfigParams.VERSION_KEY.value))
        if cur_version == version:
            return True
        else:
            return False

    @redis_exception_handler
    async def load_task(self, version):
            if (await self.check_version(version)):
                loop = asyncio.get_event_loop()
                fut = loop.create_task(self.llen(self.config.get(CeleryQueue.TASK_QUEUE.value)))
                if await asyncio.wait_for(fut, timeout=10) > 0:
                    task_str = await self.rpop(self.config.get(CeleryQueue.TASK_QUEUE.value))
                    if task_str is not None:
                        try:
                            task = json.loads(task_str)
                            task['phase'] = 1
                            return task
                        except JSONDecodeError:
                            pass
                        return

    @redis_exception_handler
    async def load_captcha(self, token, version):
        # fut = loop.create_task(self.llen(self.config.get(CeleryQueue.CAPTCHA_TASKS_QUEUE.value)))
        # if await asyncio.wait_for(fut, timeout=10) > 0:
        #     task_str = await self.rpop(self.config.get(CeleryQueue.CAPTCHA_TASKS_QUEUE.value))
        #     try:
            if (await self.check_version(version)):
                task_str = await self.rpop('sy:request:{}'.format(token))
                if task_str is not None:
                    task_str = task_str.decode()
                    task = {}
                    task[TaskParam.TOKEN.value] = token
                    task['smsvalue'] = task_str.split('_')[1]
                    cls = await self.rpop(f'{self.config.get(CeleryQueue.TASK_CLASS_NAME.value)}:{token}')
                    task['phase'] = 2
                    task['province'] = cls.decode()
                    return task

    @redis_exception_handler
    async def save_status(self, key, data, sec=None):
        if await self.exists(key):
            await self.lpush(key, data)
        else:
            await self.lpush_expire(key, data, sec or self.config[CeleryQueue.STATUS_KEY_EXPIRE.value])

    @redis_exception_handler
    async def save_meta(self, key, data, sec=None):
        if await self.exists(key):
            await self.lpush(key, data)
        else:
            await self.lpush_expire(key, data, sec or self.config[CeleryQueue.META_KEY_EXPIRE.value])

    @redis_exception_handler
    async def sub(self, key, func):
        try:
            async with self as conn:
                await conn.execute_pubsub('psubscribe', key)
                channel = conn.pubsub_patterns[key]
                await func(channel)
                await conn.execute_pubsub('unpsubscribe', key)
        except Exception as e:
            print(e)

    @redis_exception_handler
    async def zadd_task(self, member=None, sec=None):
        await self.zadd(self.config[CeleryQueue.YYS_ZSET_KEY.value], member,
                        int(time.time()) + (sec or self.config[CeleryQueue.YYS_ZSET_MEMBER_EXPIRE.value]))

    @redis_exception_handler
    async def zrem_task(self):
            mid = int(time.time())
            return await self.zremrangebyscore(self.config[CeleryQueue.YYS_ZSET_KEY.value], 0, mid - 1)

    @redis_exception_handler
    async def zrem_certain_task(self, member):
        await self.zrem(self.config[CeleryQueue.YYS_ZSET_KEY.value], member)


async def main():
    rc = RedisClient(REDIS_HOST='127.0.0.1')
    result = await rc.delete('item1')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
