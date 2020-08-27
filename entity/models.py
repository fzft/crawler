import time
import asyncio
from collections import namedtuple

from aiomongodel.fields import BoolField
from motor.motor_asyncio import AsyncIOMotorClient
from aiomongodel import *

from core.consistant import MongoConfigParams
from core.core_escache import ICacheItem
import sys

sys.path.append('..')

DeclarationMeta = namedtuple('DeclarationMeta', ['declara_date', 'payment_starttime', 'payment_endtime', 'd_project'])
PdfDeclarationUrlStruct = namedtuple('PdfDeclarationUrlStruct', ['url', 'cookie_jar', 'declarationMeta'])
PdfDeclarationBodyStruct = namedtuple('PdfDeclarationUrlStruct', ['body', 'declarationMeta'])


class Mixin:
    token = StrField(mongo_name='token', default='')
    create_at = StrField(mongo_name='create_at', default='')


class Statistics(Mixin, Document):
    success = BoolField(default=True)
    message = StrField(mongo_name='message', default='200')
    province = StrField(mongo_name='province', default='')
    company_name = StrField(mongo_name='company_name', default='')
    declarationInfo = StrField(mongo_name='declaration_info', default='0')
    inspectionInfo = StrField(mongo_name='inspection_info', default='0')
    invoiceInformation = StrField(mongo_name='invoice_information', default='0')
    person = StrField(mongo_name='person', default='0')
    ratingInfo = StrField(mongo_name='rating_info', default='0')

    class Meta:
        collection = 'statistics'


class Registration(Mixin, Document):
    taxpayer_code = StrField(default='')
    taxpayer_name = StrField(default='')
    operation_address = StrField(default='')
    business_scope = StrField(default='')
    operation_product_address = StrField(default='')
    operation_start_at = StrField(default='')
    operation_end_at = StrField(default='')
    taxpayer_status = StrField(default='')
    taxpayer_qualification = StrField(default='')

    class Meta:
        collection = 'registration'


class DeclarationInfo(EmbeddedDocument):
    declara_date = StrField(default='')
    payment_starttime = StrField(default='')
    payment_endtime = StrField(default='')
    d_project = StrField(default='')
    taxpay_amount = StrField(default='0')  # 应纳税额 taxpay_amount

    # 增值税一般纳税人
    asysljsxse = StrField(default='')  # 按适用税率计税销售额
    yshwxse = StrField(default='')  # 应税货物销售额
    yslwxse = StrField(default='')  # 应税劳务销售额
    syslnsjctzxse = StrField(default='')  # 纳税检查调整的销售额
    ajybfjsxse = StrField(default='')  # 按简易办法计税销售额
    jybfnsjctzxse = StrField(default='')  # 纳税检查调整的销售额
    mdtbfckxse = StrField(default='')  # 免、抵、退办法出口销售额
    msxse = StrField(default='')  # 免税销售额
    mshwxse = StrField(default='')  # 免税货物销售额
    mslwxse = StrField(default='')  # 免税劳务销售额
    xxse = StrField(default='')  # 销项税额
    jxse = StrField(default='')  # 进项税额
    sqldse = StrField(default='')  # 上期留抵税额
    jxsezc = StrField(default='')  # 进项税额转出
    mdtytse = StrField(default='')  # 免、抵、退应退税额
    syslnsjcybjse = StrField(default='')  # 按适用税率计算的纳税检查应补缴税额
    ydksehj = StrField(default='')  # 应抵扣税额合计
    sjdkse = StrField(default='')  # 实际抵扣税额
    ynse = StrField(default='')  # 应纳税额
    qmldse = StrField(default='')  # 期末留抵税额
    jybfynse = StrField(default='')  # 简易计税办法计算的应纳税额
    jybfnsjcybjse = StrField(
        default='')  # 按简易计税办法计算的纳税检查应补缴税额
    ynsejze = StrField(default='')  # 应纳税额减征额
    ynsehj = StrField(default='')  # 应纳税额合计
    qcwjse = StrField(default='')  # 期初未缴税额
    ssckkjzyjkstse = StrField(default='')  # 实收出口开具专用缴款书退税额
    bqyijse = StrField(default='')  # 本期已缴税额
    fcyujse = StrField(default='')  # 分次预缴税额
    ckkjzyjksyjse = StrField(default='')  # 出口开具专用缴款书预缴税额
    bqjnsqynse = StrField(default='')  # 本期缴纳上期应纳税额
    bqjnqjse = StrField(default='')  # 本期缴纳欠缴税额
    qmwjse = StrField(default='')  # 期末未缴税额
    qjsh = StrField(default='')  # 欠缴税额
    bqybtse = StrField(default='')  # 本期应补(退)税额
    jzjtsjtse = StrField(default='')  # 即征即退实际退税额
    qcwjcbse = StrField(
        default='')  # 期初未缴查补税额
    bqrkcbse = StrField(
        default='')  # 本期入库查补税额
    qmwjcbse = StrField(
        default='')  # 期末未缴查补税额

    # 增值税小规模纳税人
    yzzzsbhxse_3 = StrField(default='')  # 应征增值税不含税销售额（3%征收率）
    swjgdkzpbhxse_3 = StrField(default='')  # 税务机关代开的增值税专用发票不含税销售额
    skqkjppbhxse_3 = StrField(default='')  # 税控器具开具的普通发票不含税销售额
    yzzzsbhxse_5 = StrField(default='')  # （二）应征增值税不含税销售额（5%征收率）
    swjgdkzpbhxse_5 = StrField(default='')  # 税务机关代开的增值税专用发票不含税销售额
    skqkjppbhxse_5 = StrField(default='')  # 税控器具开具的普通发票不含税销售额
    xxsygdzcbhxse = StrField(default='')  # "（三）销售使用过的固定资产不含税销售额"
    skqkjppbhxse_gdzc = StrField(default='')  # 其中：税控器具开具的普通发票不含税销售额
    msxse = StrField(default='')  # （四）免税销售额
    xwqymsxse = StrField(default='')  # 其中：小微企业免税销售额
    wdqzdxse = StrField(default='')  # 未达起征点销售额
    qtmsxse = StrField(default='')  # 其他免税销售额
    ckmsxse = StrField(default='')  # （五）出口免税销售额
    skqkjppbhxse_ckms = StrField(default='')  # 其中：税控器具开具的普通发票销售额
    bqynse = StrField(default='')  # 本期应纳税额
    bqynsejze = StrField(default='')  # 本期应纳税额减征额
    bqmse = StrField(default='')  # 本期免税额
    xwqymse = StrField(default='')  # 其中：小微企业免税额
    wdqzdmse = StrField(default='')  # 未达起征点免税额
    ynsehj = StrField(default='')  # 应纳税额合计
    bqyujse = StrField(default='')  # 本期预缴税额
    bqybtse = StrField(default='')  # 本期应补（退）税额

    # 企业所得税月季度报表 A类 2015
    yysr = StrField(default='')  # 营业收入
    yycb = StrField(default='')  # 营业成本
    lrze = StrField(default='')  # 利润总额
    tdywynsde = StrField(default='')  # 特定业务计算的应纳税所得额
    bzssrhsjjmynsde = StrField(default='')  # 不征税收入
    gdzcjszjkctje = StrField(default='')  # 固定资产加速折旧(扣除)调减额
    mbyqndks = StrField(default='')  # 弥补以前年度亏损
    sjlre = StrField(default='')  # 实际利润额
    sl = StrField(default='')  # 税率
    ynsdse = StrField(default='')  # 应纳所得税额
    jmsdse = StrField(default='')  # 减免所得税额
    sjyyujsdse = StrField(default='')  # 实际已缴纳所得税额
    tdywyujzsdse = StrField(default='')  # 特定业务预缴(征)所得税额
    ybtsdse = StrField(default='')  # 本期应补(退)所得税额
    yqnddjbqdjsdse = StrField(default='')  # 减：以前年度多缴在本期抵缴所得税额
    byjsjybtsdse = StrField(default='')  # 本月（季）实际应补（退）所得税额
    synsndynsde = StrField(default='')  # 上一纳税年度应纳税所得额
    byjynsde = StrField(default='')  # 本月（季）应纳税所得额
    sl = StrField(default='')  # 税率(25%)
    byjynsdse = StrField(default='')  # 本月（季）应纳所得税额
    jmsdse = StrField(default='')  # 减：减免所得税额
    byjsjynsdse = StrField(default='')  # 本月（季）实际应纳所得税额
    byjswjgqdyujsdse = StrField(default='')  # 本月（季）税务机关确定的预缴所得税额

    # 企业所得税月季度申报表（A类，2018）
    yysr = StrField(default='')  # 营业收入
    yycb = StrField(default='')  # 营业成本
    lrze = StrField(default='')  # 利润总额
    tdywynsde = StrField(default='')  # 特定业务计算的应纳税所得额
    bzssr = StrField(default='')  # 不征税收入
    msjjsdjmyhje = StrField(default='')  # 减：免税收入、减计收入、所得减免等优惠金额
    gdzcjszjkctje = StrField(default='')  # 减：固定资产加速折旧（扣除）调减额
    mbyqndks = StrField(default='')  # 减：弥补以前年度亏损
    sjlre = StrField(default='')  # 实际利润额 \ 按照上一纳税年度应纳税所得额平均额确定的应纳税所得额
    sl = StrField(default='')  # 税率(25%)
    ynsdse = StrField(default='')  # 应纳所得税额
    jmsdse = StrField(default='')  # 减：减免所得税额
    sjyjnsdse = StrField(default='')  # 减：实际已缴纳所得税额
    tdywyujzsdse = StrField(default='')  # 减：特定业务预缴（征）所得税额
    bqybtsdse = StrField(default='')  # 本期应补（退）所得税额 \ 税务机关确定的本期应纳所得税额

    # 企业所得税年度申报表（A类，2014）
    yysr = StrField(default='')  # 营业收入
    yycb = StrField(default='')  # 营业成本
    yysjjfj = StrField(default='')  # 营业税金及附加
    xsfy = StrField(default='')  # 销售费用
    glfy = StrField(default='')  # 管理费用
    cwfy = StrField(default='')  # 财务费用
    zcjzss = StrField(default='')  # 资产减值损失
    gyjzbdsy = StrField(default='')  # 加：公允价值变动收益
    tzsy = StrField(default='')  # 投资收益
    yylr = StrField(default='')  # 二、营业利润
    yywsr = StrField(default='')  # 加：营业外收入
    yywzc = StrField(default='')  # 减：营业外支出
    lrze = StrField(default='')  # 三、利润总额
    jwsd = StrField(default='')  # 减：境外所得
    nstzzje = StrField(default='')  # 加：纳税调整增加额
    nstzjse = StrField(default='')  # 减：纳税调整减少额
    msjjsrjjkc = StrField(default='')  # 减：免税、减计收入及加计扣除
    jwyssddjjnks = StrField(default='')  # 加：境外应税所得抵减境内亏损
    nstzhsd = StrField(default='')  # 四、纳税调整后所得
    sdjm = StrField(default='')  # 减：所得减免
    dkynssde = StrField(default='')  # 减：抵扣应纳税所得额
    mbyqndks = StrField(default='')  # 减：弥补以前年度亏损
    ynssde = StrField(default='')  # 五、应纳税所得额
    sl = StrField(default='')  # 税率（25%）
    ynsdse = StrField(default='')  # 六、应纳所得税额
    jmsdse = StrField(default='')  # 减：减免所得税额
    dmsdse = StrField(default='')  # 减：抵免所得税额
    ynse = StrField(default='')  # 七、应纳税额
    jwsdynsdse = StrField(default='')  # 加：境外所得应纳所得税额
    jwsddmsdse = StrField(default='')  # 减：境外所得抵免所得税额
    sjynsdse = StrField(default='')  # 八、实际应纳所得税额
    bnljsjyyujsdse = StrField(default='')  # 减：本年累计实际已预缴的所得税额
    bnybtsdse = StrField(default='')  # 九、本年应补（退）所得税额
    zjgftbnybtsdse = StrField(default='')  # 其中：总机构分摊本年应补（退）所得税额
    czjzfpbnybtsdse = StrField(default='')  # 财政集中分配本年应补（退）所得税额
    zjgztjybmftbnybtsdse = StrField(default='')  # 总机构主体生产经营部门分摊本年应补（退）所得税额

    # 企业所得税年度申报表（A类，2017）
    yysr = StrField(default='')  # 营业收入
    yycb = StrField(default='')  # 营业成本
    yysjjfj = StrField(default='')  # 营业税金及附加
    xsfy = StrField(default='')  # 销售费用
    glfy = StrField(default='')  # 管理费用
    cwfy = StrField(default='')  # 财务费用
    zcjzss = StrField(default='')  # 资产减值损失
    gyjzbdsy = StrField(default='')  # 加：公允价值变动收益
    tzsy = StrField(default='')  # 投资收益
    yylr = StrField(default='')  # 二、营业利润
    yywsr = StrField(default='')  # 加：营业外收入
    yywzc = StrField(default='')  # 减：营业外支出
    lrze = StrField(default='')  # 三、利润总额
    jwsd = StrField(default='')  # 减：境外所得
    nstzzje = StrField(default='')  # 加：纳税调整增加额
    nstzjse = StrField(default='')  # 减：纳税调整减少额
    msjjsrjjkc = StrField(default='')  # 减：免税、减计收入及加计扣除
    jwyssddjjnks = StrField(default='')  # 加：境外应税所得抵减境内亏损
    nstzhsd = StrField(default='')  # 四、纳税调整后所得
    sdjm = StrField(default='')  # 减：所得减免
    dkynssde = StrField(default='')  # 减：抵扣应纳税所得额
    mbyqndks = StrField(default='')  # 减：弥补以前年度亏损
    ynssde = StrField(default='')  # 五、应纳税所得额
    sl = StrField(default='')  # 税率（25%）
    ynsdse = StrField(default='')  # 六、应纳所得税额
    jmsdse = StrField(default='')  # 减：减免所得税额
    dmsdse = StrField(default='')  # 减：抵免所得税额
    ynse = StrField(default='')  # 七、应纳税额
    jwsdynsdse = StrField(default='')  # 加：境外所得应纳所得税额
    jwsddmsdse = StrField(default='')  # 减：境外所得抵免所得税额
    sjynsdse = StrField(default='')  # 八、实际应纳所得税额
    bnljsjyyujsdse = StrField(default='')  # 减：本年累计实际已预缴的所得税额
    bnybtsdse = StrField(default='')  # 九、本年应补（退）所得税额
    zjgftbnybtsdse = StrField(default='')  # 其中：总机构分摊本年应补（退）所得税额
    czjzfpbnybtsdse = StrField(default='')  # 财政集中分配本年应补（退）所得税额
    zjgztjybmftbnybtsdse = StrField(default='')  # 总机构主体生产经营部门分摊本年应补（退）所得税额

    # 企业所得税申报表（B类，2015）
    srze = StrField(default='')  # 收入总额
    bzssr = StrField(default='')  # 减：不征税收入
    mssr = StrField(default='')  # 免税收入
    gzlxsr = StrField(default='')  # 其中:国债利息收入
    dfzfzqlxsr = StrField(default='')  # 地方政府债券利息收入
    jmqyjqyxsy = StrField(default='')  # 符合条件居民企业之间股息红利等权益性收益
    fhtjfylzzsr = StrField(default='')  # 符合条件的非营利组织收入
    qtmssr = StrField(default='')  # 其他免税收入
    ynsre = StrField(default='')  # 应税收入额
    yssdl = StrField(default='')  # 税务机关核定的应税所得率（%）
    srzehdynssde = StrField(default='')  # 应纳税所得额(按收入总额核定应纳税所得额)
    cbfyze = StrField(default='')  # 成本费用总额
    yssdl = StrField(default='')  # 税务机关核定的应税所得率（%）
    cbfyhdynssde = StrField(default='')  # 应纳税所得额(按成本费用核定应纳税所得额)
    sl = StrField(default='')  # 税率（25%）
    ynsdse = StrField(default='')  # 应纳所得税额
    fhtjxxwlqyjmsdse = StrField(default='')  # 减：符合条件的小型微利企业减免所得税额
    jbzs = StrField(default='')  # 其中：减半征税
    yyujsdse = StrField(default='')  # 已预缴所得税额
    ybtsdse = StrField(default='')  # 应补（退）所得税额

    # 企业所得税申报表（B类，2018）
    srze = StrField(default='')  # 收入总额
    bzssr = StrField(default='')  # 减：不征税收入
    mssr = StrField(default='')  # 免税收入
    gzlxsr = StrField(default='')  # 其中:国债利息收入
    jmqyjqyxtzsy = StrField(default='')  # 符合条件的居民企业之间的股息、红利等权益性投资收益免征企业所得税
    hgttzgxhl = StrField(default='')  # 其中：通过沪港通投资且连续持有H股满12个月取得的股息红利所得免征企业所得税
    sgttzgxhl = StrField(default='')  # 通过深港通投资且连续持有H股满12个月取得的股息红利所得免征企业所得税
    cxqygxhl = StrField(default='')  # 居民企业持有创新企业CDR取得的股息红利所得免征企业所得税
    jmqyjyxzlx = StrField(default='')  # 符合条件的居民企业之间属于股息、红利性质的永续债利息收入免征企业所得税
    zqtzjjfpsr = StrField(default='')  # 投资者从证券投资基金分配中取得的收入免征企业所得税
    dfzfzqlxsr = StrField(default='')  # 取得的地方政府债券利息收入免征企业所得税
    ynsre = StrField(default='')  # 应税收入额 \ 成本费用总额
    yssdl = StrField(default='')  # 税务机关核定的应税所得率（%）
    ynssde = StrField(default='')  # 应纳税所得额
    sl = StrField(default='')  # 税率（25%）
    ynssde = StrField(default='')  # 应纳所得税额
    fhtjxxwlqyjmqysds = StrField(default='')  # 减：符合条件的小型微利企业减免企业所得税
    sjyjnsdse = StrField(default='')  # 减：实际已缴纳所得税额
    bqybtsdse = StrField(default='')  # 本期应补（退）所得税额 \ 税务机关核定本期应纳所得税额
    mzzhjzmz = StrField(default='')  # 民族自治地方的自治机关对本民族自治地方的企业应缴纳的企业所得税中属于地方分享的部分减征或免征
    bqsjybtsdse = StrField(default='')  # 本期实际应补（退）所得税额

    # 印花税
    yspz = StrField(default='')  # 应税凭证
    jsjejs = StrField(default='')  # 计税金额或件数
    hdyj = StrField(default='')  # 核定依据
    hdbl = StrField(default='')  # 核定比例
    sysl = StrField(default='')  # 适用税率
    bqynse = StrField(default='')  # 本期应纳税额
    bqyijse = StrField(default='')  # 本期已交税额
    jmxzdm = StrField(default='')  # 减免性质代码
    jme = StrField(default='')  # 减免额
    bqybtse = StrField(default='')  # 本期应补（退）税额


class Declaration(Mixin, Document):
    declarationInfo = ListField(EmbDocField(DeclarationInfo), default=lambda: list(), mongo_name='declarationInfo')

    class Meta:
        collection = 'declaration'


class RatingInfo(EmbeddedDocument):
    appraisal_year = StrField(default='')
    evaluation_score = StrField(default='')
    evaluation_result = StrField(default='')


class Rating(Mixin, Document):
    ratingInfo = ListField(EmbDocField(RatingInfo), mongo_name='ratingInfo', default=lambda: list())

    class Meta:
        collection = 'rating'


class InspectionInfo(EmbeddedDocument):
    illegal_facts = StrField(default='')
    r_data = StrField(default='')
    start_at = StrField(default='')
    end_at = StrField(default='')
    status_tax_illegal = StrField(default='')


class Inspection(Mixin, Document):
    inspectionInfo = ListField(EmbDocField(InspectionInfo), default=lambda: list(), mongo_name='inspectionInfo')

    class Meta:
        collection = 'inspection'


class InvoiceInformationInfo(EmbeddedDocument):
    invoice_code = StrField(default='')
    invoice_Number = StrField(default='')
    opening_date = StrField(default='')
    buyer_name = StrField(default='')
    buyer_code = StrField(default='')
    invoice_amount = StrField(default='')
    tax_amount = StrField(default='')
    invoice_status = StrField(default='')
    invoice_typeName = StrField(default='')

    def __eq__(self, other):
        if self.invoice_code == other.invoice_code and self.invoice_Number == other.invoice_Number and \
                self.opening_date == other.opening_date and self.buyer_name == other.buyer_name and self.buyer_code == other.buyer_code \
                and self.invoice_amount == other.invoice_amount and self.tax_amount == other.tax_amount and self.invoice_status == other.invoice_status and \
                self.invoice_typeName == other.invoice_typeName:
            return True
        return False

    def __hash__(self):
        return hash(
            self.buyer_code + self.invoice_Number + self.opening_date + self.buyer_name + self.buyer_code + self.invoice_amount + self.tax_amount + self.invoice_status + self.invoice_typeName)


class InvoiceInformation(Mixin, Document):
    invoiceInformation = ListField(EmbDocField(InvoiceInformationInfo), default=lambda: list(),
                                   mongo_name='invoiceInformation')

    class Meta:
        collection = 'invoice_information'


class PersonInfo(EmbeddedDocument):
    programe_cont = StrField(default='')
    manager_name = StrField(default='')


class Person(Mixin, Document):
    person = ListField(EmbDocField(PersonInfo), default=lambda: list(), mongo_name='person')

    class Meta:
        collection = 'person'
