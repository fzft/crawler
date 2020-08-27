# -*- coding:utf-8 -*-
import asyncio
import base64
import pprint

import demjson
import requests

import re
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
ss = {
	"message": "{\"message\":\"调用接口成功！\",\"success\":true,\"ywbw\":\"<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\" standalone=\\\"yes\\\"?><taxML xsi:type=\\\"HXZGSB00789Response\\\" xmlns=\\\"http:\/\/www.chinatax.gov.cn\/dataspec\/\\\" xmlns:xsi=\\\"http:\/\/www.w3.org\/2001\/XMLSchema-instance\\\"><sbxxGrid><sbxxGridlb><zsxmDm>10101<\/zsxmDm><zspmDm>101017570<\/zspmDm><hyDm>6210<\/hyDm><nsqxDm>08<\/nsqxDm><zsdlfsDm>0<\/zsdlfsDm><jkqxDm>04<\/jkqxDm><sbqxDm>04<\/sbqxDm><skssqq>2020-01-01<\/skssqq><skssqz>2020-03-31<\/skssqz><djzclxDm>411<\/djzclxDm><sbqx>2020-04-24<\/sbqx><sl1>0.06<\/sl1><zsl>0.03<\/zsl><zgswskfjDm>11403032500<\/zgswskfjDm><swjgDm>11400000000<\/swjgDm><yjse>0.0<\/yjse><rdzsuuid>0<\/rdzsuuid><rdpzuuid>80464725504B7DD7E0530100007FEAC2<\/rdpzuuid><zfsbz>0<\/zfsbz><ysbje>0.0<\/ysbje><sfysb xsi:nil=\\\"true\\\"\/><rdyxqq>2019-01-01 00:00:00<\/rdyxqq><rdyxqz>9999-12-31 00:00:00<\/rdyxqz><wzsyhdjsyj>0.0<\/wzsyhdjsyj><qzd>0.0<\/qzd><djxh>11140300000000014722<\/djxh><wzsyjsyj>0.0<\/wzsyjsyj><wzsyhdse>0.0<\/wzsyhdse><\/sbxxGridlb><\/sbxxGrid><jmxxGrid><jmxxGridlb><yhpzuuid>11140300000000014722SXA031901021<\/yhpzuuid><djxh>11140300000000014722<\/djxh><jmsspsxDm>SXA031901021<\/jmsspsxDm><zsxmDm>10101<\/zsxmDm><jmqxq>2019-01-01<\/jmqxq><jmqxz>2021-12-31<\/jmqxz><ssjmxzhzDm>0001013611<\/ssjmxzhzDm><jzed>0.0<\/jzed><tdjmBz>0<\/tdjmBz><\/jmxxGridlb><jmxxGridlb><yhpzuuid>11140300000000014722SXA031901038<\/yhpzuuid><djxh>11140300000000014722<\/djxh><jmsspsxDm>SXA031901038<\/jmsspsxDm><zsxmDm>10101<\/zsxmDm><jmqxq>2019-01-01<\/jmqxq><jmqxz>2021-12-31<\/jmqxz><ssjmxzhzDm>0001013610<\/ssjmxzhzDm><jzed>0.0<\/jzed><tdjmBz>0<\/tdjmBz><\/jmxxGridlb><jmxxGridlb><yhpzuuid>11140300000000014722SXA031900832<\/yhpzuuid><djxh>11140300000000014722<\/djxh><jmsspsxDm>SXA031900832<\/jmsspsxDm><zsxmDm>10101<\/zsxmDm><jmqxq>2019-01-01<\/jmqxq><jmqxz>2021-12-31<\/jmqxz><ssjmxzhzDm>0001011814<\/ssjmxzhzDm><jzed>0.0<\/jzed><tdjmBz>1<\/tdjmBz><\/jmxxGridlb><jmxxGridlb><yhpzuuid>11140300000000014722SXA031901022<\/yhpzuuid><djxh>11140300000000014722<\/djxh><jmsspsxDm>SXA031901022<\/jmsspsxDm><zsxmDm>10101<\/zsxmDm><jmqxq>2019-01-01<\/jmqxq><jmqxz>2021-12-31<\/jmqxz><ssjmxzhzDm>0001013613<\/ssjmxzhzDm><jzed>0.0<\/jzed><tdjmBz>1<\/tdjmBz><\/jmxxGridlb><jmxxGridlb><yhpzuuid>11140300000000014722SXA031901039<\/yhpzuuid><djxh>11140300000000014722<\/djxh><jmsspsxDm>SXA031901039<\/jmsspsxDm><zsxmDm>10101<\/zsxmDm><jmqxq>2019-01-01<\/jmqxq><jmqxz>2021-12-31<\/jmqxz><ssjmxzhzDm>0001013612<\/ssjmxzhzDm><jzed>0.0<\/jzed><tdjmBz>1<\/tdjmBz><\/jmxxGridlb><jmxxGridlb><yhpzuuid>11140300000000014722SXA031900831<\/yhpzuuid><djxh>11140300000000014722<\/djxh><jmsspsxDm>SXA031900831<\/jmsspsxDm><zsxmDm>10101<\/zsxmDm><jmqxq>2019-01-01<\/jmqxq><jmqxz>2021-12-31<\/jmqxz><ssjmxzhzDm>0001011813<\/ssjmxzhzDm><jzed>0.0<\/jzed><tdjmBz>0<\/tdjmBz><\/jmxxGridlb><\/jmxxGrid><yjxxGrid\/><zzsxgmnsrqcsxxGrid><zzsxgmnsrqcsxxGridlb><ewblxh>3<\/ewblxh><yzzzsbhsxse>0.0<\/yzzzsbhsxse><swjgdkdzzszyfpbhsxse>0.0<\/swjgdkdzzszyfpbhsxse><skqjkjdptfpbhsxse>0.0<\/skqjkjdptfpbhsxse><xsczbdcbhsxse>0.0<\/xsczbdcbhsxse><swjgdkdzzszyfpbhsxse1>0.0<\/swjgdkdzzszyfpbhsxse1><skqjkjdptfpbhsxse2>0.0<\/skqjkjdptfpbhsxse2><xssygdysgdzcbhsxse>0.0<\/xssygdysgdzcbhsxse><skqjkjdptfpbhsxse1>0.0<\/skqjkjdptfpbhsxse1><msxse>0.0<\/msxse><xwqymsxse>0.0<\/xwqymsxse><wdqzdxse>0.0<\/wdqzdxse><qtmsxse>0.0<\/qtmsxse><ckmsxse>0.0<\/ckmsxse><skqjkjdptfpxse1>0.0<\/skqjkjdptfpxse1><hdxse>0.0<\/hdxse><bqynse>0.0<\/bqynse><hdynse>0.0<\/hdynse><bqynsejze>0.0<\/bqynsejze><bqmse>0.0<\/bqmse><xwqymse>0.0<\/xwqymse><wdqzdmse>0.0<\/wdqzdmse><ynsehj>0.0<\/ynsehj><bqyjse1>0.0<\/bqyjse1><bqybtse>0.0<\/bqybtse><\/zzsxgmnsrqcsxxGridlb><zzsxgmnsrqcsxxGridlb><ewblxh>4<\/ewblxh><yzzzsbhsxse>0.0<\/yzzzsbhsxse><swjgdkdzzszyfpbhsxse>0.0<\/swjgdkdzzszyfpbhsxse><skqjkjdptfpbhsxse>0.0<\/skqjkjdptfpbhsxse><xsczbdcbhsxse>0.0<\/xsczbdcbhsxse><swjgdkdzzszyfpbhsxse1>0.0<\/swjgdkdzzszyfpbhsxse1><skqjkjdptfpbhsxse2>0.0<\/skqjkjdptfpbhsxse2><xssygdysgdzcbhsxse>0.0<\/xssygdysgdzcbhsxse><skqjkjdptfpbhsxse1>0.0<\/skqjkjdptfpbhsxse1><msxse>0.0<\/msxse><xwqymsxse>0.0<\/xwqymsxse><wdqzdxse>0.0<\/wdqzdxse><qtmsxse>0.0<\/qtmsxse><ckmsxse>0.0<\/ckmsxse><skqjkjdptfpxse1>0.0<\/skqjkjdptfpxse1><hdxse>0.0<\/hdxse><bqynse>0.0<\/bqynse><hdynse>0.0<\/hdynse><bqynsejze>0.0<\/bqynsejze><bqmse>0.0<\/bqmse><xwqymse>0.0<\/xwqymse><wdqzdmse>0.0<\/wdqzdmse><ynsehj>0.0<\/ynsehj><bqyjse1>0.0<\/bqyjse1><bqybtse>0.0<\/bqybtse><\/zzsxgmnsrqcsxxGridlb><\/zzsxgmnsrqcsxxGrid><sbZzsxgmnsrqtxxVO><zzsqzd>300000.0<\/zzsqzd><zzsysfwqzd>300000.0<\/zzsysfwqzd><yshwlwBz>N<\/yshwlwBz><ysfwBz>Y<\/ysfwBz><yshwlwFpdkbhsxse>0.0<\/yshwlwFpdkbhsxse><ysfwFpdkbhsxse>0.0<\/ysfwFpdkbhsxse><dqdeBz>N<\/dqdeBz><dqdeYshwlwHdxse>0.0<\/dqdeYshwlwHdxse><dqdeYsfwHdxse>0.0<\/dqdeYsfwHdxse><dqdeYshwlwHdynse>0.0<\/dqdeYshwlwHdynse><dqdeYsfwHdynse>0.0<\/dqdeYsfwHdynse><zfjgBz>2<\/zfjgBz><yzl>0.0<\/yzl><desl1>0.0<\/desl1><fgdqyBz>N<\/fgdqyBz><fzjgfgdqyse>0.0<\/fzjgfgdqyse><flzlqcye>0.0<\/flzlqcye><qmsezzsskxtfy5>0.0<\/qmsezzsskxtfy5><qmsefzjgyzjnsk5>0.0<\/qmsefzjgyzjnsk5><qmsejzfwyzjnsk5>0.0<\/qmsejzfwyzjnsk5><qmsexsbdcyzjnsk5>0.0<\/qmsexsbdcyzjnsk5><qmseczbdcyzjnsk5>0.0<\/qmseczbdcyzjnsk5><yqwrdzzsybnsrBz>N<\/yqwrdzzsybnsrBz><ptfpsjkpje>18675.54<\/ptfpsjkpje><iswkjfpsqd>N<\/iswkjfpsqd><fqmsqBz>Y<\/fqmsqBz><\/sbZzsxgmnsrqtxxVO><zzssyyxgmnsrySbSbbdxxVO><zzssyyxgmnsr><sbbhead><nsrsbh>92140303MA0H4RW44L<\/nsrsbh><nsrmc>阳泉市矿区最爱妈妈菜之传奇味道餐饮店<\/nsrmc><skssqq>2020-01-01<\/skssqq><skssqz>2020-03-31<\/skssqz><sbsxDm1>11<\/sbsxDm1><sbrq1>2020-05-08<\/sbrq1><\/sbbhead><zzsxgmGrid><zzsxgmGridlb><ewblxh>1<\/ewblxh><lmc>应税货物及劳务本期数<\/lmc><yzzzsbhsxse>0.0<\/yzzzsbhsxse><swjgdkdzzszyfpbhsxse>0.0<\/swjgdkdzzszyfpbhsxse><skqjkjdptfpbhsxse>0.0<\/skqjkjdptfpbhsxse><xsczbdcbhsxse>0.0<\/xsczbdcbhsxse><swjgdkdzzszyfpbhsxse1>0.0<\/swjgdkdzzszyfpbhsxse1><skqjkjdptfpbhsxse2>0.0<\/skqjkjdptfpbhsxse2><xssygdysgdzcbhsxse>0.0<\/xssygdysgdzcbhsxse><skqjkjdptfpbhsxse1>0.0<\/skqjkjdptfpbhsxse1><msxse>0.0<\/msxse><xwqymsxse>0.0<\/xwqymsxse><wdqzdxse>0.0<\/wdqzdxse><qtmsxse>0.0<\/qtmsxse><ckmsxse>0.0<\/ckmsxse><skqjkjdptfpxse1>0.0<\/skqjkjdptfpxse1><hdxse>0.0<\/hdxse><bqynse>0.0<\/bqynse><hdynse>0.0<\/hdynse><bqynsejze>0.0<\/bqynsejze><bqmse>0.0<\/bqmse><xwqymse>0.0<\/xwqymse><wdqzdmse>0.0<\/wdqzdmse><ynsehj>0.0<\/ynsehj><bqyjse1>0.0<\/bqyjse1><bqybtse>0.0<\/bqybtse><bdcxse>0.0<\/bdcxse><\/zzsxgmGridlb><zzsxgmGridlb><ewblxh>2<\/ewblxh><lmc>应税服务本期数<\/lmc><yzzzsbhsxse>0.0<\/yzzzsbhsxse><swjgdkdzzszyfpbhsxse>0.0<\/swjgdkdzzszyfpbhsxse><skqjkjdptfpbhsxse>0.0<\/skqjkjdptfpbhsxse><xsczbdcbhsxse>0.0<\/xsczbdcbhsxse><swjgdkdzzszyfpbhsxse1>0.0<\/swjgdkdzzszyfpbhsxse1><skqjkjdptfpbhsxse2>0.0<\/skqjkjdptfpbhsxse2><xssygdysgdzcbhsxse>0.0<\/xssygdysgdzcbhsxse><skqjkjdptfpbhsxse1>0.0<\/skqjkjdptfpbhsxse1><msxse>36000.0<\/msxse><xwqymsxse>0.0<\/xwqymsxse><wdqzdxse>36000.0<\/wdqzdxse><qtmsxse>0.0<\/qtmsxse><ckmsxse>0.0<\/ckmsxse><skqjkjdptfpxse1>0.0<\/skqjkjdptfpxse1><hdxse>0.0<\/hdxse><bqynse>0.0<\/bqynse><hdynse>0.0<\/hdynse><bqynsejze>0.0<\/bqynsejze><bqmse>1080.0<\/bqmse><xwqymse>0.0<\/xwqymse><wdqzdmse>1080.0<\/wdqzdmse><ynsehj>0.0<\/ynsehj><bqyjse1>0.0<\/bqyjse1><bqybtse>0.0<\/bqybtse><bdcxse>0.0<\/bdcxse><\/zzsxgmGridlb><zzsxgmGridlb><ewblxh>3<\/ewblxh><lmc>应税货物及劳务本年累计<\/lmc><yzzzsbhsxse>0.0<\/yzzzsbhsxse><swjgdkdzzszyfpbhsxse>0.0<\/swjgdkdzzszyfpbhsxse><skqjkjdptfpbhsxse>0.0<\/skqjkjdptfpbhsxse><xsczbdcbhsxse>0.0<\/xsczbdcbhsxse><swjgdkdzzszyfpbhsxse1>0.0<\/swjgdkdzzszyfpbhsxse1><skqjkjdptfpbhsxse2>0.0<\/skqjkjdptfpbhsxse2><xssygdysgdzcbhsxse>0.0<\/xssygdysgdzcbhsxse><skqjkjdptfpbhsxse1>0.0<\/skqjkjdptfpbhsxse1><msxse>0.0<\/msxse><xwqymsxse>0.0<\/xwqymsxse><wdqzdxse>0.0<\/wdqzdxse><qtmsxse>0.0<\/qtmsxse><ckmsxse>0.0<\/ckmsxse><skqjkjdptfpxse1>0.0<\/skqjkjdptfpxse1><hdxse>0.0<\/hdxse><bqynse>0.0<\/bqynse><hdynse>0.0<\/hdynse><bqynsejze>0.0<\/bqynsejze><bqmse>0.0<\/bqmse><xwqymse>0.0<\/xwqymse><wdqzdmse>0.0<\/wdqzdmse><ynsehj>0.0<\/ynsehj><bqyjse1>0.0<\/bqyjse1><bqybtse>0.0<\/bqybtse><bdcxse>0.0<\/bdcxse><\/zzsxgmGridlb><zzsxgmGridlb><ewblxh>4<\/ewblxh><lmc>应税服务本年累计<\/lmc><yzzzsbhsxse>0.0<\/yzzzsbhsxse><swjgdkdzzszyfpbhsxse>0.0<\/swjgdkdzzszyfpbhsxse><skqjkjdptfpbhsxse>0.0<\/skqjkjdptfpbhsxse><xsczbdcbhsxse>0.0<\/xsczbdcbhsxse><swjgdkdzzszyfpbhsxse1>0.0<\/swjgdkdzzszyfpbhsxse1><skqjkjdptfpbhsxse2>0.0<\/skqjkjdptfpbhsxse2><xssygdysgdzcbhsxse>0.0<\/xssygdysgdzcbhsxse><skqjkjdptfpbhsxse1>0.0<\/skqjkjdptfpbhsxse1><msxse>36000.0<\/msxse><xwqymsxse>0.0<\/xwqymsxse><wdqzdxse>36000.0<\/wdqzdxse><qtmsxse>0.0<\/qtmsxse><ckmsxse>0.0<\/ckmsxse><skqjkjdptfpxse1>0.0<\/skqjkjdptfpxse1><hdxse>0.0<\/hdxse><bqynse>0.0<\/bqynse><hdynse>0.0<\/hdynse><bqynsejze>0.0<\/bqynsejze><bqmse>1080.0<\/bqmse><xwqymse>0.0<\/xwqymse><wdqzdmse>1080.0<\/wdqzdmse><ynsehj>0.0<\/ynsehj><bqyjse1>0.0<\/bqyjse1><bqybtse>0.0<\/bqybtse><bdcxse>0.0<\/bdcxse><\/zzsxgmGridlb><\/zzsxgmGrid><slxxForm><sfzxsb>Y<\/sfzxsb><fddbrxm>王传科<\/fddbrxm><blrysfzjlxDm>201<\/blrysfzjlxDm><blrysfzjhm>140311197901111516<\/blrysfzjhm><slswjgMc>国家税务总局阳泉市矿区税务局第一税务分局<\/slswjgMc><slrxm>赵维维<\/slrxm><slrq>2020-05-08<\/slrq><\/slxxForm><\/zzssyyxgmnsr><zzsxgmflzl\/><jdclscqyxsmxb\/><jdcxstyfpqdb\/><dlqyzzsxxsehjxsecdd\/><zzsxgmfjssb><xgmfjsxxGrid\/><\/zzsxgmfjssb><zzsjmssbmxb\/><\/zzssyyxgmnsrySbSbbdxxVO><\/taxML>\"}",
	"success": True
}
if __name__ == '__main__':
    headers = {
        'Cookie' : "yfx_c_g_u_id_10003702=_ck20040816263717035793815613598; yfx_c_g_u_id_10003710=_ck20040818085714105577386963875; yfx_mr_10003710=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003710=; UM_distinctid=171594831ad53e-0cd564188520ec-396d7500-fa000-171594831ae698; yfx_c_g_u_id_10000056=_ck20040911291011459113688577001; yfx_f_l_v_t_10000056=f_t_1586402950131__r_t_1586402950131__v_t_1586420757827__r_c_0; yfx_mr_10000056=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000056=; yfx_c_g_u_id_10003139=_ck20041614542112216072277311470; yfx_f_l_v_t_10003139=f_t_1587020061210__r_t_1587020061210__v_t_1587020061210__r_c_0; _trs_uv=k92eroh1_735_a7qt; yfx_f_l_v_t_10003710=f_t_1587442002242__r_t_1589340199497__v_t_1589340199497__r_c_1; yfx_mr_f_10003710=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_f_l_v_t_10003702=f_t_1586334397692__r_t_1590811293899__v_t_1590811293899__r_c_7; yfx_c_g_u_id_10003721=_ck20060111472517831972541916571; yfx_mr_10003721=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10003721=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003721=; yfx_f_l_v_t_10003721=f_t_1590983245775__r_t_1590983245775__v_t_1590991798994__r_c_0; LESB_SESSION=YiB4C1dMFgMjfQpReBdk8K_ZJR5ND6HfFWauZ4cCzGb1WibC4m2r!-1113978206; sto-id-20480=BGGFGIAKLPBL; lnReGnsFlag=0; user=91640100574874698D@; dlbzCookie=Y; lnSyTsFlag=1; SSOTicket=5624c507-b2b6-4357-8d68-92f88cd8b23d; tbbysb=Y; tbzbsy=Y",
    }
    resp = requests.post('https://etax.ningxia.chinatax.gov.cn/ajax.sword?r=0.15316773237067283&rUUID=onhma8GJAJHm3oaHMqoXb51zAtjdKxKO&gwssswjg=16401061800',
                         data={
                             'postData':"""{"tid":"","ctrl":"FP024CxzxFpxxCtrl_initQueryFpxxList?rUUID=onhma8GJAJHm3oaHMqoXb51zAtjdKxKO#*^@^*#gwssswjg=16401061800","page":"","data":[{"sword":"SwordForm","name":"cxForm","data":{"zzsfpzl":{"value":"zzszyfp"},"kprqq":{"value":"2019-10-01 11:13:02"},"kprqz":{"value":"2019-12-31 11:13:02"}}},{"name":"fplxmc","value":"增值税专用发票","sword":"attr"}],"bindParam":true}"""
                         },
                         headers=headers

                         )

    print(resp.content)