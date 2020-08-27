import logging
import time
import asyncio
import hashlib
import aiohttp
import concurrent

from http_utils.http_response import HtmlResponse
from core._global import current_app
from core.consistant import *
from core.exceptions import *

from core.core_utils import simple_log

import base64
import re


async def ret_handler(url, resp, response, encoding):
    return HtmlResponse(url=url, headers=resp.headers, body=response, encoding=encoding, status=resp.status)


def construct_dateitem(spider, content, url, params="", datatype='empty'):
    ts = int(round(time.time() * 1000))
    mobile = spider.task_params['UserName']
    md5 = hashlib.md5()
    md5.update(str(ts).encode('utf-8'))
    data_item = {
        "token": spider.token,
        "content": content,
        "datatype": datatype,
        "timestamp": ts,
        "mobile": mobile,
        "url": url
    }
    return data_item


async def elk_handler(resp, response, encoding=""):
    _log = ""
    if "content-type" in resp.headers:
        if (
                "image/" in resp.headers["content-type"] or
                "ms-excel" in resp.headers["content-type"] or
                "x-xls" in resp.headers["content-type"] or
                "pdf" in resp.headers["content-type"]
        ):
            _log = str(base64.b64encode(response), "utf-8")
        elif re.search("charset=(.*?)$", resp.headers["content-type"]):
            enc = re.search("charset=(.*?)$", resp.headers["content-type"]).group(1)
            if "gb2312" in enc.lower():
                encoding = "gb2312"
            elif "gbk" in enc.lower():
                encoding = "gbk"
            _log = response.decode(encoding, 'ignore')
    if not _log:
        _log = response.decode(encoding, 'ignore')
    return _log


async def request(url, spider, session, method, result_type='text', result_code_pool=[200, 201, 202], data=None,
                  params=None,
                  allow_redirects=True, encoding='utf-8', datatype="empty", is_header=True, verify_ssl=False, **kwargs):
    try:
        async with session.request(url=url, method=method, headers=spider.headers if is_header else {},
                                   proxy=spider.proxy if url != current_app.config[
                                       RequestConfig.ADSL_URL.value] else None, data=data,
                                   verify_ssl=verify_ssl,
                                   params=params, allow_redirects=allow_redirects, **kwargs) as resp:
            response = await resp.read()
            # await add_elk(spider.token,
            #               construct_dateitem(spider, await elk_handler(resp, response, encoding), url, data, datatype))
            if resp.status in result_code_pool:
                if spider.proxy is not None and (url != current_app.config[RequestConfig.ADSL_URL.value]) and (
                        spider._proxy_retry != 0):
                    spider._proxy_retry = 0
                return await ret_handler(url, resp, response, encoding)
            elif spider._proxy_retry > 0:
                await spider.get_proxy()
                return await request(url, spider, session, method, result_type=result_type,
                                     result_code_pool=result_code_pool,
                                     data=data, params=params,
                                     allow_redirects=allow_redirects, encoding=encoding, datatype=datatype, **kwargs)
            else:
                await simple_log(spider, SPECIAL_STATUS.DIY_STATUS.value,
                                 message=f'Error response_url: {url}   status_code: {resp.status} proxy: {spider.proxy} params: {params} data: {data}')
                raise WebSiteException()
    except (aiohttp.client_exceptions.ClientOSError, concurrent.futures._base.TimeoutError,aiohttp.client_exceptions.TooManyRedirects,
            aiohttp.client_exceptions.ServerDisconnectedError) as e:
        import traceback
        if spider.request_retry > 0:
            await simple_log(spider, SPECIAL_STATUS.DIY_STATUS.value,
                             message=f'Request url: {url} Error {str(traceback.format_exc())} And Start to retry')
            spider.request_retry -= 1
            return await request(url, spider, session, method, result_type=result_type,
                                 result_code_pool=result_code_pool,
                                 data=data, params=params,
                                 allow_redirects=allow_redirects, encoding=encoding, datatype=datatype,
                                 **kwargs)
        else:
            raise WebSiteException(description=f'url: {url} exec: {str(e)}')
    except (aiohttp.client_exceptions.ClientProxyConnectionError, aiohttp.client_exceptions.ClientHttpProxyError) as e:
        if spider.proxy_dynamic:
            await simple_log(spider, SPECIAL_STATUS.DIY_STATUS.value,
                             message=f'Request Error {str(traceback.format_exc())} And Start to retry')
            await spider.get_proxy()
            return await request(url, spider, session, method, result_type=result_type,
                                 result_code_pool=result_code_pool,
                                 data=data, params=params,
                                 allow_redirects=allow_redirects, encoding=encoding, datatype=datatype,
                                 **kwargs)
        else:
            raise WebSiteException(description=f'url: {url} exec: {str(e)}')
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise e


async def fetch(url, spider, session, params=None, **kwargs):
    return await request(url, spider, session, 'GET', params=params, **kwargs)


async def post(url, spider, session, params=None, data=None, **kwargs):
    return await request(url, spider, session, 'POST', params=params, data=data, **kwargs)
