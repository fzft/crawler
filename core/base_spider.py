import pickle
from collections import ChainMap

from celery.canvas import Signature, group

import entity.models
from core.ctx import TaskHandler
from encrypt.encrypt import md5
from entity.models import *
from http_utils.headers import Headers, default_headers
from core._global import task
from core.consistant import CallRecordParam as cr, ContentFlag as cf
from core.code_map import CALLRECORD_MAP as cm
from core.core_escache import *
from core.core_utils import filter_list_field

TIMEOUT = 300


def check_month(args):
    e = 'ALL'
    for i in args:
        if isinstance(i, str):
            # if re.match('\d{6}', i) or re.match('\d{4}-\d{2}', i) or re.match('\d{4}'):
            e = i
            break
    return e


def check_page(args):
    p = 1
    for i in args:
        if isinstance(i, int) and 0 < i < 500:
            p = i
            break
    return p


def set_dto(inst, clsmembers):
    for attr in clsmembers:
        inst._meta[attr] = getattr(inst, attr)


def call_record_info_adaptor(rsc: list) -> list:
    for info in rsc:
        if info == 'busi':
            rsc.append('business')
    return rsc


def content_flag_handler(cls_name, ContentFlag) -> bool:
    """
    alls(全量数据)

       all(跟全量数据相比，没有每月余额和充值记录数据）
       sms(短信记录)
       busi(业务记录)
       balance(余额)
       recharge(充值记录)

       bill ,个人基本信息，通话记录，这三个才是必须的
       除了必须要采集，其余的都是根据contentflag中的采集
       sms;recharge;busi;balance

    :param cls_name: 当前协程爬取的信息类
    :param ContentFlag: 前端传入的content参数
    :return: 是否需要爬取当前的信息
    """
    tar_space = set(cls_name)

    full_space = {cr.BUSINESS_INFO.value, cr.SMS_INFO.value, cr.BILL.value, cr.CALL_RECORD.value, cr.RECHARGE.value,
                  cr.BASIC_INFO.value, cr.BALANCE_INFO.value, cr.FAMILY.value}
    sed_full_space = {cr.BUSINESS_INFO.value, cr.SMS_INFO.value, cr.BILL.value, cr.CALL_RECORD.value,
                      cr.BASIC_INFO.value}
    nes_space = {cr.BILL.value, cr.BASIC_INFO.value, cr.CALL_RECORD.value}
    flag_space = set(call_record_info_adaptor(ContentFlag.split(';')))
    # if cf.ALLS.value in flag_space:
    #     cur_space = full_space
    if cf.ALL.value in flag_space:
        cur_space = full_space
    else:
        cur_space = flag_space | nes_space
    if len(tar_space & cur_space):
        return True
    return False


# 缓存判断逻辑
async def cache_flag_handler(inst: TaskHandler, cls_names, m=time.strftime('%Y%m'), page=1) -> bool:
    try:
        if time.strftime('%Y%m') == m or m == 'ALL':
            return True

        for cls_obj in cls_names:
            cls_str = get_enum_value_by_inst(cls_obj, CallRecordParam)
            if inst.cache.get(cls_str) is not None:
                print(f'{m} {page} {EsCache.checkMonthPage(m, page, inst.cache[cls_str].state)}')
                if EsCache.checkMonthPage(m, page, inst.cache[cls_str].state):
                    return True
                else:
                    await simple_log(inst, diy.DIY_STATUS.value, message=f'从缓存中获取{cls_str} {m}月份 第{page}页数据')
                    return False
            else:
                return True
        return True
    except Exception as e:
        import traceback
        print(traceback.format_exc())


async def log_before(inst, cls_name, attrs, args) -> bool:
    flag = False
    if attrs is not None and len(attrs):
        flag = True
        for name, values in zip(cls_name, attrs):
            clz = getattr(inst, name)
            for v in values:
                _current_inside_attr = getattr(clz, v)
                if isinstance(_current_inside_attr, list):
                    e = check_month(args)
                    await simple_log(inst, diy.DIY_STATUS.value, message=f'正在采{e}{eng_to_chn(name)}')
                else:
                    await simple_log(inst, diy.DIY_STATUS.value, message=f'正在采{eng_to_chn(name)}{v}信息')

    return flag


def eng_to_chn(eng: str) -> str:
    return cm.get(eng)


async def log_after(flag, inst, cls_name, attrs, args):
    if flag:
        for name, values in zip(cls_name, attrs):
            clz = getattr(inst, name)
            for v in values:
                _current_inside_attr = getattr(clz, v)
                if isinstance(_current_inside_attr, list):
                    e = check_month(args)
                    after = len(_current_inside_attr)
                    r = after - 0
                    if r == 0:
                        await simple_log(inst, diy.DIY_STATUS.value, message=f'采集{e}{eng_to_chn(name)}信息失败')
                    else:
                        await simple_log(inst, diy.DIY_STATUS.value, message=f'采集{e}{eng_to_chn(name)}信息成功')
                else:
                    if getattr(clz, v) is None or getattr(clz, v) == '':
                        await simple_log(inst, diy.DIY_STATUS.value, message=f'采集{eng_to_chn(name)}{v}信息失败')
                    else:
                        await simple_log(inst, diy.DIY_STATUS.value, message=f'采集{eng_to_chn(name)}{v}信息成功')


def create_inst(cls_names=[], attrs=[], is_log=True):
    def decorator(func):
        @wraps(func)
        async def wrapped(self, *args, **kwargs):
            if isinstance(self, BaseSpider):
                cls_name = list(map(lambda x: get_enum_value_by_inst(x, CallRecordParam), cls_names))
                # if content_flag_handler(cls_name, inst.task_params['ContentFlag']) and \
                #         (await cache_flag_handler(inst, cls_names, m=check_month(args),
                #                                   page=check_page(args))):  # 缓存判断逻辑

                for name in cls_name:
                    if name in self.clsmembers.keys() and getattr(self, name) is None:
                        setattr(self, name, self.clsmembers[name]())
                        setattr(getattr(self, name), 'token', getattr(self, 'task_params')['token'])
                        setattr(getattr(self, name), 'create_at', time.strftime('%Y%m%d%H%M%S'))
                if is_log:
                    flag = await log_before(self, cls_name, attrs, args)

                f = await func(self, *args, **kwargs)

                if is_log:
                    await log_after(flag, self, cls_name, attrs, args)

                return f
            return None

        return wrapped

    return decorator


def set_meta_decorator(func):
    @wraps(func)
    async def wrapped(inst, *args, **kwargs):
        if isinstance(inst, BaseSpider):
            fut = await func(inst, *args, **kwargs)
            inst._meta['cookie_dict'] = inst.cookie_jar._cookies
            for name in ['task_params', 'token', 'proxy', 'phase', 'clsmembers', 'pdf_active']:
                inst._meta[name] = getattr(inst, name)
            set_dto(inst, inst.clsmembers)
            await simple_log(inst, diy.DIY_STATUS.value, message=f'存储meta: {inst._meta}')
            await getattr(inst, 'rc').save_meta(f'{config.META_KEY_PREFIX }:{inst.token}',
                                                pickle.dumps(inst._meta))
            await inst.rc.save_status(f'{config.TASK_CLASS_NAME}:{inst.token}',
                                      inst.__class__.__name__)
            return fut

    return wrapped


class BaseSpider(TaskHandler):
    PROXY = False
    pdf_concurrence = True

    start_url = None
    base_url = None

    def __init__(self, token=None, task=None, *args, **kwargs):
        super().__init__(token, task, *args, **kwargs)
        self.pdf_declaration_bin_lst = []
        self.pdf_declaration_url_lst = []

        self.headers = Headers(default_headers())
        self.proxy = None
        self.cookie_jar = None
        self.session = None
        self._meta = {}
        self.cookie_dict = {}
        self.phase = None
        self.pdf_active = False

        self._create_dto()

    def task_timeout_handler(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait({
            task.save_data(),
            simple_log(task, diy.DIY_STATUS.value, message='任务超时')
        }))

    def run(self):
        super().run()
        self.rc = RedisClient(**current_app.config)
        mongo_url = f'mongodb://{current_app.config.MONGO_USERNAME}:{current_app.config.MONGO_PASSWORD}@{current_app.config.MONGO_HOST}:{current_app.config.MONGO_PORT}/{current_app.config.MONGO_DB}?authSource={current_app.config.MONGO_AUTHSOURCE}'
        if current_app.config.get(MongoConfigParams.MONGO_REPLICASET.value) is not None:
            mongo_url = f'{mongo_url}&replicaSet={config.get(MongoConfigParams.MONGO_REPLICASET.value)}'
        self.mongo_client = AsyncIOMotorClient(mongo_url)
        self.request_retry = current_app.config[RequestConfig.REQUEST_RETRY.value]
        self._proxy_retry = current_app.config[RequestConfig.PROXY_RETRY.value]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.sub_run())

    async def change_channel(self, des: str):
        if des not in self.task_params[current_app.config.EXECUTED_CHANNELS]:
            await simple_log(self, SPECIAL_STATUS.DIY_STATUS.value,
                             message=f'正在切换通道{self.task_params["Area"]} -> {des}')
            self.task_params['Area'] = des
            raise CHANGE_CHANNEL(task=self.task_params)
        else:
            await simple_log(self, SPECIAL_STATUS.DIY_STATUS.value,
                             message=f'目标通道{des}已被切换执行过无法执行')

    async def sub_run(self):
        # executed = (await self.rc.get(f'{current_app.config[CeleryQueue.EXECUTED_TASK_PREFIX.value]}{self.token}'))
        if self.task_params.get('phase') == 1:
            await self.resource_lock_handler(md5(self.task_params['company_name']))

        else:
            await self.main()

    async def main(self):
        self.cookie_jar = aiohttp.CookieJar(unsafe=True)
        if self.task.get('phase') == 1:
            await simple_log(self, '0010')
            # await simple_log(self,
            #                  message=f'{chn_map.get(self.task_params["mobileType"])}用户{self.task_params["UserName"]}开始登录中')
            # proxy_str = (await self.rc.get(current_app.config[CeleryQueue.PROXYXML_KEY.value])).decode()
            # if self.__class__.__name__ in proxy_str:
            #     proxy_dynamic_str = (
            #         await self.rc.get(current_app.config[CeleryQueue.PROXY_DYNAMIC_KEY.value])).decode()
            #
            #     if self.__class__.__name__ in parse_xml_to_type(proxy_dynamic_str):
            #         self.proxy_dynamic = True
            #     else:
            #         self.proxy_dynamic = False
            #     await self.get_proxy()

            # 缓存部分
            # await self.get_cache()

        await self.handle_message()

    async def init_request(self, url):
        await simple_log(self, diy.DIY_STATUS.value, message=f'start_url: {self.start_url}')
        async with aiohttp.ClientSession(cookie_jar=self.cookie_jar) as session:
            response = await fetch(url, self, session)
            return response

    async def get_cache(self):
        """处理缓存逻辑"""

        self.cache = {}
        target_lst = [cr.CALL_RECORD, cr.SMS_INFO]
        for tar in target_lst:
            cls_str = get_enum_value_by_inst(tar, CallRecordParam)
            cache_ret = await EsCache.getCache(self.task_params, tar)
            self.cache[cls_str] = cache_ret
            await simple_log(self, diy.DIY_STATUS.value, message=f'从缓存中获得数据{tar.value} 数目{len(cache_ret.caches)}')

    def init_parse(self, response):
        """parse start_url"""

    @set_meta_decorator
    async def crawl(self):
        if self.start_url is not None and self.phase == 1:
            loop = asyncio.get_event_loop()
            init_fut = loop.create_task(self.init_request(self.start_url))
            init_fut.add_done_callback(lambda future: self.init_parse(future.result()))
            await init_fut
        if self.phase > 1:
            await rc.zrem_certain_task(
                f'{self.task_params.get("province")}:{self.task_params.get("channel_id")}:{self.token}:{self.task_params.get("telephone")}:{self.task_params.get("company_name")}:{self.task_params.get("verify_result")}:{self.task_params.get("id")}')

        await self.customed_crawl()

    async def customed_crawl(self):
        """ 自定义 爬虫逻辑"""

    async def handle_message(self):
        self.phase = self.task.get('phase')
        if self.phase > 1:
            await self.get_meta()
        await simple_log(self, diy.DIY_STATUS.value, message=f'获取任务参数: {task.task_params}')
        self.change_pdf_active()
        await self.crawl()

    def change_pdf_active(self):
        self.pdf_active = current_app.config[PdfDeclaration.PDF_ACTIVE.value]
        if self.task_params.get('pdf_active') is not None:
            self.pdf_active = self.task_params.get('pdf_active')

    async def get_proxy(self):
        """获取代理ip"""
        # async with aiohttp.ClientSession() as session:
        # response = await fetch(current_app.config.ADSL_URL, self, session, result_type='json')
        # ip = response.json.get('ip')
        # self.proxy = f'http://{ip}:8907'
        self._proxy_retry -= 1
        await simple_log(self, diy.DIY_STATUS.value,
                         message=f'第{current_app.config.PROXY_RETRY - self._proxy_retry} 重试')

    async def get_pdf_bin(self, pdus: PdfDeclarationUrlStruct):
        async with aiohttp.ClientSession(cookie_jar=pdus.cookie_jar) as session:
            try:
                response = await fetch(pdus.url, self, session)
                # from reportlab.pdfgen import canvas
                # pdf_name = f'{random.randint(1 ,1000000)}.pdf'
                # canvas.Canvas(pdf_name)
                # with open(pdf_name, 'wb') as f:
                #     f.write(response.body)
                pdbs = PdfDeclarationBodyStruct(declarationMeta=pdus.declarationMeta, body=str(response.body))
                self.pdf_declaration_bin_lst.append(pdbs)
            except:
                await simple_log(self, diy.DIY_STATUS.value,
                                 message=f'获取pdf 失败url: {pdus.url} 申报项目: {pdus.declarationMeta.d_project} 所属日期起:{pdus.declarationMeta.payment_starttime} 所属日期止：{pdus.declarationMeta.payment_endtime}')

    async def save_data(self, exception=False, ex_message=None):
        await self.pdf_declaration_pipeline(exception)
        await self.statistics_pipeline(exception, ex_message)
        coros = [getattr(self, name).save(self.mongo_client[current_app.config.MONGO_DB],
                                          do_insert=False)
                 for
                 name
                 in self.clsmembers if getattr(self, name) is not None]
        if len(coros):
            f = await asyncio.wait(coros)
            for ff in f:
                if len(ff):
                    e = ff.pop().exception()
                    if e:
                        raise MongoError(description=str(e))
        if not exception:
            await simple_log(self, '200')
            await asyncio.wait({
                simple_log(self, diy.DIY_STATUS.value, message='存储中'),
                self.rc.set_expire(f'{current_app.config.EXECUTED_TASK_PREFIX}{self.token}',
                                   self.token, current_app.config.EXECUTED_TASK_PERSIST_TIME)

            })

    async def pdf_declaration_pipeline(self, exception):
        if not exception:
            if self.pdf_declaration_url_lst:
                await simple_log(self, diy.DIY_STATUS.value,
                                 message=f'下载pdf:declaration body 共计{len(self.pdf_declaration_url_lst)}')
                tasks = [self.get_pdf_bin(u) for u in self.pdf_declaration_url_lst]

                # 并行还是串行
                if self.pdf_concurrence:
                    await asyncio.wait(tasks)
                else:
                    for f in tasks:
                        await f

            if self.pdf_declaration_bin_lst:

                tasks = [Signature(current_app.config.PDF_TASK,
                                   [pdbs.body, pdbs.declarationMeta._asdict(), {'province': self.task_params['province'], 'company_name': self.task_params['company_name']}],
                                   queue=current_app.config.PDF_QUEUE, app=current_app.app) for
                         pdbs
                         in
                         self.pdf_declaration_bin_lst]
                job = group(*tasks)
                group_result = job.apply_async()
                await simple_log(self, diy.DIY_STATUS.value,
                                 message=f'已提交pdf:declaration任务 共计{len(self.pdf_declaration_bin_lst)} task_id')
                while not group_result.ready():
                    await asyncio.sleep(.1)
                success_results = [async_result.info for async_result in group_result.results if
                                   async_result.state == 'SUCCESS']
                await simple_log(self, diy.DIY_STATUS.value,
                                 message=f'获得提交pdf:declaration任务结果 共计{len(success_results)} 成功任务')
                for result in success_results:
                    if result and (not result.get('code')):
                        declaration = json_data_mapper(result, DeclarationInfo)
                        self.declaration.declarationInfo.append(declaration)
                await simple_log(self, diy.DIY_STATUS.value,
                                 message=f'实际获得declaration对象数 共计{len(self.declaration.declarationInfo)}')

    async def statistics_pipeline(self, exception=False, ex_message=None):
        stats_dict = dict(ChainMap(*[item
                                     for item in map(filter_list_field, [getattr(self, name)
                                                                         for name in self.clsmembers if
                                                                         getattr(self, name) is not None]) if
                                     item is not None]))
        await simple_log(self, diy.STATISTICS_STATUS.value, message=str(stats_dict))
        is_schedule = self.task_params.get('schedule')
        if is_schedule is not None and is_schedule is True:
            self.statistics = Statistics()
            self.statistics.company_name = self.task_params['company_name']
            self.statistics.token = self.task_params['token']
            self.statistics.province = self.task_params['province']
            self.statistics.create_at = time.strftime('%Y%m%d')
            if not exception:
                self.statistics.declarationInfo = stats_dict.get('declarationInfo', '0')
                self.statistics.inspectionInfo = stats_dict.get('inspectionInfo', '0')
                self.statistics.ratingInfo = stats_dict.get('ratingInfo', '0')
                self.statistics.invoiceInformation = stats_dict.get('invoiceInformation', '0')
                self.statistics.person = stats_dict.get('person', '0')
            else:
                self.statistics.success = False
                self.statistics.message = ex_message

    async def get_meta(self):
        result = await self.rc.rpop(f'{config.META_KEY_PREFIX }:{task.token}')
        if result is not None:
            self._meta = pickle.loads(result)
            await self.load_meta()
            await simple_log(self, diy.DIY_STATUS.value, message=f'获取meta: {self._meta}')

    async def load_meta(self):
        captcha = self.task_params.get('smsvalue')
        self.task_params.update(self._meta['task_params'])
        if captcha:
            self.task_params['smsvalue'] = captcha
        self.cookie_jar._cookies = self._meta['cookie_dict']
        for name in ['token', 'proxy', 'phase', 'clsmembers', 'pdf_active']:
            setattr(self, name, self._meta[name])
        self._load_dto()

    def _load_dto(self):
        for attr in self.clsmembers:
            setattr(self, attr, self._meta[attr])

    def _create_dto(self):
        self.clsmembers = {clsmember[0].lower(): clsmember[1] for clsmember in
                           inspect.getmembers(entity.models, inspect.isclass) if
                           issubclass(clsmember[1], Document) and not (clsmember[0] == 'Document')}
        for name in self.clsmembers:
            setattr(self, name, None)
