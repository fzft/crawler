import logging.config
import os
import time
from my_logging.logging_handler import MyTimedRotatingFileHandler
basedir = os.path.abspath(os.path.dirname(__file__))


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "%(message)s",
            # 'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'my_logging.logging_handler.MyTimedRotatingFileHandler',
            'when' : 'd',
            'backupCount': 60,
            'delay': True,
            'filename': f'{basedir}/log/core.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            # 当达到10MB时分割日志
            'maxBytes': 1024 * 1024 * 10,
            # 最多保留50份文件
            'backupCount': 50,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': f'{basedir}/log/error.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'error_file', 'console'],
            'level': 'INFO',
        },
    }
})
