# 数据库
REDIS_HOST = ''
REDIS_PORT = 6379
REDIS_PWD = '123456'
REDIS_DB = 7

MONGO_HOST = ''
MONGO_PORT = 27017
MONGO_DB = 'tax'
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = '123456'
MONGO_AUTHSOURCE = 'admin'
MONGO_AUTHMECHANISM = 'SCRAM-SHA-1'

ELK_HOST = ''
ELK_PORT = ''
ELK_INDEX = 'tax_test'
ELK_USR = ''
ELK_PWD = ''
import sys
PUPPETEER_CHROMIUM_PATH = '/usr/bin/chromium-browser'
platform = sys.platform
if ('darwin' in platform) or ('linux' in platform):
    TASK_QUEUE = 'tax:tasks:linux'
else:
    TASK_QUEUE = 'tax:tasks:win'
