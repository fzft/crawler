# from core._global import _app_ctx_stack, _task_ctx_stack
import redis_lock
import redis
from motor.motor_asyncio import AsyncIOMotorClient

from core.task_data import Structure
from core._global import _app_ctx_stack, _task_ctx_stack, current_app
from validators.validators import *
from core.consistant import TaskParam, SPECIAL_STATUS as diy, RedisConfigParams, MongoConfigParams

from core.core_utils import simple_log

_sentinel = object()


class MyDataClass(Structure):
    account = String()
    password = String()
    token = String()


class _AppCtxGlobals(object):
    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def pop(self, name, default=_sentinel):
        if default is _sentinel:
            return self.__dict__.pop(name)
        else:
            return self.__dict__.pop(name, default)

    def setdefault(self, name, default=None):
        return self.__dict__.setdefault(name, default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        top = _app_ctx_stack.top
        if top is not None:
            return '<crawl.g of %r>' % top.app
        return object.__repr__(self)


class AppContext(object):
    def __init__(self, app):
        self.app = app
        self.g = app.app_ctx_globals_class()

    def push(self):
        _app_ctx_stack.push(self)

    def pop(self):
        rv = _app_ctx_stack.pop()


class TaskHandler(object):
    task_data_cls = MyDataClass

    def __init__(self, token=None, task=None, *args, **kwargs):
        self.token = token
        self.task = task
        self.final_code = ''
        self.task_params = {}

    def run(self):
        self.task_params = self.task_data_cls(**self.task).get_data()

    def task_timeout_handler(self):
        """处理任务超时"""

    async def statistics_pipeline(self, exception=False, ex_message=None):
        """统计结果"""

    async def save_data(self, exception=False):
        """保存数据"""

    async def resource_lock_handler(self, resource_name):
        try:
            flag = True
            lock = redis_lock.Lock(current_app.redis_conn, resource_name,
                                   expire=current_app.config[RedisConfigParams.LOCK_TIMEOUT.value], auto_renewal=True)
            if lock.acquire(blocking=False):
                await self.main()
            else:
                await simple_log(self, diy.DIY_STATUS.value, message='任务已被执行')
                flag = False
        except Exception as e:
            raise e
        finally:
            if lock.locked() and flag:
                lock.release()

    async def main(self):
        """主方法"""


class TaskContext():
    task_handler = TaskHandler

    def __init__(self, app, task, task_handler):
        self.token = task.get(TaskParam.TOKEN.value)
        self.app = app
        if task_handler is not None:
            self.task_handler = task_handler
        self.task = task_handler(self.token, task)
        self.preserved = False
        self._implicit_app_ctx_stack = []

    def _get_g(self):
        return _app_ctx_stack.top.g

    def _set_g(self, value):
        _app_ctx_stack.top.g = value

    g = property(_get_g, _set_g)
    del _get_g, _set_g

    def push(self):
        _task_ctx_stack.push(self)
        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:
            app_ctx = self.app.app_context()
            app_ctx.push()
            self._implicit_app_ctx_stack.append(app_ctx)
        else:
            self._implicit_app_ctx_stack.append(None)

    def pop(self):
        app_ctx = self._implicit_app_ctx_stack.pop()
        rv = _task_ctx_stack.pop()
        if app_ctx is not None:
            app_ctx.pop()

        assert rv is self, 'Popped wrong task context.  ' \
                           '(%r instead of %r)' % (rv, self)
