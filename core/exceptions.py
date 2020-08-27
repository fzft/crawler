import sys

from core.code_map import REQUEST_TASK_STATUS_CODE
from utils.noconflict import classmaker


class CrawlException(Exception):
    code = None
    description = None
    task = None

    def __init__(self, description=None, task=None):
        Exception.__init__(self)
        if description is not None:
            self.description = description
        else:
            self.description = self.name
        self.task = task

    @classmethod
    def wrap(cls, exception, name=None):
        class newcls(cls, exception, metaclass=classmaker()):
            def __init__(self, arg=None, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)
                # exception.__init__(self, arg)

        newcls.__module__ = sys._getframe(1).f_globals.get('__name__')
        newcls.__name__ = name or cls.__name__ + exception.__name__
        return newcls

    @property
    def name(self):
        return REQUEST_TASK_STATUS_CODE.get(self.code, 'Unknown Error')

    def __str__(self):
        code = self.code if self.code is not None else '???'
        return '%s %s: %s' % (code, self.name, self.description)

    def __repr__(self):
        code = self.code if self.code is not None else '???'
        return "<%s '%s: %s'>" % (self.__class__.__name__, code, self.name)


"""传入参数的问题"""


class InvalidParams(CrawlException):
    """参数错误"""
    code = '1002'


"""系统问题"""


class SystemError(CrawlException):
    """系统问题"""
    code = '3001'


class RedisError(SystemError):
    code = '3001'


class MongoError(SystemError):
    code = '3001'


class RedisSystemError(SystemError):
    code = '3001'


"""
网站之类的问题
"""


class RequestTimeout(CrawlException):
    """访问超时"""


class WebSiteError(CrawlException):
    """网站问题"""
    code = '1117'


class LoginError(CrawlException):
    """登录时的问题"""
    code = '1117'


class LoginValidateError(CrawlException):
    """登录时验证码错误"""
    code = '6009'


class LoginAccountError(CrawlException):
    """登录时帐号错误"""
    code = '1003'


class LoginTimeout(CrawlException):
    """登录超时"""
    code = '6007'


class LoginUnknownFail(CrawlException):
    """登录时的未知错误"""
    code = '1117'


class DownloadFieldDoesNotExist(CrawlException):
    code = '6002'


class PermissionDenied(CrawlException):
    code = '1020'


class SessionTimeout(CrawlException):
    code = '1021'


class InvalidUsername(CrawlException):
    code = '1022'


class DownloadTimeout(CrawlException):
    code = '6007'


class DownloadPageNotFound(CrawlException):
    code = '6003'


class ParamsFormatterError(CrawlException):
    code = '2041'


class RequestParamsError(CrawlException):
    code = '1013'


class SendSmsWrong(CrawlException):
    code = '2008'


class SmsSendTooMany(CrawlException):
    code = '2006'


class WebSiteTimeOut(CrawlException):
    code = '1118'


class SMSError(CrawlException):
    code = '2002'


class WebSiteException(CrawlException):
    code = '3001'


class IdentityCardError(CrawlException):
    code = '2027'


class SMSWrongTooMany(CrawlException):
    code = '2001'


class UserInfoError(CrawlException):
    code = '1018'


class AuthCodeErrorTooMany(CrawlException):
    code = '2100'


class SHXYDMError(CrawlException):
    code = '1019'


class WaitInputSMSTimeOut(CrawlException):
    code = '2033'


class SendWrongNumber(CrawlException):
    code = '2004'


class PasswordWrongTooMany(CrawlException):
    code = '1105'


class PasswordError(CrawlException):
    code = '1102'


class AccountLock(CrawlException):
    code = '1005'


class TelephoneError(CrawlException):
    code = '1004'


class PasswordReset(CrawlException):
    code = '1016'


class UnLogin(CrawlException):
    code = '1008'


class UserNameNoExist(CrawlException):
    code = '1103'


class CompanyNameError(CrawlException):
    code = '1009'


class PasswordTooEasy(CrawlException):
    code = '1011'


class LoginExceeded(CrawlException):
    code = '1017'


class IllegalUser(CrawlException):
    code = '1013'


class PreserveError(CrawlException):
    code = '2054'


class NSRSBHMismatch(CrawlException):
    code = '1010'


class PasswordUnset(CrawlException):
    code = '2007'


class CELERY_TASK_RETRY(Exception):
    pass


class CHANGE_CHANNEL(CrawlException):
    pass


default_exceptions = {}
__all__ = ['CrawlException']

from werkzeug._compat import iteritems


def _find_exceptions():
    for name, obj in iteritems(globals()):
        try:
            is_http_exception = issubclass(obj, CrawlException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.code is None:
            continue
        __all__.append(obj.__name__)
        old_obj = default_exceptions.get(obj.code, None)
        if old_obj is not None and issubclass(obj, old_obj):
            continue
        default_exceptions[obj.code] = obj


_find_exceptions()
del _find_exceptions

if __name__ == '__main__':
    print(default_exceptions)
