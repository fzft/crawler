
from http.cookies import SimpleCookie
from core.core_utils import *

import re
import execjs
import sys,os
import aiohttp
import asyncio
import hashlib
from utils.chen.DateTime import *
from utils.chen.TimeSpan import *
from utils.chen.ExObject import *
from core.core_requests import *
from core.core_utils import *
from types import MethodType
class Convert(object):
    @staticmethod
    def ToInt32(value,defaultValue=0)->int:
        try:
            if value:
                return int(value)
            else:
                return defaultValue
        except:
            return defaultValue

    @staticmethod
    def ToFloat(value)->float:
        try:
            if value:
                return float(value)
            else:
                return 0
        except:
            return 0

    @staticmethod
    def ToDateTime(dateStr="",formatStr="")->DateTime:
        if len(formatStr)!=len(dateStr):
            raise Exception()
        _year=1970
        _month=1
        _day=1
        _hour=0
        _minute=0
        _second=0
        if "yyyy" in formatStr:
            pos=formatStr.index("yyyy")
            _year=int(dateStr[pos:pos+4])
        if "MM" in formatStr:
            pos=formatStr.index("MM")
            _month=int(dateStr[pos:pos+2])
        if "dd" in formatStr:
            pos=formatStr.index("dd")
            _day=int(dateStr[pos:pos+2])
        if "HH" in formatStr:
            pos=formatStr.index("HH")
            _hour=int(dateStr[pos:pos+2])
        if "hh" in formatStr:
            pos=formatStr.index("hh")
            _hour=int(dateStr[pos:pos+2])
        if "mm" in formatStr:
            pos=formatStr.index("mm")
            _minute=int(dateStr[pos:pos+2])
        if "ss" in formatStr:
            pos=formatStr.index("ss")
            _second=int(dateStr[pos:pos+2])
        return DateTime(_year,_month,_day,_hour,_minute,_second)

    @staticmethod
    def ToTimeSpan(dateStr="",formatStr="")->DateTime:
        if len(formatStr)!=len(dateStr):
            raise Exception()
        _day=0
        _hour=0
        _minute=0
        _second=0
        if "dd" in formatStr:
            pos=formatStr.index("dd")
            _day=int(dateStr[pos:pos+2])
        if "HH" in formatStr:
            pos=formatStr.index("HH")
            _hour=int(dateStr[pos:pos+2])
        if "hh" in formatStr:
            pos=formatStr.index("hh")
            _hour=int(dateStr[pos:pos+2])
        if "mm" in formatStr:
            pos=formatStr.index("mm")
            _minute=int(dateStr[pos:pos+2])
        if "ss" in formatStr:
            pos=formatStr.index("ss")
            _second=int(dateStr[pos:pos+2])
        return TimeSpan(_hour,_minute,_second,_day)
        
class Console(object):
    @staticmethod
    def WriteLine(str):
        print(str)

    @staticmethod
    def ReadLine():
        userIn = input()
        return userIn

class Logger(object):
    """Logger类"""
    token=""
    logText={}
    language=0#0=中文 1=英文 2=日文
    def __init__(self,_token,_spider):
        self.token=_token
        self.spider=_spider
        self.logText={}
        self.logText["login"]=["开始登陆","Start loggin.","ウェブサイトへのログインを開始"]
        self.logText["login_s"]=["登陆成功","Loggin success.","ウェブサイトはログインに成功しました"]
        self.logText["login_f"]=["登陆失败","Loggin failed.","ウェブサイトはログインに失敗しました"]
        self.logText["basic"]=["开始抓取基本信息","Start crawling basic info.","基本情報のクロールを開始"]
        self.logText["busi"]=["开始抓取业务信息","Start crawling business info.","ビジネス情報のクロールを開始"]
        self.logText["recharge"]=["正在抓取{}充值记录","Start crawling {} recharge records.","{}アカウントのリチャージ履歴を取得する"]
        self.logText["call"]=["正在抓取{}通话详单","Start crawling {} call records.","{}通話の詳細を取得する"]
        self.logText["call_s"]=["抓取{}通话详单成功","{} call records success.","{}通話リストの取得に成功しました"]
        self.logText["call_f"]=["抓取{}通话详单失败","{} call records failed.","{}通話リストの取得に失敗しました"]
        self.logText["sms"]=["正在抓取{}短信详单","Start crawling {} sms records.","{}のSMSリストを把握する"]
        self.logText["sms_s"]=["抓取{}短信详单成功","{} sms records success.","{} SMS詳細の取得に成功しました"]
        self.logText["sms_f"]=["抓取{}短信详单失败","{} sms records failed.","{} SMS詳細の取得に失敗しました"]
        self.logText["bill"]=["正在抓取{}账单","Start crawling {} bill records.","{}モバイル請求書を入手する"]
        self.logText["bill_s"]=["抓取{}账单成功","{} bill records success.","{}モバイル請求書の取得に成功しました"]
        self.logText["bill_f"]=["抓取{}账单失败","{} bill records failed.","{}モバイル請求書の取得に失敗しました"]
        self.logText["address"]=["开始抓取收获地址","Start crawling user address","収穫先住所のクロールを開始"]
        self.logText["alipay"]=["开始抓取支付宝信息","Start crawling Alipay Information","Alipayの情報を入手し始める"]
        self.logText["order"]=["开始抓取订单信息","Start crawling order information","発注情報の取得を開始"]
        
    def Write(self,msg):
        print(msg)

    async def AWrite(self,msg):
        print(msg)
        await simple_log(self.spider,message=msg)

    async def SendSms(self):
        await simple_log(self.spider, '0001')

    async def CheckSms(self):
        await simple_log(self.spider, '0100')

    async def WriteElk(self,msg,url="",datatype=""):
        await add_elk(self.spider,  construct_dateitem(self.spider, msg, url, "", datatype))

    #region 日志打印
    async def StartLogin(self):
        await self.AWrite(self.logText["login"][self.language])

    async def LoginSuccess(self):
        await self.AWrite(self.logText["login_s"][self.language])

    async def LoginFailed(self):
        await self.AWrite(self.logText["login_f"][self.language])

    async def StartBasicInfo(self):
        await self.AWrite(self.logText["basic"][self.language])

    async def StartBusiness(self):
        await self.AWrite(self.logText["busi"][self.language])
    
    async def StartRecharge(self,month:DateTime=None):
        if month:
            await self.AWrite(self.logText["recharge"][self.language].format(month.ToString("yyyyMM")))
        else:
            await self.AWrite(self.logText["recharge"][self.language].format(""))

    async def StartCall(self,month:DateTime=None):
        if month:
            await self.AWrite(self.logText["call"][self.language].format(month.ToString("yyyyMM")))
        else:
            await self.AWrite(self.logText["call"][self.language].format(""))

    async def CallSuccess(self,month:DateTime):
        await self.AWrite(self.logText["call_s"][self.language].format(month.ToString("yyyyMM")))

    async def CallFailed(self,month:DateTime):
        await self.AWrite(self.logText["call_f"][self.language].format(month.ToString("yyyyMM")))

    async def StartSms(self,month:DateTime):
        await self.AWrite(self.logText["sms"][self.language].format(month.ToString("yyyyMM")))

    async def SmsSuccess(self,month:DateTime):
        await self.AWrite(self.logText["sms_s"][self.language].format(month.ToString("yyyyMM")))
        
    async def SmsFailed(self,month:DateTime):
        await self.AWrite(self.logText["sms_f"][self.language].format(month.ToString("yyyyMM")))

    async def StartBill(self,month:DateTime=None):
        if month:
            await self.AWrite(self.logText["bill"][self.language].format(month.ToString("yyyyMM")))
        else:
            await self.AWrite(self.logText["bill"][self.language].format(""))

    async def StartAddress(self):
        await self.AWrite(self.logText["address"][self.language])

    async def StartAlipay(self):
        await self.AWrite(self.logText["alipay"][self.language])

    async def StartOrder(self):
        await self.AWrite(self.logText["order"][self.language])
    #endregion

def GetRunPath():
    """获得脚本执行目录"""
    return os.getcwd()

def GetMd5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

def GetJs(fileName):
    """通过execjs模块获得Js对象"""
    path=os.path.join(GetRunPath(),"core","encrypt_file",fileName)
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    jsstr = ''
    while line:
        jsstr = jsstr + line
        line = f.readline()
    f.close()
    if(jsstr[0:1]=='\ufeff'):
        jsstr=jsstr[1:]
    ctx = execjs.compile(jsstr)
    return ctx

def GetTestFile(fileName):
    """获得测试文件"""
    path=os.path.join(GetRunPath(),"testData",fileName)
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    jsstr = ''
    while line:
        jsstr = jsstr + line
        line = f.readline()
    f.close()
    if(jsstr[0:1]=='\ufeff'):
        jsstr=jsstr[1:]
    return jsstr

def GetTestFileByte(fileName):
    """获得测试文件"""
    path=os.path.join(GetRunPath(),"testData",fileName)
    f = open(path, 'rb').read()
    return f
    
def SetTestFile(fileName,Content):
    path=os.path.join(GetRunPath(),"testData",fileName)
    pass

def CleanDateTime(str):
    """
    字符串转DateTime对象
    """
    if not str:
        return DateTime()
    #region 包含完整时间
    r=re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",str)
    if r:
        _dt="{}-{}-{} {}:{}:{}".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            ,r.group(4).zfill(2)
            ,r.group(5).zfill(2)
            ,r.group(6).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})\\/([0-9]{1,2})\\/([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",str)
    if r:
        _dt="{}-{}-{} {}:{}:{}".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            ,r.group(4).zfill(2)
            ,r.group(5).zfill(2)
            ,r.group(6).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日 (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",str)
    if r:
        _dt="{}-{}-{} {}:{}:{}".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            ,r.group(4).zfill(2)
            ,r.group(5).zfill(2)
            ,r.group(6).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})([0-9]{1,2})([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",str)
    if r:
        _dt="{}-{}-{} {}:{}:{}".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            ,r.group(4).zfill(2)
            ,r.group(5).zfill(2)
            ,r.group(6).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([1-2][0-9]{3})([0-1][0-9])([0-3][0-9])([0-2][0-9])([0-5][0-9])([0-5][0-9])",str)
    if r:
        _dt="{}-{}-{} {}:{}:{}".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            ,r.group(4).zfill(2)
            ,r.group(5).zfill(2)
            ,r.group(6).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    #endregion

    #region 只包含年月日
    r=re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2})",str)
    if r:
        _dt="{}-{}-{} 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})\\/([0-9]{1,2})\\/([0-9]{1,2})",str)
    if r:
        _dt="{}-{}-{} 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日",str)
    if r:
        _dt="{}-{}-{} 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([1-2][0-9]{3})([0-1][0-9])([0-3][0-9])",str)
    if r:
        _dt="{}-{}-{} 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    #endregion

    #region 只包含年月
    r=re.search("([0-9]{4})\\-([0-9]{1,2})",str)
    if r:
        _dt="{}-{}-01 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})\\/([0-9]{1,2})",str)
    if r:
        _dt="{}-{}-01 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([0-9]{4})年([0-9]{1,2})月",str)
    if r:
        _dt="{}-{}-01 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    r=re.search("([1-2][0-9]{3})([0-1][0-9])",str)
    if r:
        _dt="{}-{}-01 00:00:00".format(
            r.group(1)
            ,r.group(2).zfill(2)
            )
        return Convert.ToDateTime(_dt,"yyyy-MM-dd HH:mm:ss")
    #endregion

def CleanTimeSpan(str):
    if not str:
        return TimeSpan(0,0,0)
    #region 时分秒
    r=re.search("(\\d{1,2}):(\\d{1,2}):(\\d{1,2})",str)
    if r:
        _dt="{}:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d{1,2})时(\\d{1,2})分(\\d{1,2})秒",str)
    if r:
        _dt="{}:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d{1,2})小时(\\d{1,2})分(\\d{1,2})秒",str)
    if r:
        _dt="{}:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d{1,2})小时(\\d{1,2})分钟(\\d{1,2})秒",str)
    if r:
        _dt="{}:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            ,r.group(3).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")

    #endregion

    #region 分秒
    r=re.search("(\\d{1,2}):(\\d{1,2})",str)
    if r:
        _dt="00:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d{1,2})分(\\d{1,2})秒",str)
    if r:
        _dt="00:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d{1,2})分钟(\\d{1,2})秒",str)
    if r:
        _dt="00:{}:{}".format(
            r.group(1).zfill(2)
            ,r.group(2).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d+):(\\d{1,2})",str)
    if r:
        m=int(r.group(1))
        s=int(r.group(2))
        return TimeSpan(0,m,s)
    #endregion
    #region 只有秒
    r=re.search("(\\d{1,2})秒",str)
    if r:
        _dt="00:00:{}".format(
            r.group(1).zfill(2)
            )
        return Convert.ToTimeSpan(_dt,"HH:mm:ss")
    r=re.search("(\\d{3,4,5,6,7,8,9,10})秒",str)
    if r:
        return TimeSpan(second=int(r.group(1)))
    #endregion

    #region 单独情况判断
    hint=0
    mint=0
    sint=0
    h=re.search("(\\d+)(时|小时)",str)
    if h:
        hint=int(h.group(1))
    m=re.search("(\\d+)(分|分钟)",str)
    if m:
        mint=int(m.group(1))
    s=re.search("(\\d+)(秒|分钟)",str)
    if s:
        sint=int(s.group(1))
    return TimeSpan(hint,mint,sint)
    #endregion

def GetTimeStamp():
    return str(int(round(time.time()) * 1000))

def SetCookie(cookieJar,key,value,path="/",domain=None):
    """添加一个COOKIE"""
    addCookie=SimpleCookie()
    addCookie[key]=value
    if domain:
        addCookie[key]["domain"]=domain
    addCookie[key]["path"]="/"
    cookieJar.update_cookies(addCookie)
    return cookieJar

def ClearCookieDomain(cookieJar):
    _c=[]
    for cookie in cookieJar:
        _c.append({"key":cookie.key,"value":cookie.value})
    for _item in _c:
        SetCookie(cookieJar,_item["key"],_item["value"],"/","")

def GetCrawlMonth(crawlCount,add=0):
    """根据抓取COUNT获得抓取月份DateTime对象
    crawlCount=抓取Count
    add=偏移量
    """
    results=[]
    crawlCount=int(crawlCount)
    if (crawlCount > 0):
        crawlCount = -crawlCount
    crawlCount = crawlCount - add
    date=DateTime.Now()
    for i in range(0,crawlCount,-1):
        results.append(date.AddMonths(i))
    return results

def CFor(i,func1,func2,func3):
    while(func1(i)):
        func3(i)
        i=func2(i)

def setHeaders(self):
    if "user-agent" not in self.headers :
        self.headers['user-agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    if ("Content-Type" not in self.headers 
    and "content-Type" not in self.headers
    and "content-type" not in self.headers
    and "Content-type" not in self.headers):
        self.headers['Content-Type']="application/x-www-form-urlencoded"

async def GET(self, url,retryRegex=None,_maxRetryCount=5,_retrySleep=1,_retry=0,_encode="",datatype="empty", **kwargs)->str:
    setHeaders(self)
    try:
        async with aiohttp.ClientSession(
                cookie_jar=self.cookie_jar) as session:
            response = await fetch(url, self, session,datatype=datatype, **kwargs)
            byte=response.body
            if _encode=="image":
                return ""
            if _encode:
                text = byte.decode(_encode)
            elif "content-type" in response.headers:
                if "image" in response.headers["content-type"]:
                    return ""
                enc=ExObject.regex("charset=(.*?)$",response.headers["content-type"])["?0"].ToString()
                if enc:
                    text = byte.decode(enc)
                else:
                    text = byte.decode("utf-8")
            else:
                text = byte.decode("utf-8")
            if retryRegex and _retry<_maxRetryCount:
                if re.search(retryRegex,text):
                    await asyncio.sleep(_retrySleep)
                    return await GET(self,url,retryRegex,_maxRetryCount,_retrySleep,_retry+1,_encode,**kwargs)
                else:
                    return text
            else:
                return text
    except Exception as e:
        if _retry<_maxRetryCount:
            await asyncio.sleep(_retrySleep)
            return await GET(self,url,retryRegex,_maxRetryCount,_retrySleep,_retry+1,_encode,**kwargs)
        else:
            await simple_log(self,message=str(e))
            return "timeout"

async def GETByte(self, _url,datatype="empty", **kwargs):
    setHeaders(self)
    try:
        async with aiohttp.ClientSession(
                cookie_jar=self.cookie_jar) as session:
            response = await fetch(_url, self, session,datatype=datatype, **kwargs)
            return response.body
    except Exception as e:
        await simple_log(self,message=str(e))
        return "timeout"

async def GETResp(self, _url,datatype="empty",_maxRetryCount=5,_retrySleep=1,_retry=0, **kwargs):
    setHeaders(self)
    try:
        async with aiohttp.ClientSession(
                cookie_jar=self.cookie_jar) as session:
            response = await fetch(_url, self, session,datatype=datatype, **kwargs)
            return response
    except Exception as e:
        if _retry<_maxRetryCount:
            await asyncio.sleep(_retrySleep)
            return await GETResp(self,_url,datatype,_maxRetryCount,_retrySleep,_retry+1,**kwargs)
        else:
            await simple_log(self,message=str(e))
            return "timeout"

async def POST(self, url, param,_encode="",retryRegex=None,datatype="empty",_maxRetryCount=5,_retrySleep=1,_retry=0, **kwargs)->str:
    setHeaders(self)
    try:
        async with aiohttp.ClientSession(
                cookie_jar=self.cookie_jar) as session:
            response = await post(url, self, session, data=param,datatype=datatype, **kwargs)
            body=response.body
            if _encode:
                text = body.decode(_encode)
            elif "content-type" in response.headers:
                enc=ExObject.regex("charset=(.*?)$",response.headers["content-type"])["?0"].ToString()
                if enc:
                    text = body.decode(enc)
                else:
                    text = body.decode("utf-8")
            else:
                text = body.decode("utf-8")
            if retryRegex and _retry<_maxRetryCount:
                if re.search(retryRegex,text):
                    await asyncio.sleep(_retrySleep)
                    return await POST(self,url,param,_encode,retryRegex,datatype,_maxRetryCount,_retrySleep,_retry+1,**kwargs)
                else:
                    return text
            else:
                return text
    except Exception as e:
        if _retry<_maxRetryCount:
            await asyncio.sleep(_retrySleep)
            return await POST(self,url,param,_encode,retryRegex,datatype,_maxRetryCount,_retrySleep,_retry+1,**kwargs)
        else:
            await simple_log(self,message=str(e))
            return "timeout"

async def POSTResp(self, url, param,datatype="empty",_maxRetryCount=5,_retrySleep=1,_retry=0, **kwargs):
    setHeaders(self)
    try:
        async with aiohttp.ClientSession(
                cookie_jar=self.cookie_jar) as session:
            response = await post(url, self, session, data=param,datatype=datatype, **kwargs)
            return response
    except Exception as e:
        if _retry<_maxRetryCount:
            await asyncio.sleep(_retrySleep)
            return await POSTResp(self,url,param,datatype,_maxRetryCount,_retrySleep,_retry+1,**kwargs)
        else:
            await simple_log(self,message=str(e))
            return "timeout"

def createAttrFromMeta(crawl):
    """
    从_meta中动态创建类内部属性
    """
    for k in crawl._meta.keys():
        if k not in ["realname","recharge","request_retry",
        "server_host","session","sms","start_url","stati","tFillIdentityCard","tFillRealName","tPassWord","tSmsValue",
        "tUserName","task","task_data_cls","task_params","token","_headers","_meta","_proxy_retry","phase"]:
            crawl.__setattr__(k,crawl._meta[k])
    crawl.tUserName=crawl.task_params["UserName"]
    crawl.tPassWord=crawl.task_params["Password"]
    if "FillIdentityCard" in crawl.task_params:
        crawl.tFillIdentityCard=crawl.task_params["FillIdentityCard"]
    else:
        crawl.tFillIdentityCard=""
    if "FillRealName" in crawl.task_params:
        crawl.tFillRealName=crawl.task_params["FillRealName"]
    else:
        crawl.tFillRealName=""
    if "smsvalue" in crawl.task_params:
        crawl.tSmsValue=crawl.task_params["smsvalue"]
    else:
        crawl.tSmsValue=""

def debug_SmsCode(crawl):
    if not crawl.debugMode:
        return
    userIn = input("输入短信验证码:")
    import redis
    import json
    import random
    from core.config import Config
    root_path = get_root_path(__name__)
    cfg = Config(root_path)
    conn = redis.Redis(
        host=cfg.get('REDIS_HOST'),
        port=cfg.get('REDIS_PORT'),
        db=cfg.get('REDIS_DB'))
    #data = dict(smsvalue=userIn, token=self.token)
    crawl.task["smsvalue"]=userIn
    key="sy_request_{}".format(crawl.token)
    value="动态密码_{}".format(userIn)
    conn.lpush(key,value)
    #conn.lpush('captcha:queue', json.dumps(self.task))



class dynamicMeta():
    def __init__(self, *args, **kwargs):
        self.tUserName=""
        self.tPassWord=""
        self.tFillIdentityCard=""
        self.tFillRealName=""
        self.tSmsValue=""
    def __setattr__(self, name, value):
        if name in ["realname","recharge","request_retry",
        "server_host","session","sms","start_url","stati","tFillIdentityCard","tFillRealName","tPassWord","tSmsValue",
        "tUserName","task","task_data_cls","task_params","token","_headers","_meta","_proxy_retry","phase"]:
            return super().__setattr__(name, value)
        if "_meta" in self.__dict__:
            if name not in self.__dict__["_meta"]:
                if (type(value) is str or
                    type(value) is int or
                    type(value) is bool or
                    type(value) is float):
                    self.__dict__["_meta"][name]=value
        return super().__setattr__(name, value)