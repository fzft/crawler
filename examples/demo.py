import redis
import json
import random

# conn = redis.Redis(host='192.168.3.103', port=6379, db=5, password='123456')
# conn = redis.Redis(host='101.37.117.44', port=6379, db=7, password='123456')
# conn = redis.Redis(host='127.0.0.1', port=6379)
# conn = redis.Redis(host='47.98.195.245', port=6379,db=7, password='123456')
conn = redis.Redis(host='101.37.117.44', port=6379, db=8, password='123456')

import uuid

# 18552852069

{
    'token': '123123123',
    "username": "91610131MA6TXFEE94",
    "password": "Kl198467",
    'companyname': '',
    'telephone': '',
    'province': 'Shaanxi',
    'channel_id': '123'
}
# conn.lpush(f'sy:request:{41227101}', f'动态密码_asdasd')
#
# 东莞市荣信皮革制品有限公司
for _ in range(1):
    # data = dict(username='91440300MA5DQJCJ3X111', password='Micro778899', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='深圳市微光视界科技有限公司'
    #             , province='Shenzhen', channel_id='123123', verify_result='123123123123', telephone='13713969846', tax_code='91440300MA5DQJCJ3X')
    data = dict(username='15849133111', password='A000000a', token=
    f'{random.randrange(1000000, 50000000)}', company_name='西安蒯祥建筑工程有限公司'
                , province='Neimeng', channel_id='123123', verify_result='123123123123', telephone='15988345338', tax_code='911501023291180392')
    # data = dict(username='912200001239465170', password='Jl000000', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='吉林省吉峰科贸公司'
    #             , province='Jilin',channel_id='123123',verify_result='123123123123',telephone='18621812013')
    # data = dict(username='91430102597555163G', password='sy627518', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='长沙九维矿业有限公司'
    #             , province='Hunan',channel_id='123123',verify_result='123',telephone='18621812013')
    # data = dict(username='91640100574874698D', password='a1234567.', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='宁夏新大地交通设施工程有限公司'
    #             , province='Ningxia',channel_id='123123',verify_result='123',telephone='18621812013')
    # 湖南 浙江 山东 安徽 河北
    # data = dict(username='91610112MA6TY8RT0P', password='Zj123456', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='陕西中久安防有限公司'
    #             , province='Shaanxi',channel_id='123123',verify_result='123123123123', telephone='18123289355')
    # print(data)
    # data = dict(username='钟英能', password='Aa123456',
    #             token=f'{random.randrange(1000000, 50000000)}',
    # print(data)
    # 9144190033830233XP
    # data = dict(username='91130130MA08T3PMX3', password='xyr1234567', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='河北三合电子科技有限公司'
    #             , province='Hebei',channel_id='123123',verify_result='123123123123')
    # print(data)
    # data = dict(username='91141002MA0HA5238U', password='Hx174364', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='临汾市隆博钰工矿机电设备有限公司'
    #             , province='ShanXi',channel_id='123123',verify_result='123123123123')
    # data = dict(username='92140303MA0H4RW44L', password='YQkq1234', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='临汾市隆博钰工矿机电设备有限公司'
    #             , province='ShanXi',channel_id='123123',verify_result='123123123123',pdf_active=True)
    # printHx174364
    # data= dict(username='91141002MA0HA5238U', password='Hx174364', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='临汾市隆博钰工矿机电设备有限公司'
    #             , province='ShanXi',channel_id='123123',verify_result='123123123123', telephone='18780628054')
    # data= dict(username='91110105597682285H', password='N46TLj0d', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='北京如雅商务酒店有限公司'
    #             , province='Beijing',channel_id='123123',verify_result='123123123123', telephone='13818821720',tax_code='91441900MA51DBGF23')
    # data = dict(username='131082198209110456', password='wy123456', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='河北助业网络科技有限公司'
    #             , province='Hebei',channel_id='123123',verify_result='123123123123')
    # data = dict(username='91410103397253611T', password='QS123456', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='唐山市鼎晔金属材料有限责任公司'
    #             , province='Henan',channel_id='123123',verify_result='13213201588', telephone='13213201588')
    # data = dict(username='91330110MA27WMWY32', password='182024', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='杭州先卓机械有限公司'
    #             , province='Zhejiang',channel_id='123123',verify_result='123123123123')
    # data = dict(username='91330723MA28DQKG8X', password='246318', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='武义合伟休闲用品有限公司'
    #             , province='Zhejiang',channel_id='123123',verify_result='123123123123')
    # data = dict(username='91341203MA2T4MkW85', password='qwer1234', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='阜阳博衣雅制衣有限公司'
    #             , province='Anhui',channel_id='result123123',verify_result='123123123123', telephone='13896335888')
    # data = dict(username='91341221MA2T2T453F', password='qwer1234', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='临泉县李士杰建材有限公司'
    #             , province='Anhui',channel_id='123123',verify_result='123123123123', telephone='19922125778')
    # data = dict(username='91320506MA1MQCDP02', password='XTT086022', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='苏州紫荆清远新能源汽车技术有限公司'
    #             , province='Fujian',channel_id='123123',verify_result='123123123123', telephone='13896335888')
    # data= dict(username='91371328MA3MHYUU4W', password='sd123456', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='山东川苗绿化工程有限公司'
    #             , province='Shandong',channel_id='123123',verify_result='123123123123', telephone='18980000269')
    # data = dict(username='13883113334', password='gsl13883113334', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='重庆市铭牌机械配件厂'
    #             , province='Chongqing', channel_id='123123', verify_result='123123123123', telephone='18223095595',
    #             tax_code='91500107688920445N', id=123)
    # data = dict(username='13983277881', password='yxj19810102', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='重庆万日峰工贸有限公司'
    #             , province='Chongqing', channel_id='123123', verify_result='123123123123',
    #             tax_code='91500107MA5U3RA07H', telephone='15988345338', id=123, pdf_active=False)
    # data = dict(username='915309005848462362', password='daj1024', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='临沧永亮贸易有限责任公司'
    #             , province='Yunnan',channel_id='123123',verify_result='123123123123', telephone='15988345338', id=123)
    # data = dict(username='91340111MA2P0YY10A', password='abc1234561', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='合肥创业爸爸企业服务有限公司'
    #             , province='Anhui',channel_id='123123',verify_result='123123123123', telephone='15988345338', id=123)
    # data = dict(username='91611100305639331H', password='Wdf123456', token=
    # f'{random.randrange(1000000, 50000000)}', company_name='陕西沃达沣商贸有限公司'
    #             , province='Shaanxi', channel_id='123123', verify_result='123123123123')
    # data = dict(telephone="13818821720",username='913101133015325884', password='310105198207203611', token=f'{random.randrange(1000000, 50000000)}', company_name='上海华峥建筑工程有限公司', province='Shanghai',channel_id='123123',verify_result='123123123123')
    # smsvalue="",

    # data = dict(telephone="", username='91320214735714995T', password='glsj123456',
    #             token=f'{random.randrange(1000000, 50000000)}', company_name='无锡高联三杰精密铸造有限公司', province='Jiangsu',
    #             channel_id='123123', verify_result='123123123123')

    conn.lpush('tax:tasks:linux', json.dumps(data))
    # conn.lpush(f'sy:request:{17004384}', f'动态密码_547294')
    # conn.lpush('tax:tasks:linux', json.dumps(data2))
    # conn.lpush('tax:tasks:linux', json.dumps(data3))
    # conn.lpush('tax:tasks:linux', json.dumps(data2))
    # conn.lpush('tax:tasks:linux', json.dumps(data))
