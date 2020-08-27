from utils.chen.chenUtils import *
from utils.chen.ExObject import *
class CefAdapt():
    def __init__(self,spider, *args, **kwargs):
        self.spider=spider
        hosts=current_app.config['CEF_ADAPT_HOSTS']
        self.host=hosts[0]
    pass

    async def loadUrl(self,url,cookies=None,setCookieUrl=None):
        """
        访问一个URL
        url:访问的地址
        cookies:绑定的cookie
        setCookieUrl:cookie生效的url地址,完全形式 如:http://baidu.com
        """
        cefurl=self.host+"/TaskApi/action"
        _param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"loadurl",
            "param":url,
            "setCookie":None
        }
        if cookies:
            _param["setCookie"]=cookies
            _param["setCookieUrl"]=setCookieUrl
        result=await self.POST(cefurl,json.dumps(_param))
        return ExObject.loadJson(result)

    async def loadUrlWaitRender(self,url,query,cookies=None,setCookieUrl=None):
        """
        访问一个URL并等待渲染完成。
        url:访问的地址
        query:判断渲染完成条件的css选择器
        cookies:绑定的cookie
        setCookieUrl:cookie生效的url地址,完全形式 如:http://baidu.com
        """
        cefurl=self.host+"/TaskApi/action"
        _param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"loadurl_waitrender",
            "param":url+"@@"+query,
            "setCookie":None
        }
        if cookies:
            _param["setCookie"]=cookies
            _param["setCookieUrl"]=setCookieUrl
        result=await self.POST(cefurl,json.dumps(_param))
        return ExObject.loadJson(result)

    async def getHtml(self,cookies=None):
        cefurl=self.host+"/TaskApi/action"
        param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"html",
            "param":"",
            "setCookie":None
        }
        if cookies:
            param["setCookie"]=cookies
        result=await self.POST(cefurl,json.dumps(param))
        return ExObject.loadJson(result)

    async def getHtmlByQuery(self,query,cookies=None):
        cefurl=self.host+"/TaskApi/action"
        param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"query",
            "param":query,
            "setCookie":None
        }
        if cookies:
            param["setCookie"]=cookies
        result=await self.POST(cefurl,json.dumps(param))
        return ExObject.loadJson(result)
    
    async def runScript(self,script,cookies=None):
        """
        执行JS命令(从Console)
        script:脚本
        cookies:如果需要同时写入cookie
        """
        cefurl=self.host+"/TaskApi/action"
        param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"script",
            "param":script,
            "setCookie":None
        }
        if cookies:
            param["setCookie"]=cookies
        result=await self.POST(cefurl,json.dumps(param))
        return ExObject.loadJson(result)

    async def runScriptWaitRender(self,script,query,cookies=None):
        """
        执行JS命令(从Console)
        script:脚本
        cookies:如果需要同时写入cookie
        """
        cefurl=self.host+"/TaskApi/action"
        param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"script_waitrender",
            "param":script+"@@"+query,
            "setCookie":None
        }
        if cookies:
            param["setCookie"]=cookies
        result=await self.POST(cefurl,json.dumps(param))
        return ExObject.loadJson(result)


    async def loadUrlAndGetByQuery(self,url,query,cookies=None,setCookieUrl=None):
        """
        访问一个URL并等待渲染完成。
        url:访问的地址
        query:判断渲染完成条件的css选择器
        cookies:绑定的cookie
        setCookieUrl:cookie生效的url地址,完全形式 如:http://baidu.com
        """
        cefurl=self.host+"/TaskApi/action"
        _param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"loadurl_getbyquery",
            "param":url+"@@"+query,
            "setCookie":None
        }
        if cookies:
            _param["setCookie"]=cookies
            _param["setCookieUrl"]=setCookieUrl
        result=await self.POST(cefurl,json.dumps(_param))
        return ExObject.loadJson(result)

    async def regUrlMonitor(self,urlRule,mode)->str:
        """
        注册一个Url监视器。
        urlRule:监视URL规则
        mode:模式[contain,notcontain,equal,regex]
        return:监视器id->str
        """
        cefurl=self.host+"/TaskApi/reg"
        param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"seturlmon",
            "param":urlRule,
            "mode":mode
        }
        result=await self.POST(cefurl,json.dumps(param))
        return ExObject.loadJson(result)

    async def getUrlMonitorResult(self,urlMonitorId,mode="last"):
        """
        根据Url监视器ID获得拦截到的response
        urlMonitorId:monitor的ID
        mode:模式[first,last,all]
        return:{url,text}
        """
        cefurl=self.host+"/TaskApi/reg"
        param={
            "token":self.spider.token,
            "appKey":"tanzhi#1234",
            "action":"geturlmon",
            "param":urlMonitorId,
            "mode":mode
        }
        result=await self.POST(cefurl,json.dumps(param))
        return ExObject.loadJson(result)

    def construct_dateitem(self, content, url,param, datatype='cefAdapt'):
        ts = int(round(time.time() * 1000))
        content=content.decode("utf-8", 'ignore')
        mobile = self.spider.task_params['UserName']
        md5 = hashlib.md5()
        md5.update(str(ts).encode('utf-8'))
        data_item = {
            "token": self.spider.token,
            "content": "==================Request====================\r\n\r\n\r\n\r\n"+json.dumps(param)+"\r\n\r\n\r\n\r\n==================Content====================\r\n\r\n\r\n\r\n"+content,
            "datatype": datatype,
            "timestamp": ts,
            "mobile": mobile,
            "url": url
        }
        return data_item

    async def POST(self, url, param, **kwargs)->str:
        header={'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(url=url, method="POST", headers=header,
                                        verify_ssl=False,timeout=60,
                                        data=param, allow_redirects=True, **kwargs) as resp:
                    response = await resp.read()
                    await add_elk(self.spider.token,self.construct_dateitem(response, url,param))
                    return response
        except Exception as e:
            print(str(e))
            pass