import asyncio

from captcha.chaojiying import Chaojiying_Client
from captcha.MachineDistinguish import MachineDistinguish
from core.core_utils import simple_log
from core.consistant import SPECIAL_STATUS
import traceback
from core.exceptions import *


class CaptchaValidatorUtils(object):

    def __init__(self):
        pass

    @staticmethod
    async def GetCapthaByContent(spider, content, codetype=1902, clz=Chaojiying_Client):
        if issubclass(clz, Chaojiying_Client):
            capt_validator = Chaojiying_Client()
        elif issubclass(clz, MachineDistinguish):
            capt_validator = MachineDistinguish(codetype)
        try:
            result = await capt_validator.post_pic(content, codetype)
        except Exception as e:
            await simple_log(spider, SPECIAL_STATUS.DIY_STATUS.value, message=f'打码平台出错{str(traceback.format_exc())}')
            result = {'err_no': 0, 'err_str': 'OK', 'pic_str': ''}
        code, result = capt_validator.result_handler(result)
        await simple_log(spider, SPECIAL_STATUS.DIY_STATUS.value, message=f'打码平台返回结果{result}')
        if issubclass(clz, Chaojiying_Client):
            return code
        elif issubclass(clz, MachineDistinguish):
            return code, result

    @classmethod
    async def get_captcha_with_retry(cls, spider, content, codetype=1902, retry=3, clz=Chaojiying_Client):
        while retry > 0:
            ret = await cls.GetCapthaByContent(spider, content, codetype, clz=clz)
            if ret is not None and ret.strip():
                return ret
            else:
                retry -= 1
        return None
