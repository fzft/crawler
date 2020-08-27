# -*- coding: utf-8 -*-
"""
@File    : chongqing.py
@Time    : 2020-06-01 10:16
@Author  : Dingkou
@Email   : dingkou@dachagui.com
@Software: PyCharm
"""
import os, sys, json, traceback
import asyncio
import aiohttp
from settings import BASE_DIR
pdf_path = BASE_DIR + r'/test/tax_test/pdf/'


async def fetch(session, url, headers):
    async with session.get(url=url, headers=headers) as resp:
        return await resp.read()


async def post(session, url, data, headers):
    async with session.post(url=url, data=data, headers=headers) as resp:
        return await resp.text()


async def parse_result(html):
    pass


async def main():
    ret_data = []

    async def fill(yzpzzlMc):
        szlx_lst = ["增值税", "企业所得税", "印花税"]
        return list(filter(lambda x: x in yzpzzlMc, szlx_lst))

    async with aiohttp.ClientSession() as session:
        # query_url = 'https://etax.chongqing.chinatax.gov.cn:6001/ajax.sword?ctrl=SB702SbdyCtrl_querySbbxx&9K' \
        #             'KukoOt=405nND1B1F0Xpch6X9xixy1riHHXmZ7tVvjkiCzpXT.2cg9bcQ3v61fUW3QboXlm1Mji.OVKKUAk61f6f' \
        #             'zAGZAIPaEBpbNMIZGRpxzHCyg9p_J_BYEPeZoXgZbZOI0q2uoqnCcl84hJ0cdwuC8pGOYwGskj.QGjGg19NVJh0Epr' \
        #             'Y4T3AR37C4fVGVZRGhXYfN90pu5YBnALK.5ysGFbOYau6PVKgEl2bdI0aJ4KwFP6IP76aQAOUVxdObLOKuU_CPrD2' \
        #             'H0Pp6uR9Um9eRueJzhwl56tNEvQw08Ad1bT41xNYnZm5KeY15bVfV5oMtzXrJY92aBh1OBlKIXvC6udmXuoTHy1p' \
        #             'SPpvT6GvQQ26waz8EaaFgOT1Q4Ig0HRbh_LropwaOV9Kf.iA9zpNdOczHCyfnpywphtqlsBS4qJ_pamoarUz' \
        #             'z4oNPjzLvNHrOIxCQHyw'
        query_url = 'https://etax.chongqing.chinatax.gov.cn:6001/ajax.sword?ctrl=SB702SbdyCtrl_querySbbxx'
        headers = {
            "Host": "etax.chongqing.chinatax.gov.cn:6001",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://etax.chongqing.chinatax.gov.cn:6001",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://etax.chongqing.chinatax.gov.cn:6001/sword?ctrl=SB702SbdyCtrl_initView&cssParam=vrSY%2FPTwP%2Fxekp8PiLmT6R2asTgOqq%2FcthNlIRQeBXLb9yw0S5pWbFpyK6xWEUtWE5HzPwlRU%2B3CdT0peEDwVpPxOnTp2KwqJQtkzeg%2Fzi8Asw9pZXPxOdxlohospj64JqU%2FBAoXncUF2V4xRtWVAcYMbj%2Fk9b8HWIUNZ5r4zJttokP%2F2DKJgEnVoHlu%2FPhA%2FpTJPrVTye1YUUGv8nhxJ5TwzWg2YdugoeGJ%2BdYXApmXDWIFWJE4YpJLy1sOpfEKBrvMMkeJ%2FASiDfYOziR7uVlQ70iig3zl%2F2MFsm1sZAr1calvBle8r%2FCapmmPzly8FU3vHPytD3eh5aTAcrOBQnPRNxV8ZtOeJWPxViT9foXY1QPEOUftK8mIg%2FD6qKW03ZVtIIgcS7mVJtNKW3hoTA%3D%3D&xtBz=WSBS&r=0.5433847097758615",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "yfx_c_g_u_id_10003718=_ck19101111223315435671951147789; yfx_mr_10003718=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003718=; yfx_c_g_u_id_10003702=_ck19101211270710515445125431533; yfx_c_g_u_id_10001429=_ck19101615105111260230483139122; yfx_mr_10001429=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10001429=; yfx_c_g_u_id_10003139=_ck19101617164219771838858083791; _trs_uv=k1t29vbb_735_h7tk; yfx_mr_10003139=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003139=; yfx_c_g_u_id_10003710=_ck19103114120210119522016535547; yfx_c_g_u_id_10003703=_ck19103114150216525888588966198; yfx_f_l_v_t_10003703=f_t_1572502502647__r_t_1572502502647__v_t_1572502502647__r_c_0; yfx_c_g_u_id_10003709=_ck19103114192710557361921437012; yfx_c_g_u_id_10000015=_ck19110115322110217359697181238; yfx_f_l_v_t_10000015=f_t_1572593541014__r_t_1572593541014__v_t_1572593541014__r_c_0; yfx_mr_10000015=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000015=; yfx_c_g_u_id_10001434=_ck19110711350717937977857953978; yfx_c_g_u_id_10003170=_ck19112016330918933835615490423; yfx_mr_10003170=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003170=; yfx_c_g_u_id_10003717=_ck19112611474211106211372777382; yfx_mr_10003717=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003717=; xqOYlxg4MJSh443S=IekyqtMJMLMaE2pZ.aQpcV9cIatjFiC5E1XadyHS8uHP58ItgJn4Mgoz7FbbXpXO; xqOYlxg4MJSh6011S=yASM0irxgJtsW2WJf2dk.P6GWauP.1g9HPzNqO5xQtwwITqS.VWF56gn2UyAuYI9; xqOYlxg4MJSh6011T=405Ep92qzTI4vD81rMAzpkFe1yd.APl.r4kR6rnmvTMR6JUphd3NdimyltuuLAqO.5nReD_uONyOfnxrKNb1No2WXHW.SLYjtEzbECUdQ2cenOxdqPql9QAHTyHGuA7xVcNY.OcZwfdy7vQhMp4RpnP0O_gu0PN3cY6tNfbj2jddxrbXTs73M3CKrmmuxDDisrwSV16RbEHWOL8phyRyPUGmHiyramwco3uzXk43UrbqLiDVxoQPOFcF9G8pQdQk1qoJUL25uYawU4flZAux1Q7jVmxdodBLyHh6hHhM96AQL8hCmJo.ISZ3rViwyHjr0ANZ4aWvz3FeeZ8uCYcc4ia38Lb3kSP1wlFvO3JDEFaPMzq; yfx_f_l_v_t_10001429=f_t_1571209851120__r_t_1575265004926__v_t_1575265004926__r_c_8; yfx_c_g_u_id_10003677=_ck19122510145710603353361225551; yfx_f_l_v_t_10003170=f_t_1574238789880__r_t_1577331184015__v_t_1577331184015__r_c_5; yfx_mr_10003710=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003710=; yfx_f_l_v_t_10003710=f_t_1572502321999__r_t_1582878535992__v_t_1582878535992__r_c_2; yfx_c_g_u_id_10000080=_ck20030515082919749072595155790; yfx_mr_10000080=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000080=; yfx_f_l_v_t_10003702=f_t_1570850827036__r_t_1584414393627__v_t_1584427312158__r_c_10; yfx_c_g_u_id_10003701=_ck20032717311116592035659018206; yfx_f_l_v_t_10003701=f_t_1585301471498__r_t_1585301471498__v_t_1585301471498__r_c_0; yfx_mr_10003701=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003701=; yfx_c_g_u_id_10003704=_ck20040311122814633775488147329; yfx_mr_10003704=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003704=; yfx_f_l_v_t_10003704=f_t_1585883548439__r_t_1586828736937__v_t_1586828736937__r_c_1; UM_distinctid=1718239747db8-01e4996b8f5c34-404e022c-1fa400-1718239747e48f; yfx_f_l_v_t_10003709=f_t_1572502767044__r_t_1587348523436__v_t_1587348523436__r_c_2; yfx_f_l_v_t_10003677=f_t_1577240097058__r_t_1587550969511__v_t_1587550969511__r_c_4; yfx_c_g_u_id_10003706=_ck20051114224117281538833593150; yfx_mr_10003706=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10003706=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003706=; yfx_f_l_v_t_10003706=f_t_1589178161711__r_t_1589263570815__v_t_1589263570815__r_c_1; yfx_f_l_v_t_10003718=f_t_1570764153538__r_t_1589858236634__v_t_1589858236634__r_c_4; yfx_mr_f_10003718=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_f_l_v_t_10001434=f_t_1577161974165__r_t_1590377102873__v_t_1590377102873__r_c_8; yfx_f_l_v_t_10000080=f_t_1583392109958__r_t_1590386268115__v_t_1590392469177__r_c_5; UqZBpD3n3iXGAwNU9A6lpWmXQPIC8YR0YNbLtw@@=v1XrRag32g2GF; UqZBpD3n3iXPAw1X9A6siXqHXu0fy5FfT8vRspKYpAOV=v1g7RagyeUK69; DZSWJMHSESSIONID=qptvQ_nq6L95ChxSs54jQKkW-tUQ_-koQX3FxYSC0uFZ7VlinGkA!1452204418; dzswj-mh-session-=dzswj-mh-session-46b7f1f6aaa9419aa5b4a0715456d79c; xqOYlxg4MJSh443T=4ScRjIOY75VfSaIvnZHknKO41zuR4Byd3C3.0EBowVaqTrHauIwzmJhxeQe7rNDZMBD0Z.aa_QQQdSqnc58gtX_b6Tgk857RbVpaX5eS50XmnwodhEtEcO2PB85TCWBdT2.H4wquJ_mEX5p9CAs.njgVTYFESnlyfoaJ1ZB8n9B6cH8j22_AJf_NsoFf_ET4vhlE9enOx4jskfd0BPGVaigZAvh_Rm_mwmuK99rkiecGi56saetZoHWuESM19h3ZV1idCu8e.APzpuJVofqE7nEQ8OOBKejWlPXUYk.wIBRrK9r6UT0SgMnyEa0PsBcMaue3uwmQ8pk1jibMXwnmfRRS8xXUeFOEDKsn4LuRlzximiDWJyAYeHiUfLnir5GZUn4Z; YWBLZXT=M8BvRL_PT704uIh0hn7kBgCneyI8w7vhhsyvNm7RN2aDtJ_fXq_5!1776497097; UqZBpD3n3iXHDgBW9A2siXqHXu0fy5FfT8nLtI0@=v1YLRag32gF50; xqOYlxg4MJSh6001S=HKGKCuAUCpVG9TBS4PvWWJjLpcvA9bw8mp3ldXTHL1hrkbaJasbsIfd._Y3ErGkz; xqOYlxg4MJSh6001T=4_J81EfkNVocjWgMYj_Pn6fzTrZc5nIbBNRBTg8eY43xyCUty1.hWQ146KBtZG6NNYRPAzv_zROBWQ1MFOOWo87ihnBBw4i9okr7daBLgjdr15sYcO5Y3JA7ZZCU.P7BrN7UKTD14ma_QyEjOtyVAfxL3r.7GRvh6uY88qvvciivs9zTwkQyh1StBUDuwz4EoHdKIA_7pe6AMG7dHvNa9vBMMfCMJpIgtxxMTFOD7eN_xfM0_ywBXe8mtyJLnNY00XouJ9IWTu8d1e14jiJWS3xuAfNWcIYbI9dgxNG6jzbHmkLmBWKPWapj0NAQzfTI1aauHqbTz6C7_C734JU.yI5E0YLz1oF_ym5_eEyJabB07eXTQNnRDK18PMQTak8yiuBV",

        }
        post_data = '{"tid":"","ctrl":"SB702SbdyCtrl_querySbbxx","data":[{"name":"rqlx","value":"0",' \
                    '"sword":"attr"},{"name":"rq1","value":"2020-01-01","sword":"attr"},' \
                    '{"name":"rq2","value":"2020-06-01","sword":"attr"},' \
                    '{"name":"yzpzzlDm","value":"","sword":"attr"}],"bindParam":true}'
        json_data = await post(session, query_url, {'postData': post_data}, headers)
        # print(json_data)
        json_data = json.loads(json_data)
        print(json_data)
        trs = json_data['data'][0]['trs']
        print(len(trs))
        mc_lst = []
        fill_lst = []

        for tr in trs:
            pzxh = tr['tds']['pzxh'].get('value')
            sbuuid = tr['tds']['sbuuid'].get('value')
            sbrq1 = tr['tds']['sbrq1'].get('value')
            skssqq = tr['tds']['skssqq'].get('value')
            skssqz = tr['tds']['skssqz'].get('value')
            yzpzzlDm = tr['tds']['yzpzzlDm'].get('value')
            yzpzzlMc = tr['tds']['yzpzzlMc'].get('value')
            mc_lst.append(yzpzzlMc)
            ret = await fill(yzpzzlMc)
            if ret:
                fill_lst.append(yzpzzlMc)
                d_project = ret[0]
                print(d_project)
                pdf_url = f'https://etax.chongqing.chinatax.gov.cn:6001/sword?ctrl=SB702SbdyCtrl_openByPzxh' \
                    f'&pzxh={pzxh}' \
                    f'&sbuuid={sbuuid}' \
                    f'&format=PDF&skssqq={skssqq}' \
                    f'&skssqz={skssqz}' \
                    f'&yzpzzlDm={yzpzzlDm}'
                print(pdf_url)
                pdf_headers = {
                    "Host": "etax.chongqing.chinatax.gov.cn:6001",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                    "Referer": "https://etax.chongqing.chinatax.gov.cn:6001/sword?ctrl=SB702SbdyCtrl_initView&cssParam=vrSY%2FPTwP%2Fxekp8PiLmT6R2asTgOqq%2FcthNlIRQeBXLb9yw0S5pWbFpyK6xWEUtWE5HzPwlRU%2B3CdT0peEDwVpPxOnTp2KwqJQtkzeg%2Fzi8Asw9pZXPxOdxlohospj64JqU%2FBAoXncUF2V4xRtWVAcYMbj%2Fk9b8HWIUNZ5r4zJttokP%2F2DKJgEnVoHlu%2FPhA%2FpTJPrVTye1YUUGv8nhxJ5TwzWg2YdugoeGJ%2BdYXApmXDWIFWJE4YpJLy1sOpfEKBrvMMkeJ%2FASiDfYOziR7uVlQ70iig3zl%2F2MFsm1sZAr1calvBle8r%2FCapmmPzly8FU3vHPytD3eh5aTAcrOBQnPRNxV8ZtOeJWPxViT9foXY1QPEOUftK8mIg%2FD6qKW03ZVtIIgcS7mVJtNKW3hoTA%3D%3D&xtBz=WSBS&r=0.5433847097758615",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": "yfx_c_g_u_id_10003718=_ck19101111223315435671951147789; yfx_mr_10003718=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003718=; yfx_c_g_u_id_10003702=_ck19101211270710515445125431533; yfx_c_g_u_id_10001429=_ck19101615105111260230483139122; yfx_mr_10001429=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10001429=; yfx_c_g_u_id_10003139=_ck19101617164219771838858083791; _trs_uv=k1t29vbb_735_h7tk; yfx_mr_10003139=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003139=; yfx_c_g_u_id_10003710=_ck19103114120210119522016535547; yfx_c_g_u_id_10003703=_ck19103114150216525888588966198; yfx_f_l_v_t_10003703=f_t_1572502502647__r_t_1572502502647__v_t_1572502502647__r_c_0; yfx_c_g_u_id_10003709=_ck19103114192710557361921437012; yfx_c_g_u_id_10000015=_ck19110115322110217359697181238; yfx_f_l_v_t_10000015=f_t_1572593541014__r_t_1572593541014__v_t_1572593541014__r_c_0; yfx_mr_10000015=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000015=; yfx_c_g_u_id_10001434=_ck19110711350717937977857953978; yfx_c_g_u_id_10003170=_ck19112016330918933835615490423; yfx_mr_10003170=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003170=; yfx_c_g_u_id_10003717=_ck19112611474211106211372777382; yfx_mr_10003717=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003717=; xqOYlxg4MJSh443S=IekyqtMJMLMaE2pZ.aQpcV9cIatjFiC5E1XadyHS8uHP58ItgJn4Mgoz7FbbXpXO; xqOYlxg4MJSh6011S=yASM0irxgJtsW2WJf2dk.P6GWauP.1g9HPzNqO5xQtwwITqS.VWF56gn2UyAuYI9; xqOYlxg4MJSh6011T=405Ep92qzTI4vD81rMAzpkFe1yd.APl.r4kR6rnmvTMR6JUphd3NdimyltuuLAqO.5nReD_uONyOfnxrKNb1No2WXHW.SLYjtEzbECUdQ2cenOxdqPql9QAHTyHGuA7xVcNY.OcZwfdy7vQhMp4RpnP0O_gu0PN3cY6tNfbj2jddxrbXTs73M3CKrmmuxDDisrwSV16RbEHWOL8phyRyPUGmHiyramwco3uzXk43UrbqLiDVxoQPOFcF9G8pQdQk1qoJUL25uYawU4flZAux1Q7jVmxdodBLyHh6hHhM96AQL8hCmJo.ISZ3rViwyHjr0ANZ4aWvz3FeeZ8uCYcc4ia38Lb3kSP1wlFvO3JDEFaPMzq; yfx_f_l_v_t_10001429=f_t_1571209851120__r_t_1575265004926__v_t_1575265004926__r_c_8; yfx_c_g_u_id_10003677=_ck19122510145710603353361225551; yfx_f_l_v_t_10003170=f_t_1574238789880__r_t_1577331184015__v_t_1577331184015__r_c_5; yfx_mr_10003710=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003710=; yfx_f_l_v_t_10003710=f_t_1572502321999__r_t_1582878535992__v_t_1582878535992__r_c_2; yfx_c_g_u_id_10000080=_ck20030515082919749072595155790; yfx_mr_10000080=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000080=; yfx_f_l_v_t_10003702=f_t_1570850827036__r_t_1584414393627__v_t_1584427312158__r_c_10; yfx_c_g_u_id_10003701=_ck20032717311116592035659018206; yfx_f_l_v_t_10003701=f_t_1585301471498__r_t_1585301471498__v_t_1585301471498__r_c_0; yfx_mr_10003701=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003701=; yfx_c_g_u_id_10003704=_ck20040311122814633775488147329; yfx_mr_10003704=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003704=; yfx_f_l_v_t_10003704=f_t_1585883548439__r_t_1586828736937__v_t_1586828736937__r_c_1; UM_distinctid=1718239747db8-01e4996b8f5c34-404e022c-1fa400-1718239747e48f; yfx_f_l_v_t_10003709=f_t_1572502767044__r_t_1587348523436__v_t_1587348523436__r_c_2; yfx_f_l_v_t_10003677=f_t_1577240097058__r_t_1587550969511__v_t_1587550969511__r_c_4; yfx_c_g_u_id_10003706=_ck20051114224117281538833593150; yfx_mr_10003706=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10003706=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10003706=; yfx_f_l_v_t_10003706=f_t_1589178161711__r_t_1589263570815__v_t_1589263570815__r_c_1; yfx_f_l_v_t_10003718=f_t_1570764153538__r_t_1589858236634__v_t_1589858236634__r_c_4; yfx_mr_f_10003718=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_f_l_v_t_10001434=f_t_1577161974165__r_t_1590377102873__v_t_1590377102873__r_c_8; yfx_f_l_v_t_10000080=f_t_1583392109958__r_t_1590386268115__v_t_1590392469177__r_c_5; UqZBpD3n3iXGAwNU9A6lpWmXQPIC8YR0YNbLtw@@=v1XrRag32g2GF; UqZBpD3n3iXPAw1X9A6siXqHXu0fy5FfT8vRspKYpAOV=v1g7RagyeUK69; DZSWJMHSESSIONID=qptvQ_nq6L95ChxSs54jQKkW-tUQ_-koQX3FxYSC0uFZ7VlinGkA!1452204418; dzswj-mh-session-=dzswj-mh-session-46b7f1f6aaa9419aa5b4a0715456d79c; xqOYlxg4MJSh443T=4ScRjIOY75VfSaIvnZHknKO41zuR4Byd3C3.0EBowVaqTrHauIwzmJhxeQe7rNDZMBD0Z.aa_QQQdSqnc58gtX_b6Tgk857RbVpaX5eS50XmnwodhEtEcO2PB85TCWBdT2.H4wquJ_mEX5p9CAs.njgVTYFESnlyfoaJ1ZB8n9B6cH8j22_AJf_NsoFf_ET4vhlE9enOx4jskfd0BPGVaigZAvh_Rm_mwmuK99rkiecGi56saetZoHWuESM19h3ZV1idCu8e.APzpuJVofqE7nEQ8OOBKejWlPXUYk.wIBRrK9r6UT0SgMnyEa0PsBcMaue3uwmQ8pk1jibMXwnmfRRS8xXUeFOEDKsn4LuRlzximiDWJyAYeHiUfLnir5GZUn4Z; YWBLZXT=M8BvRL_PT704uIh0hn7kBgCneyI8w7vhhsyvNm7RN2aDtJ_fXq_5!1776497097; UqZBpD3n3iXHDgBW9A2siXqHXu0fy5FfT8nLtI0@=v1YLRag32gF50; xqOYlxg4MJSh6001S=HKGKCuAUCpVG9TBS4PvWWJjLpcvA9bw8mp3ldXTHL1hrkbaJasbsIfd._Y3ErGkz; xqOYlxg4MJSh6001T=4mnfz68ZK.geYuo9jYmwJE81t5kerJGRAKbAtofcjlvCDxLTDzV0uOzlENATkIEKKjbwB13m1bQAuOz92QQugfsS0nes4__Yx.d7KR0uSmpNksWuv3adYYKPKDYji1mzU56VUtpYTlEbxS3E6nHw79s_PKObtUGxf0I_YzQKCMO.CiYH3yKO.fXZYEuWzFtYhRa8fnxS7dnbLMtl0fhrfi70fpWym4UpVjBXmuL3hPW.YFoT.Wq1hZdKdqdz0ogbNkOPDQwQORPK7e.XS5kdchu1sntToACdgdAP2To0cLaY2547Pp.pL0VRqEPaxixY5G.dKM.WPQ1iKgQm9qefWRsANOclc96gcn.PJxG07vR4TBkJyX1ngA0n9IuFMVHyMVMV",

                }
                resp_body = await fetch(session, pdf_url, pdf_headers)
                ret_data.append({
                    "d_project": d_project,
                    "declara_date": str(sbrq1).split(' ')[0],
                    "payment_starttime": str(skssqq).split(' ')[0],
                    "payment_endtime": str(skssqz).split(' ')[0],
                    'body': resp_body
                })

        print(mc_lst)
        print(fill_lst)
        print(ret_data)


# def fill(yzpzzlMc):
#     # name = ['《城建税、教育费附加、地方教育附加税（费）申报表》', '《增值税纳税申报表（一般纳税人适用）》', '《城建税、教育费附加、地方教育附加税（费）申报表》', '《增值税纳税申报表（一般纳税人适用）》', '《A200000中华人民共和国企业所得税月（季）度预缴纳税申报表（A类，2018年版）》', '《中华人民共和国企业所得税年度纳税申报表（A类）》（A100000）', '《城建税、教育费附加、地方教育附加税（费）申报表》', '《增值税纳税申报表（一般纳税人适用）》', '《增值税纳税申报表（一般纳税人适用）》', '《城建税、教育费附加、地方教育附加税（费）申报表》', '《城建税、教育费附加、地方教育附加税（费）申报表》', '《A200000中华人民共和国企业所得税月（季）度预缴纳税申报表（A类，2018年版）》', '《增值税纳税申报表（一般纳税人适用）》']
#     szlx_lst = ["增值税", "企业所得税", "印花税"]
#     rest = list(filter(lambda x: x in yzpzzlMc, szlx_lst))
#     print(rest)
#     if rest:
#         return True
#     else:
#         return False


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # fill()
    pass
