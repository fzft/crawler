CELERYD_MAX_TASKS_PER_CHILD = 1
#
import sys

#
platform = sys.platform
if ('darwin' in platform) or ('linux' in platform):
    CELERY_ROUTES = {
        'tasks.*': {'queue': 'tax:linux'}
    }
else:
    CELERY_ROUTES = {
        'tasks.*': {'queue': 'tax:win'}
    }

CELERYD_CONCURRENCY = 2

# CELERYD_FORCE_EXECV = True
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_ENABLE_UTC = True

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化 ls: json yaml msgpack pickle(不推荐)

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 15  # 任务过期时间

CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_TASK_PUBLISH_RETRY = False  # 重试
CELERYD_TASK_SOFT_TIME_LIMIT = 600

CELERY_DISABLE_RATE_LIMITS = True
TASK_ACKS_LATE = True
