import logging
import time
from functools import update_wrapper
from inspect import isfunction
from multiprocessing import Process
import multiprocessing as mp
import asyncio
import uuid
import random
import redis

from celery import Celery
# from rq.timeouts import JobTimeoutException
from twisted.internet import defer, reactor
from werkzeug.datastructures import ImmutableDict
import aiojobs
from celery.exceptions import SoftTimeLimitExceeded

from core.config import Config
from core.consistant import TaskStatus, RedisConfigParams, MongoConfigParams, CeleryQueue, SPECIAL_STATUS
from core.ctx import _AppCtxGlobals, TaskContext, AppContext
from core.exceptions import *
from core.exceptions import default_exceptions, CHANGE_CHANNEL
from db.redishelper import RedisClient
from utils.helpers import _PackageBoundObject
from core.core_utils import simple_log, log
from core._global import task


def setupmethod(f):
    def wrapper_func(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    return update_wrapper(wrapper_func, f)


class Crawl(_PackageBoundObject):
    default_config = ImmutableDict({
        RedisConfigParams.REDIS_HOST.value: '127.0.0.1',
        RedisConfigParams.REDIS_PORT.value: 6379,
        RedisConfigParams.REDIS_PWD.value: None,
        RedisConfigParams.REDIS_DB.value: 0,
        MongoConfigParams.MONGO_HOST.value: '127.0.0.1',
        MongoConfigParams.MONGO_PORT.value: '27017',
        CeleryQueue.TASK_QUEUE.value: None,
        CeleryQueue.CAPTCHA_TASKS_QUEUE.value: None
    })

    app_ctx_globals_class = _AppCtxGlobals
    config_class = Config
    celery_class = Celery

    def __init__(self, import_name, celery_config, root_path=None):
        super().__init__(import_name, root_path=root_path)
        self.config = self.make_config()
        self._error_handlers = {}
        self.error_handler_spec = {None: self._error_handlers}
        self.logger = logging.getLogger(__name__)
        self.deferred = None
        self.app = self.make_celery_config(celery_config)
        self.current_version = ''

    async def get_version(self):
        _db = RedisClient(**self.config)
        self.current_version = await _db.get(self.config.get(RedisConfigParams.VERSION_KEY.value))

    def _find_error_handler(self, e):
        exc_class, code = self._get_exc_class_and_code(type(e))

        def find_handler(handler_map):
            if not handler_map:
                return
            for cls in exc_class.__mro__:
                handler = handler_map.get(cls)
                if handler is not None:
                    handler_map[exc_class] = handler
                    return handler

        return find_handler(self.error_handler_spec[None].get(code))

    def make_celery_config(self, config):
        celery = self.celery_class('tasks')
        redis_url = 'redis://:%s@%s:%s/%s' % (
            self.config.get(RedisConfigParams.REDIS_PWD.value) or '',
            self.config.get(RedisConfigParams.REDIS_HOST.value),
            self.config.get(RedisConfigParams.REDIS_PORT.value),
            self.config.get(RedisConfigParams.CELERY_DB.value) or self.config.get(RedisConfigParams.REDIS_DB.value))
        self.redis_conn = redis.StrictRedis.from_url(redis_url)
        celery.conf.broker_url = redis_url
        celery.conf.result_backend = redis_url
        celery.config_from_object(config)
        return celery

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return self.config_class(root_path, self.default_config)

    @setupmethod
    def errorhandler(self, code_or_exception):

        """
        @app.errorhandler(404)
        def sys_err_handler(error):
            return print(error)
        """

        def decorator(f):
            self._register_error_handler(None, code_or_exception, f)
            return f

        return decorator

    async def task_monitor(self):
        _db = RedisClient(**self.config)
        scheduler = await aiojobs.create_scheduler()
        while True:
            try:
                task = await _db.load_task(self.current_version)
                if task is not None:
                    await log(task['token'], SPECIAL_STATUS.DIY_STATUS.value, message=f'从redis成功获取任务')
                    await scheduler.spawn(self.generate_tasks(task))
                await asyncio.sleep(.1)
            except:
                import traceback
                print(traceback.format_exc())

    # async def captcha_monitor(self):
    #     _db = RedisClient(**self.config)
    #     scheduler = await aiojobs.create_scheduler()
    #     while True:
    #         task = await _db.load_captcha()
    #         if task is not None:
    #             await scheduler.spawn(self.generate_tasks(task))
    #         await asyncio.sleep(.1)

    async def zrm_task(self):
        _db = RedisClient(**self.config)
        scheduler = await aiojobs.create_scheduler()
        while True:
            try:
                ret = await _db.zrem_task()
                if ret:
                    rem, rest = ret
                    notices = [log(token.decode().split(':')[2], '2003', __name__, area=token.decode().split(':')[0],
                                   channel_id=token.decode().split(':')[1],
                                   telephone=token.decode().split(':')[3],
                                   company_name=token.decode().split(':')[4],
                                   verify_result=token.decode().split(':')[5],
                                   id=token.decode().split(':')[6]
                                   ) for token
                               in rem]
                    dispatch = [_db.load_captcha(t.decode().split(':')[2], self.current_version) for t in rest]
                    for f in asyncio.as_completed(notices):
                        await f
                    for f2 in asyncio.as_completed(dispatch):
                        ret = await f2
                        if ret is not None:
                            await scheduler.spawn(self.generate_tasks(ret))
                    await asyncio.sleep(.1)
            except:
                import traceback
                print(traceback.format_exc())

    def monitor(self):
        loop = asyncio.get_event_loop()
        task_monitor_coro = self.task_monitor()
        zrm_task_coro = self.zrm_task()
        version_coro = self.get_version()
        loop.create_task(task_monitor_coro)
        loop.create_task(zrm_task_coro)
        loop.create_task(version_coro)
        loop.run_forever()

    def run(self):
        self.logger.info('monitor processing running')
        monitor_process = Process(target=self.monitor)
        monitor_process.start()

        # 启动一个进程监控 任务队列

    def generate_tasks(self, task):
        """specify the task delay process"""

    def _get_error_handlers(self, key):
        return self._error_handlers.get(key)

    def register_error_handler(self, code_or_exception, f):
        self._register_error_handler(None, code_or_exception, f)

    @setupmethod
    def _register_error_handler(self, key, code_or_exception, f):
        exc_class, code = self._get_exc_class_and_code(code_or_exception)

        handlers = self.error_handler_spec.setdefault(key, {}).setdefault(code, {})
        handlers[exc_class] = f

    def _set_error_handlers(self, value):
        self._error_handlers = value
        self.error_handler_spec[None] = value

    error_handlers = property(_get_error_handlers, _set_error_handlers)
    del _get_error_handlers, _set_error_handlers

    def handle_exception(self, e):
        handler = self._find_error_handler(e)
        return self.finalize_request(handler)

    def finalize_request(self, handler):
        d = defer.Deferred()
        d.addErrback(self.log_exception)
        if handler is not None and isfunction(handler):
            d.addErrback(handler)
        return d

    def log_exception(self, e):
        _db = RedisClient(**self.config)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait({
            e.value.task.save_data(exception=True, ex_message=e.value.code),
            _db.set_expire(f'{self.config.EXECUTED_TASK_PREFIX}{e.value.task.token}',
                           e.value.task.token, self.config[CeleryQueue.EXECUTED_TASK_PERSIST_TIME.value]),
            simple_log(e.value.task, e.value.code, out_message=e.value.description)
        }))
        raise e

    def driver_quit(self, e):
        pass

    # async def generate_tasks(self, task):
    #     print(task)
    #     result = eval('area_{}_task.delay'.format(task['area_code']))(task, )
    #     while True:
    #         if result.status == 'PENDING':
    #             break

    def my_monitor(self):
        app = self.app
        state = app.events.State()

        def announce_failed_tasks(event):
            state.event(event)
            # task name is sent only with -received event, and state
            # will keep track of this for us.
            task = state.tasks.get(event['uuid'])

            print('TASK FAILED: %s[%s] %s' % (
                task.name, task.uuid, task.info(),))

        def announce_receive_tasks(event):
            state.event(event)
            # task name is sent only with -received event, and state
            # will keep track of this for us.
            task = state.tasks.get(event['uuid'])

            print('TASK RECEIVED: %s[%s] %s' % (
                task.name, task.uuid, task.info(),))

        with app.connection() as connection:
            recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-received': announce_receive_tasks,
                '*': state.event,
            })
            recv.capture(limit=None, timeout=None, wakeup=True)

    def __call__(self, ctask, task_handler):
        src_area = ctask.get('Area')
        if ctask.get(self.config.get(CeleryQueue.EXECUTED_CHANNELS.value)) is None:
            ctask[self.config.get(CeleryQueue.EXECUTED_CHANNELS.value)] = [ctask.get('Area')]
        else:
            ctask.get(self.config.get(CeleryQueue.EXECUTED_CHANNELS.value)).append(ctask.get('Area'))
        task_context = TaskContext(self, ctask, task_handler)
        # 创建一个任务上下文
        task_context.push()
        # 将任务上下文入栈
        try:
            try:
                # 运行任务
                task_context.task.run()
            except SoftTimeLimitExceeded:
                # celery任务超时处理
                task.task_timeout_handler()
            except Exception as e:
                if isinstance(e, CHANGE_CHANNEL) and e.task is not None:
                    raise e
                if not isinstance(e, CrawlException):
                    import traceback
                    InternalServerError = SystemError.wrap(e.__class__)
                    e = InternalServerError(description=traceback.format_exc())
                    # 将错误封装成 InternalServerError 异常
                e.task = task
                deferred = self.handle_exception(e)
                # 生成一个错误处理的延迟函数
                deferred.errback(e)
                # 处理错误
        finally:
            final_code = task.final_code
            task_context.pop()
            # 任务上下文出栈
            return final_code

    def app_context(self):
        return AppContext(self)

    @staticmethod
    def _get_exc_class_and_code(exc_class_or_code):
        if isinstance(exc_class_or_code, str):
            exc_class = default_exceptions[exc_class_or_code]
        else:
            exc_class = exc_class_or_code

        assert issubclass(exc_class, Exception)

        if issubclass(exc_class, CrawlException):
            return exc_class, exc_class.code
        else:
            return exc_class, None
