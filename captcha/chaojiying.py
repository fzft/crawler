#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5
import os

from captcha.captcha_validator import CaptchaValidatorImpl
from core.exceptions import AuthCodeErrorTooMany


class Chaojiying_Client(CaptchaValidatorImpl):
    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    async def post_pic(self, im, codetype):
        """请求超级鹰验证码识别,type=识别类型 请参阅超级鹰官网,content=图片的Byte
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

    def result_handler(self, data):
        result = data.get('err_no')
        if result == 0:
            code = data.get('pic_str')
            return code, data
        if str(result).startswith('1'):
            err_msg = data.get('err_str')
            raise AuthCodeErrorTooMany(description=err_msg)
        return None, data


