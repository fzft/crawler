from werkzeug.local import LocalStack, LocalProxy
from functools import partial

_task_ctx_err_msg = '''\
Working outside of task context.
'''
_app_ctx_err_msg = '''\
Working outside of app context.
'''


def _lookup_task_object(name):
    top = _task_ctx_stack.top
    if top is None:
        raise RuntimeError(_task_ctx_err_msg)
    return getattr(top, name)


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return getattr(top, name)


_app_ctx_stack = LocalStack()
_task_ctx_stack = LocalStack()

task = LocalProxy(partial(_lookup_task_object, 'task'))
g = LocalProxy(partial(_lookup_app_object, 'g'))


def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app


current_app = LocalProxy(_find_app)


