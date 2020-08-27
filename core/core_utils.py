# encoding=utf-8
import inspect
import json
import logging
import os
import re
import time
import sys
import urllib

from enum import Enum
from functools import wraps
import enum
import traceback

from aioelasticsearch import Elasticsearch, helpers
import execjs
from aiomongodel import Document
from bs4 import BeautifulSoup
from werkzeug.local import LocalProxy

import datetime
from dateutil.relativedelta import relativedelta
from core.code_map import REQUEST_TASK_STATUS_CODE
from core import config
from core.consistant import CeleryQueue, ELK, RedisConfigParams, SPECIAL_STATUS as diy
from core.exceptions import *
from core import IP
from db.redishelper import RedisClient
from encrypt.encrypt import EncryptDate, Rsa_bcii
from utils import get_root_path

# from core.ctx import TaskHandler

sys.path.append("..")
from ext import config


def make_signature(names):
    return inspect.Signature(inspect.Parameter(fname, inspect.Parameter.POSITIONAL_OR_KEYWORD) for fname in names)


def file_reader(file_path):
    htmlstr = ''
    with open(file_path, 'r', encoding='UTF-8') as f:
        line = f.readline()
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
    return htmlstr


def time_stamp():
    return str(int(time.time() * 1000))


def get_project_path():
    return os.getcwd().split('/core')[0]


def parse_xml_to_dic(path: str) -> dict:
    dit = {}
    html = file_reader(path)
    nodes = re.compile(r'ClassName=\"(.*?)\"\s*code=\"(.*?)\"').findall(html)
    for n in nodes:
        dit[n[0]] = n[1]
        dit[f'{n[0]}App'] = n[1]
    return dit


def parse_xml_to_chn(path: str) -> dict:
    dit = {}
    html = file_reader(path)
    nodes = re.compile(r'<(.*?)\s*ClassName=\"(.*?)\"\s*code=\".*\"').findall(html)
    for n in nodes:
        dit[n[1]] = n[0]
        dit[f'{n[1]}App'] = n[0]
    return dit


def parse_xml_to_type(src: str) -> dict:
    nodes = re.compile(r'MoBileType=\"(.*?)\"').findall(src)
    return nodes


rc = RedisClient(**config)


# srv_map = parse_xml_to_dic(os.path.join(get_project_path(), 'SrvCode.xml'))
# sys_map = parse_xml_to_dic(os.path.join(get_project_path(), 'SysCode.xml'))
# chn_map = parse_xml_to_chn(os.path.join(get_project_path(), 'SrvCode.xml'))


def get_spider_name(inst):
    if isinstance(inst, LocalProxy):
        return inst.__dict__.get('task').get('Area')
    else:
        return inst.__class__.__name__


def get_area_name(inst):
    if isinstance(inst, LocalProxy):
        return inst.__dict__.get('task_params').get('mobileType')
    else:
        return inst.task_params.get("mobileType")


async def simple_log(spider_inst, status_code=None, **kwargs):
    _final_code(spider_inst, status_code)
    await log(spider_inst.token, status_code=status_code, cls=get_spider_name(spider_inst),
              Area=spider_inst.task_params['province'], task_params=spider_inst.task_params,
              **kwargs)


def _final_code(spider_inst, status_code):
    if status_code not in [diy.DIY_STATUS.value, diy.STATISTICS_STATUS.value]:
        spider_inst.final_code = status_code


# 记录日志信息
async def log(token, status_code=None, cls=None, iselk=True, **kwargs):
    """
    日志 输出路径分三类
    1. redis_status (有status_code， 但不包含code为10086的信息)
    2. redis_log (所有信息 但不包含code为10086的信息)
    3. elk （所有信息）



    :param token:
    :param status_code:
    :param cls:
    :param kwargs:
    :return:
    """
    try:
        logger = logging.getLogger(cls)
        status_msg = REQUEST_TASK_STATUS_CODE.get(status_code)
        elk_fmt = dict(machine_id=IP, token=token, sys_code=kwargs.get('sys_code') or '',
                       event_time=time.strftime('%Y-%m-%d %H:%M:%S'), timestamp=time_stamp(),
                       msg_type=kwargs.get('msg_type') or '',
                       err_type=kwargs.get('err_type') or '',
                       message=kwargs.get('message') or status_msg or '',
                       ex_message=kwargs.get('ex_message') or '',
                       out_message=kwargs.get('out_message') or '',
                       # Area=kwargs.get('area') or '',
                       channel_id=kwargs.get('channel_id') or '',
                       province=kwargs.get('area') or '',
                       telephone=kwargs.get('telephone') or '',
                       company_name=kwargs.get('company_name') or '',
                       id=kwargs.get('id') or '',
                       identity=kwargs.get('identity') or ''
                       )
        if kwargs.get('task_params'):
            elk_fmt.update(channel_id=kwargs.get('task_params').get('channel_id', ''),
                           telephone=kwargs.get('task_params').get('telephone', ''),
                           verify_result=kwargs.get('task_params').get('verify_result', ''),
                           company_name=kwargs.get('task_params').get('company_name', ''),
                           id=kwargs.get('task_params').get('id', ''),
                           identity=kwargs.get('task_params').get('identity', ''),
                           province=kwargs.get('task_params').get('province', ''), )
        if status_code is not None:
            elk_fmt.update(reason_code=status_code)
            if status_code not in [diy.DIY_STATUS.value, '200']:
                key_prefix = config.get('MOBILE_STATUS')
                await rc.save_status(f'{key_prefix}{token}', f'{token}_{status_msg}_{status_code}',
                                     config.STATUS_KEY_EXPIRE)
        if (status_code is None) or (status_code not in [diy.DIY_STATUS.value]):
            if elk_fmt.get('out_message').strip():
                elk_fmt['message'] = status_msg or elk_fmt['out_message']
                await rc.zrem_certain_task(
                    f'{kwargs.get("Area")}:{elk_fmt.get("channel_id")}:{token}:{elk_fmt.get("telephone")}:{elk_fmt.get("company_name")}:{elk_fmt.get("verify_result")}:{elk_fmt.get("id")}')
            await rc.lpush(f"{config.TAX_CRAWL}:{token}", json.dumps(elk_fmt))
        if iselk:
            await add_elk(token, elk_fmt, index=config.ELK_INDEX, doc_type='doc')
        if config.get('PROFILE_ACTIVE') in ['prod']:
            logger.info(str(elk_fmt))

        else:
            logger.info(str(elk_fmt))

        if status_code in ['110', '111', '112']:
            await rc.zadd_task(
                member='{}:{}:{}:{}:{}:{}:{}'.format(kwargs.get('Area'), elk_fmt.get('channel_id'),
                                                     token, elk_fmt.get('telephone'), elk_fmt.get('company_name'),
                                                     elk_fmt.get('verify_result'), elk_fmt.get('id')))
        if status_code == '100':
            await rc.zrem_certain_task(
                f'{kwargs.get("Area")}:{elk_fmt.get("channel_id")}:{token}:{elk_fmt.get("telephone")}:{elk_fmt.get("company_name")}:{elk_fmt.get("verify_result")}:{elk_fmt.get("id")}')
    except:
        import traceback
        # print(traceback.format_exc())


async def add_elk(token, date_item, index=config.ELK_INDEX, doc_type='dataitem'):
    try:
        date_item.update(
            {'@timestamp': (datetime.datetime.now() + relativedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S.000Z')})
        async with Elasticsearch(
                [{'host': config.ELK_HOST, 'port': config.ELK_PORT,
                  'http_auth': (config[ELK.USR.value], config[ELK.PWD.value]),
                  "timeout": 360000}]) as es_client:
            await es_client.index(index=index, body=date_item, doc_type=doc_type)
    except:
        import traceback
        print(traceback.format_exc())
        await log(token, status_code=diy.DIY_STATUS.value, message=f'存入elk报错', iselk=False)


def get_js_ctx(file_name):
    js_dir = os.path.join(get_root_path(__name__), 'encrypt_file', file_name)
    jsstr = file_reader(js_dir)
    ctx = execjs.compile(jsstr)
    return ctx


# xx时xx分xx秒
def str_to_secs(src):
    if re.match(r'\d+时\d+分\d+秒', src):
        mdict = re.match(r'^(?P<h>[^ ]*)时(?P<m>[^ ]*)分(?P<s>[^ ]*)秒', src).groupdict()
        return str(int(mdict.get('h')) * 3600 + int(mdict.get('m')) * 60 + int(mdict.get('s')))
    if re.match(r'\d+小时\d+分\d+秒', src):
        mdict = re.match(r'^(?P<h>[^ ]*)小时(?P<m>[^ ]*)分(?P<s>[^ ]*)秒', src).groupdict()
        return str(int(mdict.get('h')) * 3600 + int(mdict.get('m')) * 60 + int(mdict.get('s')))
    if re.match(r'\d+分\d+秒', src):
        mdict = re.match(r'^(?P<m>[^ ]*)分(?P<s>[^ ]*)秒', src).groupdict()
        return str(int(mdict.get('m')) * 60 + int(mdict.get('s')))
    if re.match(r'\d+秒', src):
        mdict = re.match(r'^(?P<s>[^ ]*)秒', src).groupdict()
        return str(int(mdict.get('s')))
    if re.match(r'\d+分', src):
        mdict = re.match(r'^(?P<m>[^ ]*)分', src).groupdict()
        return str(int(mdict.get('m')) * 60)


# xx:xx:xx
def str_to_secs2(src):
    mdict = re.match(r'^(?P<h>[^ ]*):(?P<m>[^ ]*):(?P<s>[^ ]*)', src).groupdict()
    return str(int(mdict.get('h')) * 3600 + int(mdict.get('m')) * 60 + int(mdict.get('s')))


# xx'xx'xx
def str_to_secs3(src):
    mdict = re.match(r"^(?P<h>[^ ]*)\'(?P<m>[^ ]*)\'(?P<s>[^ ]*)", src).groupdict()
    return str(int(mdict.get('h')) * 3600 + int(mdict.get('m')) * 60 + int(mdict.get('s')))


def date_format(src, format='%Y-%m-%d'):
    if re.match(r'\d+年\d+月\d+日', src):
        mdict = re.match(r'^(?P<y>[^ ]*)年(?P<m>[^ ]*)月(?P<d>[^ ]*)日', src).groupdict()
        d = datetime.date(int(mdict.get('y')), int(mdict.get('m')), int(mdict.get('d')))
        return d.strftime(format)


def date_range(bDate='201001', eDate=None):
    beginDate = datetime.date(int(bDate[:4]), int(bDate[4:6]), 1)
    if eDate is None:
        endDate = datetime.datetime.now().date()
    else:
        endDate = datetime.date(int(eDate[:4]), int(eDate[4:6]), 1)
    dates = [bDate]
    while beginDate < endDate:
        beginDate = beginDate + relativedelta(months=1)
        date = beginDate.strftime("%Y%m")
        dates.append(date)
    return dates


def compute_month(init_date=None, months=0, days=0, format='%Y%m'):
    dt = datetime.datetime.now()
    if init_date is not None:
        if len(init_date) == 6:
            dt = datetime.date(int(init_date[:4]), int(init_date[4:6]), 1)
        if len(init_date) == 8:
            dt = datetime.date(int(init_date[:4]), int(init_date[4:6]), int(init_date[6:8]))
    result = dt + relativedelta(months=months + 1, days=days)
    return result.strftime(format)


def get_year_lst(from_year: int) -> list:
    return [(from_year + diff) for diff in range(datetime.datetime.now().year - from_year + 1)]


def get_jquery_json(src, prefix='jQuery'):
    if prefix in src:
        content = re.compile(f'{prefix}\d+_\d+\((.*)\)').findall(src)[0]
        return json.loads(content)
    return src


def get_enum_value_by_inst(inst: Enum, clz: enum.EnumMeta) -> str:
    if isinstance(inst, str):
        return inst
    elif isinstance(inst, clz):
        for name, member in clz.__members__.items():
            if member == inst:
                return member.value


def traceback_printer(original_function):
    @wraps(original_function)
    def wrapped(*args, **kwargs):
        x = original_function(*args, **kwargs)
        return x

    return wrapped


def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


def date_range_category(start_date, end_date=datetime.datetime.now().strftime('%Y-%m-%d'), month=3,
                        out_fmt='%Y-%m-%d'):
    dt_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    dt_end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    date_range = relativedelta(months=month)
    start_dates = [dt_start.strftime(out_fmt)]
    end_dates = []
    today = dt_start
    while today <= dt_end:
        tomorrow = today + date_range
        if tomorrow.month != today.month and (tomorrow < dt_end):
            start_dates.append(tomorrow.strftime(out_fmt))
            end_dates.append((tomorrow + relativedelta(days=-1)).strftime(out_fmt))
        today = tomorrow
    end_dates.append(dt_end.strftime(out_fmt))
    return list(zip(start_dates, end_dates))


def parse_to_html(str):
    return str.replace("&quot;", "\"").replace("&amp;", "&").replace("&gt;", ">").replace("&prime;", "'").replace(
        "&lt;", "<")


def json_data_mapper(src: json, cls):
    inst = cls()
    for attr in src.keys():
        setattr(inst, attr, src.get(attr))
    return inst


def get_entity_lst(inst):
    lst = [name[1] for name in inspect.getmembers(inst) if
           isinstance(name[1], list) and (not inspect.isbuiltin(name[1]))]
    if len(lst):
        return lst[0]
    return []


def filter_list_field(doc: Document) -> dict:
    list_field = next(filter(lambda x: isinstance(getattr(doc, x), list), dir(doc)), None)
    if list_field is not None:
        list_len = len(getattr(doc, list_field))
        return {list_field: list_len}


def cls_decorator(func=None):
    """
    类装饰器 为类所有的方法添加 func 装饰器
    :param func: 方法装饰器
    :return:
    """

    def wrapped(Cls):
        class NewClass(object):
            def __init__(self, *args, **kwargs):
                self.oInstance = Cls(*args, **kwargs)

            def __getattribute__(self, s):
                try:
                    x = super(NewClass, self).__getattribute__(s)
                except AttributeError:
                    pass
                else:
                    return x
                x = self.oInstance.__getattribute__(s)
                if type(x) == type(self.__init__):
                    return func(x)
                else:
                    return x

        return NewClass

    return wrapped


def Time_Comparison(date_obj):
    """
    比较当前日期的前半年与真实数据日期比较
    :param date_obj:
    :return:
    """
    date_obj = str(date_obj).strip().split(" ")[0]
    # print(date_obj)
    today = datetime.date.today()
    # print(today)  # 2019-10-29
    vaildDate = str(today - relativedelta(months=6))
    # print(vaildDate)  # 2019-04-29
    testDate = datetime.datetime.strptime(date_obj, "%Y-%m-%d")
    strtime = datetime.datetime.strptime(vaildDate, "%Y-%m-%d")
    # print(testDate > strtime)
    if testDate > strtime:
        # 说明该日期在半年以内
        return True
    else:
        # 说明该日期在半年以外，违法违章的状态要改变
        return False


from Crypto.Cipher import AES
import base64
import requests
from retrying import retry

requests.packages.urllib3.disable_warnings()

qxb_api_map = {
    "0": "https://dcgapp.dachagui.com/api/company/searchcpinfo",  # 正式 查询企业基本信息
    "1": "https://dcgapp.dachagui.com/api/company/stockerholder",  # 正式 股东信息接口
}


class Enterprise_api:
    """ 启信宝-企业信息明细 """

    def __init__(self, tv):
        self.url = qxb_api_map.get(tv, "")
        self.key = b'13gxdszbuty4ifq7'
        self.iv = b'gtmvduiebfz52q39'
        self.mode = AES.MODE_CFB
        self.client = '120'

    def encrypt(self, text, key, iv):
        cryptor = AES.new(key, self.mode, iv, segment_size=128)
        ciphertext = cryptor.encrypt(text)
        return base64.b64encode(ciphertext)

    def getTimeStamp(self):
        time_url = 'https://dcgapp.dachagui.com/version.php'
        qxb_time = requests.get(url=time_url, verify=False)
        qxb_time = json.loads(qxb_time.text)
        qxb_timestamp = qxb_time['data']['timestamp']
        return qxb_timestamp

    @retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=3000)
    def _request(self, data_str):
        """  请求  """
        headers = {'client': self.client}
        res = requests.post(url=self.url, data=data_str, headers=headers, verify=False, timeout=10)
        return res

    def getDetailByName(self, keyword):
        """
        :param keyword: 公司名称/税号/组织机构代码
        :return: 企业基本详情信息
        """
        try:
            qxb_timestamp = self.getTimeStamp()
            data = {
                'keyword': keyword,
                'timestamp': qxb_timestamp,
                # 'id_search':1
            }
            data = json.dumps(data)
            data = bytes(data, encoding='utf-8')
            data_str = self.encrypt(data, self.key, self.iv)  # 加密
            res = self._request(data_str)
            result = res.json()

            result['data'] = {k: v if v != '-' else '' for k, v in result['data'].items()}

            return result
        except:
            result = {'code': 909, 'msg': '查询无结果', 'data': []}
            return result

    def getStockerholderByName(self, companyName):
        """
        :param companyName:
        :return: 股东信息
        """
        try:
            qxb_timestamp = self.getTimeStamp()
            data = {
                'keyword': companyName,
                'timestamp': qxb_timestamp
            }
            data = json.dumps(data)
            data = bytes(data, encoding='utf-8')
            data_str = self.encrypt(data, self.key, self.iv)  # 加密
            # res = requests.post(url=self.url,data=data_str,headers=headers,timeout=5,verify=False)
            res = self._request(data_str)
            result = res.json()
            if result['code'] == 200:
                return result['data']['stocker']
            else:
                print(result['msg'])
                return {}
        except:
            print(traceback.format_exc())
            print("股东信息异常")
            return {}


if __name__ == '__main__':
    ret = Rsa_bcii(text='13652348193',
                   pk='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCBt2np4cyi9q+xyp/0is+Fu4Y7LRzV84bivHzIAlKPG6h5WpMC7qUEC8HNocVwGqQ6HUSMSD1/bHme90c4rUsZvXPNXRA6VVMHj84cUmzUbErxQ+3qK5rFALLG+mSfJCghaWK8gwiphS5fVFWroxvreZb309NWthtluOh7uitnLQIDAQAB').rsa_encrypt()
    print(ret)
