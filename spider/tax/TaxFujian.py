from captcha.captcha_validator_utils import CaptchaValidatorUtils
from core.base_spider import *
from core.core_requests import fetch, post
from core.core_utils import *
from encrypt.encrypt import Encrypt_CBC


class Fujian(BaseSpider):
    # PROXY = True

    key = 'cn.com.foresee01'
    iv = 'cn.com.foresee02'

    zsxmDm_lst = ['10101', '10104', '10112', '10111', '10121']

    async def customed_crawl(self):
        if self.phase == 1:
            self._meta['captcha_retry'] = 5
            return await self.index()
        elif self.phase == 2:
            await self.login()
            return await self.save_data()

    async def index(self):
        url = f"https://etax.fujian.chinatax.gov.cn/sso/login?service=https://etax.fujian.chinatax.gov.cn/xxmh/html/index_login.html?t=" \
              f"{time_stamp()}"
        self._meta['index_url'] = url
        async with aiohttp.ClientSession(cookie_jar=self.cookie_jar) as session:
            response = await fetch(url, self, session)
            self._meta['lt'] = response.css('input[name=lt]::attr(value)').extract_first()
            self._meta['execution'] = response.css('input[name=execution]::attr(value)').extract_first()
            self._meta['_llqmc'] = response.css('input[name=_llqmc]::attr(value)').extract_first()
            self._meta['_llqbb'] = response.css('input[name=_llqbb]::attr(value)').extract_first()
            await self.get_captcha(session)

    async def get_captcha(self, session):
        self.headers['Upgrade-Insecure-Requests'] = '1'
        url = 'https://etax.fujian.chinatax.gov.cn/sso/base/captcha.do'
        response = await fetch(url, self, session)
        self._meta['vcode'] = await CaptchaValidatorUtils.get_captcha_with_retry(self, response.body, codetype='1006')
        await self.send_sms(session)

    async def send_sms(self, session):
        self.headers['Sec-Fetch-Dest'] = 'iframe'
        self.headers['Sec-Fetch-Mode'] = 'navigate'
        self.headers['Sec-Fetch-Site'] = 'same-origin'
        self.headers['Sec-Fetch-User'] = '?1'
        self.headers['Referer'] = self._meta['index_url']
        url = f'https://etax.fujian.chinatax.gov.cn/sso/login?service=https://etax.fujian.chinatax.gov.cn/xxmh/html/index_login.html?t={time_stamp()}'
        CBC_obj = Encrypt_CBC(self.key, self.iv)
        username_enc = CBC_obj.encrypt(self.task_params['username'])
        passwd_enc = CBC_obj.encrypt(self.task_params['password'])
        resp = await post(url, self, session, data={
            'lt': self._meta['lt'],
            'execution': self._meta['execution'],
            '_eventId': 'submit',
            '_llqmc': self._meta['_llqmc'],
            '_llqbb': self._meta['_llqbb'],
            '_czxt': 'Unix',
            '_czxtbb': 'Unknown',
            'sjly': '2',
            'userName': username_enc,
            'passWord': passwd_enc,
            'captchCode': self._meta['vcode'],
            'authencationHandler': 'FjgsUsernamePasswordAuthencationHandler'
        })
        resp_html = resp.text
        if "用户名或密码错误" in resp_html:
            raise LoginAccountError()
        if "验证码出错" in resp_html:
            if self._meta['captcha_retry'] > 0:
                self._meta['captcha_retry'] -= 1
                return await self.get_captcha(session)
            else:
                raise AuthCodeErrorTooMany()
        msg_captche_url = f"https://etax.fujian.chinatax.gov.cn/sso/fjgsAuth/sendCheckCodeQy.do?lxdh={self.task_params['telephone']}&t={time_stamp()}"
        resp = await post(msg_captche_url, self, session)
        data = resp.json
        if '发送短信成功' in data['msg']:
            self.phase = 2
            await simple_log(self, '110')
        elif '不允许重复发送' in data['msg']:
            raise SmsSendTooMany(description=str(data['msg']))
        elif '该纳税人未登记有效的手机号码' in data['msg']:
            raise TelephoneError(description=str(data['msg']))
        else:
            raise WebSiteException(description=str(data))

    async def login(self):
        async with aiohttp.ClientSession(cookie_jar=self.cookie_jar) as session:
            url = 'https://etax.fujian.chinatax.gov.cn/sso/fjgsAuth/qyCheckCode.do'
            resp = await post(url, self, session, data={
                'yzm': self.task_params['smsvalue']
            })
            data = resp.json
            if data["flag"] == "Y" and data["msg"] == "验证成功!":
                resp = await  post('https://etax.fujian.chinatax.gov.cn/sso/login', self, session)
                resp_html = resp.text
                if "CAS登录成功" in resp_html:
                    await simple_log(self, '100')
                    await self.get_all(session)
            else:
                raise SMSError(description=str(data))

    async def get_all(self, session):
        year_lst = get_year_lst(current_app.config.TAX_FROM_YEAR)
        tasks = [
            self.get_taxpayer_info(session),
            *[self.get_rating_details(session, y) for y in year_lst],
            *[self.get_inspection_details(session, y) for y in year_lst],
            *[self.get_invoice_details(session, y, fplx) for y in year_lst for fplx in ["11", "1130"]],
        ]

        pdf_active = current_app.config[PdfDeclaration.PDF_ACTIVE.value]
        if pdf_active:
            tasks.extend([self.get_declaration_pdf_details(session, y) for y in year_lst])
        else:
            tasks.extend([self.get_declaration_details(session, y, zsxm) for y in year_lst for zsxm in self.zsxmDm_lst])

        await asyncio.wait(tasks)

    @create_inst(cls_names=['registration', cr.PERSON], attrs=[
        ('taxpayer_code', 'taxpayer_name', 'operation_product_address', 'operation_product_address', 'taxpayer_status',
         'operation_address',
         'business_scope'), ('person',)])
    async def get_taxpayer_info(self, session):
        url = "https://etax.fujian.chinatax.gov.cn/yhgl/service/um/cxpt/query.do?bw=%7B%22taxML%22:%7B%22head%22:%7B%22gid%22:%22311085A116185FEFE053C2000A0A5B63%22,%22sid%22:%22dzswj.yhgl.qyxx.djxxcx%22,%22tid%22:%22+%22,%22version%22:%22%22%7D,%22body%22:%7B%7D%7D%7D&gdslxDm=1"
        resp = await fetch(url, self, session)
        resp_dict = resp.json
        result_dict = resp_dict["taxML"]["body"]["taxML"]["djxxGrid"]["djxxGridlb"][0]
        qxb_data = Enterprise_api(tv="0").getDetailByName(keyword=result_dict.get("nsrmc", ""))
        if qxb_data.get("code", 0) == 200:
            self.registration.operation_start_at = qxb_data.get("data").get("term_start")
            self.registration.operation_end_at = qxb_data.get("data").get("term_end")
        self.registration.taxpayer_code = result_dict.get("nsrsbh", "")
        self.registration.taxpayer_name = result_dict.get("nsrmc", "")
        self.registration.operation_product_address = result_dict.get("scjydz", "")
        self.registration.taxpayer_status = result_dict.get("nsrzt", "")
        self.registration.business_scope = result_dict.get("jyfw", "")
        self.registration.operation_address = result_dict.get("scjydz", "")
        person1 = PersonInfo()
        person1.manager_name = result_dict.get("fdfzr", "")
        person1.programe_cont = '法定负责人'
        self.person.person.append(person1)
        url = 'https://etax.fujian.chinatax.gov.cn/yhgl/service/um/cxpt/query.do?bw=%7B%22taxML%22:%7B%22head%22:%7B%22gid%22:%22311085A116185FEFE053C2000A0A5B63%22,%22sid%22:%22dzswj.yhgl.qyxx.zgxx%22,%22tid%22:%22+%22,%22version%22:%22%22%7D,%22body%22:%7B%7D%7D%7D&gdslxDm=1'
        response = await fetch(url, self, session)
        data = response.json
        ybnsrzgxx = data["taxML"]["body"]["taxML"]["zgzz"]["ybnsrzgxxList"]['ybnsrzgxx']
        if ybnsrzgxx is not None and len(ybnsrzgxx):
            nsrzg = ybnsrzgxx[0]['nsrzglxmc']
            if "一般" in nsrzg:
                nsrzg = "一般纳税人"
            elif "小规模" in nsrzg:
                nsrzg = "小规模纳税人"
            self.registration.taxpayer_qualification = nsrzg

    @create_inst(cls_names=[cr.DECLARATION], attrs=[('declarationInfo',)])
    async def get_declaration_details(self, session, year, zsxm):
        url = f"https://etax.fujian.chinatax.gov.cn/tycx-cjpt-web/cxpt/query.do?bw=%7B%22taxML%22:%7B%22head%22:%7B%22gid%22:%22311085A116185FEFE053C2000A0A5B63%22,%22sid%22:%22dzswj.yhscx.sbzs.sbxxcx%22,%22tid%22:%22+%22,%22version%22:%22%22%7D,%22body%22:%7B%22s2id_autogen1%22:%22%22,%22s2id_autogen1_search%22:%22%22,%22zsxmDm%22:%22{zsxm}%22,%22skssqq%22:%22%22,%22skssqz%22:%22%22,%22s2id_autogen2%22:%22%22,%22s2id_autogen2_search%22:%22%22,%22sblxDm%22:%22%22,%22sbssqq%22:%22{year}-01-01%22,%22sbssqz%22:%22{year}-12-31%22%7D%7D%7D&gdslxDm=1"
        response = await fetch(url, self, session)
        data = response.json
        result_list_dict = data["taxML"]["body"]["taxML"]["ysbxxList"]["ysbxx"]
        if result_list_dict:
            for item in result_list_dict:
                declaration = DeclarationInfo()
                declaration.d_project = item["zsxmmc"]
                declaration.declara_date = item["sbrq_1"]
                declaration.payment_starttime = item["skssqq"]
                declaration.payment_endtime = item["skssqz"]
                declaration.taxpay_amount = item["ynse"]
                self.declaration.declarationInfo.append(declaration)

    @create_inst(cls_names=[cr.DECLARATION], attrs=[('declarationInfo',)])
    async def get_declaration_pdf_details(self, session, year):
        url = 'https://etax.fujian.chinatax.gov.cn/sbzs-cjpt-web/sbxxcxDeliver/getSbxxcx.do'
        start_date, end_date = f'{year}-01-01', f'{year}-12-31'
        response = await fetch(url, self, session, params={
            'skssqq': start_date,
            'skssqz': end_date,
            'gdbz': '1',
            'sbny': '',
            'urlgdslxDm': '3',
            'sbrqq': '',
            'sbrqz': '',
            'ywbm': ''
        })
        text = response.text
        data = eval(text)
        for sb in data['sbList']:
            zsxmmc = sb['zsxmmc']
            if zsxmmc in ['增值税', '企业所得税', '印花税']:
                version = sb['version']
                gdslxDm = sb['gdslxDm']
                pzxh = sb['pzxh']
                ysqxxid = sb['ysqxxid']
                url = 'https://etax.fujian.chinatax.gov.cn/sbzs-cjpt-web/sbxxcx/openPdf.do'
                response = await fetch(url, self, session, params={
                    'version': version,
                    'gdslxDm': gdslxDm,
                    'pzxh': pzxh,
                    'ysqxxid': ysqxxid
                })
                declarationMeta = DeclarationMeta(declara_date=sb['sbrq'], payment_starttime=sb['ssqq'],
                                                  payment_endtime=sb['ssqz'], d_project=sb['zsxmmc'])
                pdbs = PdfDeclarationBodyStruct(declarationMeta=declarationMeta, body=str(response.body))
                self.pdf_declaration_bin_lst.append(pdbs)

    @create_inst(cls_names=[cr.RATING], attrs=[('ratingInfo',)])
    async def get_rating_details(self, session, year):
        url = "https://etax.fujian.chinatax.gov.cn/sxsq-cjpt-web/sxsq/query.do"

        response = await post(url, self, session, data={
            'gdslxDm': '1',
            'applicationId': 'NFZC.NSXY',
            'sid': 'dzswj.sxsq.wsinit.nsrxxcx.queryndpj',
            'pjnd': str(year)
        })
        data = response.json
        result_dict = data["taxML"]["body"]["taxML"]
        pjnd = result_dict["pjnd"]
        if pjnd == str(year):
            rating_info = RatingInfo()
            rating_info.appraisal_year = result_dict["pjnd"]
            rating_info.evaluation_score = result_dict["pjfs"]
            rating_info.evaluation_result = result_dict["pjjg"]
            self.rating.ratingInfo.append(rating_info)

    @create_inst(cls_names=[cr.INSPECTION],
                 attrs=[('inspectionInfo',)])
    async def get_inspection_details(self, session, year):
        url = f"https://etax.fujian.chinatax.gov.cn/tycx-cjpt-web/cxpt/query.do?bw=%7B%22taxML%22:%7B%22head%22:%7B%22gid%22:%22311085A116185FEFE053C2000A0A5B63%22,%22sid%22:%22dzswj.yhscx.wfwz.wfwzcx%22,%22tid%22:%22+%22,%22version%22:%22%22%7D,%22body%22:%7B%22ajdjrqq%22:%22{year}-01-01%22,%22ajdjrqz%22:%22{year}-12-31%22,%22s2id_autogen1%22:%22%22,%22s2id_autogen1_search%22:%22%22,%22ajzt%22:%22%22,%22s2id_autogen2%22:%22%22,%22s2id_autogen2_search%22:%22%22,%22clzt%22:%22%22%7D%7D%7D&gdslxDm=1"
        response = await fetch(url, self, session)
        data = response.json
        result_list_dict = data["taxML"]["body"]["taxML"]["wfwzxxList"]["wfwzxx"]
        if result_list_dict:
            for result in result_list_dict:
                inspection_info = InspectionInfo()
                inspection_info.illegal_facts = result["wfss"]
                inspection_info.start_at = result["ssqjq"]
                inspection_info.end_at = result["ssqjz"]
                inspection_info.r_data = result["djrq"]
                inspection_info.status_tax_illegal = result["ajzt"]
                self.inspection.inspectionInfo.append(inspection_info)

    @create_inst(cls_names=[cr.INVOICEINFORMATION],
                 attrs=[('invoiceInformation',)])
    async def get_invoice_details(self, session, year, fplxdm):
        try:
            start_date = str(year) + "-01-01"
            end_date = str(year) + "-12-31"
            url = f"https://etax.fujian.chinatax.gov.cn/tycx-cjpt-web/cxpt/query.do?&bw=%7B%22taxML%22:%7B%22head%22:%7B%22gid%22:%22311085A116185FEFE053C2000A0A5B63%22,%22sid%22:%22dzswj.yhscx.fpxxcx%22,%22tid%22:%22+%22,%22version%22:%22%22%7D,%22body%22:%7B%22s2id_autogen1%22:%22%22,%22fplxdm%22:%22{fplxdm}%22,%22fpdm%22:%22%22,%22fphm%22:%22%22,%22kprqq%22:%22{start_date}%22,%22kprqz%22:%22{end_date}%22,%22endRow%22:%22{'50000'}%22,%22startRow%22:%22{'1'}%22%7D%7D%7D&gdslxDm=1"  # ,%22kpyf%22:%22{'201905'}%22
            response = await fetch(url, self, session)
            data = response.json
            fpxx_list = data.get("taxML").get("body").get("fpxx", [])
            if len(fpxx_list) > 0:
                for fp_obj in fpxx_list:
                    invoice_info = InvoiceInformationInfo()
                    invoice_info.invoice_typeName = fp_obj.get("fpzlmc", "")
                    invoice_info.invoice_code = fp_obj.get("fpdm", "")
                    invoice_info.opening_date = fp_obj.get("kprq", "")
                    invoice_info.invoice_Number = fp_obj.get("fphm", "")
                    invoice_info.invoice_amount = fp_obj.get("fpje", "")
                    invoice_info.tax_amount = fp_obj.get("se", "")
                    invoice_info.invoice_status = fp_obj.get("fpztmc", "")
                    invoice_info.buyer_name = fp_obj.get("ghfmc", "")
                    invoice_info.buyer_code = fp_obj.get('gfsbh', '')
                    self.invoiceinformation.invoiceInformation.append(invoice_info)
        except:
            import traceback
            print(traceback.format_exc())
