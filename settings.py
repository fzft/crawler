PROFILE_ACTIVE = 'local'

# 切换异步任务框架
TASK_FRAMEWORK = 'celery'

TIME_OUT = 30000
TASK_QUEUE = 'tax:tasks'
CAPTCHA_QUEUE = 'captcha:queue'
MOBILE_STATUS = 'sy_response_'
STATUS_KEY_EXPIRE = 600
META_KEY_EXPIRE = 600
TASK_CLASS_NAME = 'task:cls'
META_KEY_PREFIX = 'mobile:meta'
# PROXYXML_KEY = 'proxyXml'
YYS_ZSET_KEY = 'tax:zset'
YYS_ZSET_MEMBER_PREFIX = 'tax:member'
YYS_ZSET_MEMBER_EXPIRE = 300
METRICS_PORT = 5000
PROXY_RETRY = 3

LOCK_TIMEOUT = 300

## tax params
TAX_FROM_YEAR = 2018

PROXYXML_KEY = 'credit:config:proxyXml'

EXECUTED_CHANNELS = 'executed_channels'

# 版本号
VERSION_KEY = 'credit:config:py:operator:version'

# 归属地是否检测ip
PROXY_DYNAMIC_KEY = 'credit:config:py:operator:proxy:dynamic'

# 已执行任务的地址
EXECUTED_TASK_PREFIX = 'py:operator:executed:task:'
# 已执行1任务保存时间
EXECUTED_TASK_PERSIST_TIME = 86400

REQUEST_TIMEOUT = 30
REQUEST_RETRY = 3

ADSL_URL = 'http://jproxy.tanzhishuju.com/JProxy/update/proxy/scoreproxy'

REDIS_CRAWL_LOG = 'CRAWLER_LOG'

CALL_RECORD_TOKEN = 'CallRecordToken'

TAX_CRAWL = 'tax:crawl'

# pdf 申报解析
PDF_ACTIVE = False  # 是否启用 申报表
PDF_QUEUE = 'parse:pdf'
PDF_TASK = 'tasks.parse_pdf_distribute_server_route'

import sys
import os

platform = sys.platform

if ('darwin' in platform) or ('linux' in platform):
    TASK_QUEUE = 'tax:tasks:linux'
else:
    TASK_QUEUE = 'tax:tasks:win'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CHROME_DOWM = os.path.join(BASE_DIR, 'log', 'seleniumdown')
CHROME_DRIVER = os.path.join(BASE_DIR, 'chromedriver')