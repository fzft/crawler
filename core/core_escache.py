from core.consistant import CallRecordParam as FLAG
from datetime import datetime
from aioelasticsearch import Elasticsearch
from core.core_utils import *
from utils.chen.DateTime import *
from utils.chen.ExObject import *
from utils.chen.chenUtils import *
import asyncio
import random
import hashlib
from typing import TypeVar, Iterable, Tuple, Dict, List
#region Model
class ICacheItem():
    """
    缓存补充字段模型，注意page从1开始！
    """
    month:str=""
    page:int=1
    maxPages:int=1
    def __init__(self):
        self.month:str=""
        self.page:int=1
        self.maxPages:int=1
    
class CrawledStateMonth():
    """
    已抓取月份状态
    """
    def __init__(self,monthStr, *args, **kwargs):
        self.crawledMonth=monthStr
        self.crawledMonth:str
        self.crawledPages:List[int]=[]
        self.maxPages:int=1
    def getDict(self):
        result={}
        result['crawledMonth']=self.crawledMonth
        result['crawledPages']=self.crawledPages
        result['maxPages']=self.maxPages
        return result

    @staticmethod
    def create(obj):
        r=CrawledStateMonth(obj['crawledMonth'])
        r.crawledPages=obj['crawledPages']
        r.maxPages=obj['maxPages']
        return r

class EsCacheModel():
    """
    ES数据库缓存模型
    """

    def __init__(self):
        self.month:str=""
        self.apiClass:str=""
        self.phoneNo:str=""
        self.dataType:str=""
        self.page:int=1
        self.maxPages:int=1
        self.updateTime:int=0
        self.items:list=[]

    def create(self,esResult):
        pass

    def getId(self):
        return hashlib.md5((self.apiClass+self.dataType+self.phoneNo+self.month+str(self.page)).encode(encoding='UTF-8')).hexdigest()

    def getDict(self):
        _r={
            "id":self.getId(),
            "month":self.month,
            "apiClass":self.apiClass,
            "phoneNo":self.phoneNo,
            "dataType":self.dataType,
            "page":self.page,
            "maxPages":self.maxPages,
            "updateTime":self.updateTime,
            "items":self.items
        }
        return _r

class CacheResult():
    def __init__(self, *args, **kwargs):
        self.state:List[CrawledStateMonth]=[]
        #caches=List[EsCacheModel]
        self.caches=[]

#endregion

#region utils
def changeStateDictToObj(state)->Dict[str,CrawledStateMonth]:
    r:Dict[str,CrawledStateMonth]={}
    for key in state.keys():
        if type(state[key]) is dict:
            r[key]=CrawledStateMonth.create(state[key])
        else:
            r[key]=state[key]
    return r
def createEsDataModel(originData,dataType:FLAG):
    result={}
    result['month']=originData.month
    result['page']=originData.page
    result['maxPages']=originData.maxPages
    if dataType==FLAG.CALL_RECORD:
        result['callAddress']=originData.callAddress
        result['callDateTime']=originData.callDateTime
        result['callTimeLength']=originData.callTimeLength
        result['callType']=originData.callType
        result['mobileNo']=originData.mobileNo
    elif dataType==FLAG.SMS_INFO:
        result['mobileNo']=originData.mobileNo
        result['sendSmsToTelCode']=originData.sendSmsToTelCode
        result['sendSmsAddress']=originData.sendSmsAddress
        result['sendSmsTime']=originData.sendSmsTime
        result['sendType']=originData.sendType
    elif dataType==FLAG.BILL:
        result['mobileNo']=originData.mobileNo
        result['startTime']=originData.startTime
        result['comboCost']=originData.comboCost
        result['sumCost']=originData.sumCost
        result['realCost']=originData.realCost
    elif dataType==FLAG.RECHARGE:
        result['rechanreTime']=originData.rechanreTime
        result['rechanreAmount']=originData.rechanreAmount
    elif dataType==FLAG.BALANCE_INFO:
        result['settlementDate']=originData.settlementDate
        result['balance']=originData.balance
    else:
        return None
    return result

def getMonthStr(crawlCount,add=0):
    results:List[str]=[]
    crawlCount=int(crawlCount)
    if (crawlCount > 0):
        crawlCount = -crawlCount
    crawlCount = crawlCount - add
    date=DateTime.Now()
    for i in range(0,crawlCount,-1):
        results.append(date.AddMonths(i).ToString("yyyyMM"))
    return results

def analysisCrawledState(items:List[EsCacheModel])->Dict[str,CrawledStateMonth]:
    """
    根据所有缓存数据统计已抓取信息
    items:所有缓存数据
    """
    result:Dict[str,CrawledStateMonth]={}
    for item in items:
        if item.month not in result.keys():
            result[item.month]=CrawledStateMonth(item.month)
        if item.page not in result[item.month].crawledPages:
            result[item.month].crawledPages.append(item.page)
        result[item.month].maxPages=item.maxPages
    return result

def checkData(cacheItem,dataType:FLAG)->bool:
    """
    检测数据是否正常
    """
    if dataType==FLAG.CALL_RECORD:
        if not re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",cacheItem['callDateTime']):
            return False
        return True
    if dataType==FLAG.SMS_INFO:
        if not re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",cacheItem['sendSmsTime']):
            return False
        return True
    if dataType==FLAG.BILL:
        if not re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",cacheItem['startTime']):
            return False
        return True
    if dataType==FLAG.RECHARGE:
        if not re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",cacheItem['rechanreTime']):
            return False
        return True
    if dataType==FLAG.BALANCE_INFO:
        if not re.search("([0-9]{4})\\-([0-9]{1,2})\\-([0-9]{1,2}) (\\d{1,2}):(\\d{1,2}):(\\d{1,2})",cacheItem['settlementDate']):
            return False
        return True
    #Not Support
    False

#endregion

class EsCache:
    def __init__(self, *args, **kwargs):
        self.esindex = "operator_cache_current"
        self.estype = "cachemodel"

    async def getAllCache(self,classStr:str,phoneStr:str,dataType:FLAG,monthRange:List[str]) ->List[EsCacheModel]:
        """
        根据指定条件获得所有缓存
        classStr:类名称
        phoneStr:手机号码
        dataType:缓存数据类型
        monthRange:日期数组
        返回类型:list(EsCacheModel)
        """
        result=[]
        monthRange=[f"month:{month}" for month in monthRange]
        query='apiClass:{} AND phoneNo:{} AND dataType:{} AND ({})'.format(
            classStr,
            phoneStr,
            dataType.value,
            ' OR '.join(monthRange))
        async with Elasticsearch(
                [{'host': config[ELK.ELK_HOST.value], 'port': config[ELK.ELK_PORT.value],
                  "timeout": 360000}]) as es:
            r=await es.search(index=self.esindex,doc_type=self.estype,q=query)
        r=ExObject(r)
        for item in r["?hits"]["?hits"]:
            _ec=EsCacheModel()
            _ec.apiClass=item["?_source"]["?apiClass"].ToString()
            _ec.month=item["?_source"]["?month"].ToString()
            _ec.phoneNo=item["?_source"]["?phoneNo"].ToString()
            _ec.dataType=item["?_source"]["?dataType"].ToString()
            _ec.page=item["?_source"]["?page"].ToOriginal()
            _ec.maxPages=item["?_source"]["?maxPages"].ToOriginal()
            _ec.updateTime=item["?_source"]["?updateTime"].ToOriginal()
            _ec.items=item["?_source"]["?items"].ToOriginal()
            result.append(_ec)
        return result

    async def setSingleCache(self,cacheModel:EsCacheModel)->bool:
        """
        写入单条缓存数据
        classStr:类名称
        phoneStr:手机号码
        dataType:缓存数据类型
        month:日期(格式:yyyyMM)
        page:页码
        maxPages:总页数
        dataItems:缓存数据
        返回:是否成功写入
        """
        _item=cacheModel
        try:
            async with Elasticsearch(
                [{'host': config[ELK.ELK_HOST.value], 'port': config[ELK.ELK_PORT.value],
                  "timeout": 360000}]) as es:
                await es.index(index=self.esindex, body=_item.getDict(), doc_type=self.estype,id=_item.getId())
            return True
        except Exception:
            traceback.print_exc()
            return False

    async def setBulkCache(self,cacheModels:List[EsCacheModel]):
        async with Elasticsearch(
                [{'host': config[ELK.ELK_HOST.value], 'port': config[ELK.ELK_PORT.value],
                  "timeout": 360000}]) as es:
            _actions=[]
            for item in cacheModels:
                _actions.append({"index":{"_index": self.esindex, "_type": self.estype, "_id": item.getId()}})
                _actions.append(item.getDict())
            return await es.bulk(body=_actions)
        pass

    @staticmethod
    def checkMonthPage(monthYear:str,page:int,_state:Dict[str,CrawledStateMonth])->bool:
        """
        根据已抓取信息[state]判断是否需要抓取数据，返回（True：抓取） or （False：不抓取）
        cacheType:数据类型
        monthYear:判断抓取的年月
        page:判断抓取的页码
        _state:已抓取状态信息，从getCache方法中返回的CacheResult对象的state属性 获得
        """
        
        if monthYear not in _state.keys():
            return True

        state=changeStateDictToObj(_state)

        if page==1:
            #如果已抓取的最大页数大于maxPage则表示第一页必抓系列。。。。
            if len(state[monthYear].crawledPages)>0 and max(state[monthYear].crawledPages)>state[monthYear].maxPages:
                return True
            for i in range(1,state[monthYear].maxPages+1):
                if i not in state[monthYear].crawledPages:
                    return True
            return False

        if page not in state[monthYear].crawledPages:
            return True
        return False

    @staticmethod
    async def getCache(task_params:dict,cacheType:FLAG)->CacheResult:
        """
        根据任务参数以及缓存类型获得所有缓存
        task_params:任务参数
        cacheType:缓存类型(CallRecordParam:emum)
        """
        result=CacheResult()
        try:
            es=EsCache()
            _caches= await es.getAllCache(task_params['Area'],task_params['UserName'],cacheType,getMonthStr(task_params['month']))
            result.state=analysisCrawledState(_caches)
            result.caches=[]
            for item in _caches:
                #判断如果第一页是否为必抓（当该月数据缺月的情况） 如果必抓，则缓存的数据不返回
                if item.page==1 and EsCache.checkMonthPage(item.month,1,result.state):
                    pass
                elif item.page==-1:
                    pass
                else:
                    result.caches.extend(item.items)
            for key in result.state.keys():
                result.state[key]=result.state[key].getDict()
                
        except Exception:
            result.state={}
            result.caches=[]
        finally:
            return result

    @staticmethod
    async def setCache(task_params:dict,cacheType:FLAG,cacheData:List[ICacheItem],_state:Dict[str,CrawledStateMonth]=None)->bool:
        """
        储存缓存数据
        task_params:任务参数
        cacheType:缓存类型(CallRecordParam:emum)
        cacheData:具体需要缓存的所有数据
        _state:获得缓存数据时返回的已缓存数据状态
        """
        try:
            nowStr=DateTime.Now().ToString("yyyyMM")
            nowStrOffSet=DateTime.Now().AddDays(-3).ToString("yyyyMM")
            if not _state:
                state={}
            else:
                state=changeStateDictToObj(_state)

            cacheModels:List[EsCacheModel]=[]
            es=EsCache()
            #遍历数据，按月进行分组，并且清洗所有DateTime不正确的格式
            _cmonths=state.keys()
            for item in cacheData:
                #判断是否开发者有漏写month(必要)
                if not item.month:
                    #忽略记录缓存
                    print("检测到没有month,此条缓存记录无效")
                    continue

                #判断如果当前月份的当前页已在state里面，说明已经缓存过，不存储
                if (item.month in _cmonths):
                    if (item.page in state[item.month].crawledPages):
                        continue

                #判断如果数据月份为当月，不储存当月数据
                if (item.month==nowStr):
                    continue
                if (item.month==nowStrOffSet):
                    continue
                #分组数据
                _r=ExObject(list(filter(lambda x:x.month==item.month and x.page==item.page,cacheModels)))["?0"]
                item=createEsDataModel(item,cacheType)
                if not item:
                    return False
                if _r:
                    _r.ToOriginal().items.append(item)
                else:
                    _item=EsCacheModel()
                    _item.apiClass=task_params['Area']
                    _item.phoneNo=task_params['UserName']
                    _item.dataType=cacheType.value
                    _item.month=item['month']
                    _item.page=item['page']
                    _item.maxPages=item['maxPages']
                    _item.items=[]
                    _item.items.append(item)
                    _item.updateTime=DateTime().Now().TimeStampLong()
                    cacheModels.append(_item)

            #判断数据中的所有子数据，如果有一条清洗失败，则整条不写缓存
            rCacheModel=[]
            for cacheModel in cacheModels:
                if checkData(cacheModel.items[0],cacheType):
                    rCacheModel.append(cacheModel)
            if len(rCacheModel)==0:
                return False
            r=await es.setBulkCache(rCacheModel)
            if r['errors']:
                errObj=ExObject(r)
                reason=errObj['?items']['?0']['?index']['?error']['?reason'].ToString()
                print("写入错误 理由:"+reason)
                return False
            return True
        except:
            print(traceback.format_exc())
            print('失败')
            return False

    @staticmethod
    async def deleteSingleCache(_id:str):
        pass