from enum import Enum, unique


@unique
class TaskStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    RUNNING = 'RUNNING'


@unique
class RedisConfigParams(Enum):
    REDIS_HOST = 'REDIS_HOST'
    REDIS_PORT = 'REDIS_PORT'
    REDIS_PWD = 'REDIS_PWD'
    REDIS_DB = 'REDIS_DB'
    REDIS_CRAWL_LOG = 'REDIS_CRAWL_LOG'
    CALL_RECORD_TOKEN = 'CALL_RECORD_TOKEN'
    VERSION_KEY = 'VERSION_KEY'
    CELERY_DB = 'CELERY_DB'
    TAX_CRAWL = 'TAX_CRAWL'
    LOCK_TIMEOUT = 'LOCK_TIMEOUT'


@unique
class Framework(Enum):
    TASK_FRAMEWORK = 'TASK_FRAMEWORK'


@unique
class MongoConfigParams(Enum):
    MONGO_HOST = 'MONGO_HOST'
    MONGO_PORT = 'MONGO_PORT'
    MONGO_USERNAME = 'MONGO_USERNAME'
    MONGO_PASSWORD = 'MONGO_PASSWORD'
    MONGO_AUTHSOURCE = 'MONGO_AUTHSOURCE'
    MONGO_AUTHMECHANISM = 'MONGO_AUTHMECHANISM'
    MONGO_DB = 'MONGO_DB'
    MONGO_REPLICASET = 'MONGO_REPLICASET'


@unique
class CeleryQueue(Enum):
    TASK_QUEUE = 'TASK_QUEUE'
    CAPTCHA_TASKS_QUEUE = 'CAPTCHA_QUEUE'
    META_KEY_PREFIX = 'META_KEY_PREFIX'
    META_KEY_EXPIRE = 'META_KEY_EXPIRE'
    STATUS_KEY_EXPIRE = 'STATUS_KEY_EXPIRE'
    YYS_ZSET_KEY = 'YYS_ZSET_KEY'
    YYS_ZSET_MEMBER_PREFIX = 'YYS_ZSET_MEMBER_PREFIX'
    YYS_ZSET_MEMBER_EXPIRE = 'YYS_ZSET_MEMBER_EXPIRE'
    TASK_CLASS_NAME = 'TASK_CLASS_NAME'
    PROXYXML_KEY = 'PROXYXML_KEY'
    PROXY_DYNAMIC_KEY = 'PROXY_DYNAMIC_KEY'
    EXECUTED_TASK_PREFIX = 'EXECUTED_TASK_PREFIX'
    EXECUTED_TASK_PERSIST_TIME = 'EXECUTED_TASK_PERSIST_TIME'
    TASK_FRAMEWORK = 'TASK_FRAMEWORK'
    EXECUTED_CHANNELS = 'EXECUTED_CHANNELS'


@unique
class CrawlPhase(Enum):
    BEFORE_LOGIN = 3
    AUTHORITY_LOGIN = 5
    AROUND_LOGIN = 7
    VALIDATOR_LOGIN = 9
    AFTER_LOGIN = 11


@unique
class CaptchaValidatorType(Enum):
    CAPTCHA_ONLINE = 1
    CAPTCHA_REDIS = 2


@unique
class PrometheusConfig(Enum):
    PORT = 'METRICS_PORT'


@unique
class RequestConfig(Enum):
    REQUEST_TIMEOUT = 'REQUEST_TIMEOUT'
    REQUEST_RETRY = 'REQUEST_RETRY'
    PROXY_RETRY = 'PROXY_RETRY'
    ADSL_URL = 'ADSL_URL'


@unique
class RABBITMQ(Enum):
    RABBITMQ_HOST = 'RABBITMQ_HOST'
    RABBITMQ_PORT = 'RABBITMQ_PORT'
    RABBITMQ_USERNAME = 'RABBITMQ_USERNAME'
    RABBITMQ_PASSWORD = 'RABBITMQ_PASSWORD'


@unique
class ELK(Enum):
    ELK_HOST = 'ELK_HOST'
    ELK_PORT = 'ELK_PORT'
    ELK_INDEX = 'ELK_INDEX'
    USR = 'ELK_USR'
    PWD = 'ELK_PWD'


@unique
class TaskParam(Enum):
    TOKEN = 'token'


@unique
class CallRecordParam(Enum):
    REGISTRATION_INFO = 'registration'
    DECLARATION = 'declaration'
    RATING = 'rating'
    INSPECTION = 'inspection'
    INVOICEINFORMATION = 'invoiceinformation'
    PERSON = 'person'
    STATISTICS = 'statistics'


@unique
class ContentFlag(Enum):
    ALLS = 'alls'
    ALL = 'all'
    SMS = 'sms'
    BUSI = 'busi'
    NET = 'net'
    BALANCE = 'balance'
    RECHARGE = 'recharge'


@unique
class TaxParams(Enum):
    TAX_FROM_YEAR = 'TAX_FROM_YEAR'


@unique
class PdfDeclaration(Enum):
    PDF_QUEUE = 'PDF_QUEUE'
    PDF_TASK = 'PDF_TASK'
    PDF_ACTIVE = 'PDF_ACTIVE'


@unique
class SPECIAL_STATUS(Enum):
    """个人使用"""
    DIY_STATUS = '10086'
    STATISTICS_STATUS = '10085'


if __name__ == '__main__':
    import enum
