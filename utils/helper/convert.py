import hashlib
import re
import urllib
import datetime
import base64
import uuid



def get_md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

def get_md5_byte(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).digest()

def to_int(data):
    try:
        if data:
            return  int(data)
        else:
            return 0
    except:
        return 0

def is_float(data):
    try:
        return float(data)
    except:
        return False


def format_mobile_type(data):
    if '主' in data:
        return "主叫"
    elif '被' in data:
        return "被叫"
    else:
        return data
def format_sms_type(data):
    if '收' in data:
        return "接收"
    elif '发' in data:
        return "发送"
    else:
        return data


def to_time_seconds(data):
    rdata = data
    try:
        t = 0

        if re.search(r'^\d{2}:\d{2}:\d{2}$',rdata):
            t = str(int(data[:2])*3600+int(data[3:5])*60+int(data[6:8]))

        else:
            hour = re.search(r'^(\d*)(小时|时)(.*?)$',data)
            if hour:
                h = hour.group(1)
                data = hour.group(3)
                t = to_int(h) * 3600
            minute = re.search(r'^(\d*)(分钟|分)(.*?)$',data)
            if minute:
                m = minute.group(1)
                data = minute.group(3)
                t = t + to_int(m) * 60

            second = re.search(r'^(\d*)(秒?)$',data)
            if second:
                s = second.group(1)
                t = t + to_int(s)

        return str(t)

    except:
        return rdata

# %y 两位数的年份表示（00-99）
# %Y 四位数的年份表示（000-9999）
# %m 月份（01-12）
# %d 月内中的一天（0-31）
# %H 24小时制小时数（0-23）
# %I 12小时制小时数（01-12） 
# %M 分钟数（00=59）
# %S 秒（00-59）
def to_datetime(data,format=r'%Y-%m-%d %H:%M:%S'):
    try:
        time=''
        if re.search(r"^\d{4}年\d{1,2}月$",data):
            regex = re.search(r"^(.*?)年(.*?)月$",data)
            if regex:
                data = regex.group(1) + regex.group(2).zfill(2)
        elif re.search(r"^\d{4}年\d{1,2}月\d{1,2}日$",data):
            regex = re.search(r"^(.*?)年(.*?)月(.*?)日$",data)
            if regex:
                data = regex.group(1) + regex.group(2).zfill(2) + regex.group(3).zfill(2)
        if re.search(r"^\d{14}$",data):
            time = datetime.datetime.strptime(data,r'%Y%m%d%H%M%S')
        elif re.search(r"^\d{8}$",data):
            time = datetime.datetime.strptime(data,r'%Y%m%d')
        elif re.search(r"^\d{6}$",data):
            time = datetime.datetime.strptime(data,r'%Y%m')
        elif re.search(r"^\d{8} \d{2}:\d{2}:\d{2}$",data):
            time = datetime.datetime.strptime(data,r'%Y%m%d %H:%M:%S')
        elif re.search(r"^\d{4}-\d{2}$",data):
            time = datetime.datetime.strptime(data,r'%Y-%m')
        elif re.search(r"^\d{4}-\d{2}-\d{2}$",data):
            time = datetime.datetime.strptime(data,r'%Y-%m-%d')
        elif re.search(r"^\d{4}/\d{2}$",data):
            time = datetime.datetime.strptime(data,r'%Y/%m')
        elif re.search(r"^\d{4}/\d{2}/\d{2}$",data):
            time = datetime.datetime.strptime(data,r'%Y/%m/%d')
        elif re.search(r"^\d{4}/\d{2}/\d{2} \d{2}:\d{2}$",data):
            time = data + ":00"
        elif re.search(r"^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$",data):
            time = datetime.datetime.strptime(data,r'%Y/%m/%d %H:%M:%S')
        elif re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d*$",data):
            return data[:19]
        elif re.search(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$",data):
            return data.replace('T'," ")


        
        if time:
            datestr = datetime.datetime.strftime(time,format)
            return datestr
        else:
            return data
    except:
        return data

def url_encode(data):
    return urllib.parse.quote(data)

def url_decode(data):
    return urllib.parse.unquote(data)

def base64encode(data):
    return base64.b64encode(bytes(data,encoding='utf-8'))

def base64encodestr(data):
    return str(base64.b64encode(bytes(data,encoding='utf-8')),encoding='utf-8')

def base64decode(data):
    return base64.b64decode(bytes(data,encoding='utf-8'))

def base64tobyte(data):
    try:
        return base64.b64decode(data)
    except Exception as e:
        print(e)


def base64tostr(data,encode='utf-8'):
    return str(base64.b64decode(data),encode)


def readfile(filename):
    f = open(filename, 'r', encoding='utf-8') # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr+line
        line = f.readline()
    f.close()
    return htmlstr

def doubletoint(data):
    idata = int(data)
    if data>idata:
        idata +=1
    return idata
def unicodetostr(data):
    try:
        return data.encode('latin-1').decode('unicode_escape')
    except:
        return ''
def get_uuid():   
    return "".join(str(uuid.uuid4()).split("-")).upper()

def code_to_city(code):
    try:
        if not code:
            return ''
        if type(code) is not str:
            return ''
        codelist={
            "010":"北京市",
            "021":"上海市",
            "022":"天津市",
            "023":"重庆市",
            "852":"香港",
            "853":"澳门",
            "0310":"邯郸市",
            "0311":"石家庄",
            "0312":"保定市",
            "0313":"张家口",
            "0314":"承德市",
            "0315":"唐山市",
            "0316":"廊坊市",
            "0317":"沧州市",
            "0318":"衡水市",
            "0319":"邢台市",
            "0335":"秦皇岛",
            "0570":"衢州市",
            "0571":"杭州市",
            "0572":"湖州市",
            "0573":"嘉兴市",
            "0574":"宁波市",
            "0575":"绍兴市",
            "0576":"台州市",
            "0577":"温州市",
            "0578":"丽水市",
            "0579":"金华市",
            "0580":"舟山市",
            "024":"沈阳市",
            "0410":"铁岭市",
            "0411":"大连市",
            "0412":"鞍山市",
            "0413":"抚顺市",
            "0414":"本溪市",
            "0415":"丹东市",
            "0416":"锦州市",
            "0417":"营口市",
            "0418":"阜新市",
            "0419":"辽阳市",
            "0421":"朝阳市",
            "0427":"盘锦市",
            "0429":"葫芦岛",
            "027":"武汉市",
            "0710":"襄城市",
            "0711":"鄂州市",
            "0712":"孝感市",
            "0713":"黄州市",
            "0714":"黄石市",
            "0715":"咸宁市",
            "0716":"荆沙市",
            "0717":"宜昌市",
            "0718":"恩施市",
            "0719":"十堰市",
            "0722":"随枣市",
            "0724":"荆门市",
            "0728":"江汉市",
            "025":"南京市",
            "0510":"无锡市",
            "0511":"镇江市",
            "0512":"苏州市",
            "0513":"南通市",
            "0514":"扬州市",
            "0515":"盐城市",
            "0516":"徐州市",
            "0517":"淮阴市",
            "0518":"连云港",
            "0519":"常州市",
            "0523":"泰州市",
            "0470":"海拉尔",
            "0471":"呼和浩特",
            "0472":"包头市",
            "0473":"乌海市",
            "0474":"集宁市",
            "0475":"通辽市",
            "0476":"赤峰市",
            "0477":"东胜市",
            "0478":"临河市",
            "0479":"锡林浩特",
            "0482":"乌兰浩特",
            "0790":"新余市",
            "0791":"南昌市",
            "0792":"九江市",
            "0793":"上饶市",
            "0794":"临川市",
            "0795":"宜春市",
            "0796":"吉安市",
            "0797":"赣州市",
            "0798":"景德镇",
            "0799":"萍乡市",
            "0701":"鹰潭市",
            "0350":"忻州市",
            "0351":"太原市",
            "0352":"大同市",
            "0353":"阳泉市",
            "0354":"榆次市",
            "0355":"长治市",
            "0356":"晋城市",
            "0357":"临汾市",
            "0358":"离石市",
            "0359":"运城市",
            "0930":"临夏市",
            "0931":"兰州市",
            "0932":"定西市",
            "0933":"平凉市",
            "0934":"西峰市",
            "0935":"武威市",
            "0936":"张掖市",
            "0937":"酒泉市",
            "0938":"天水市",
            "0941":"甘南州",
            "0943":"白银市",
            "0530":"菏泽市",
            "0531":"济南市",
            "0532":"青岛市",
            "0533":"淄博市",
            "0534":"德州市",
            "0535":"烟台市",
            "0536":"淮坊市",
            "0537":"济宁市",
            "0538":"泰安市",
            "0539":"临沂市",
            "0450":"阿城市",
            "0451":"哈尔滨",
            "0452":"齐齐哈尔",
            "0453":"牡丹江",
            "0454":"佳木斯",
            "0455":"绥化市",
            "0456":"黑河市",
            "0457":"加格达奇",
            "0458":"伊春市",
            "0459":"大庆市",
            "0591":"福州市",
            "0592":"厦门市",
            "0593":"宁德市",
            "0594":"莆田市",
            "0595":"泉州市",
            "0596":"漳州市",
            "0597":"龙岩市",
            "0598":"三明市",
            "0599":"南平市",
            "020":"广州市",
            "0751":"韶关市",
            "0752":"惠州市",
            "0753":"梅州市",
            "0754":"汕头市",
            "0755":"深圳市",
            "0756":"珠海市",
            "0757":"佛山市",
            "0758":"肇庆市",
            "0759":"湛江市",
            "0760":"中山市",
            "0762":"河源市",
            "0763":"清远市",
            "0765":"顺德市",
            "0766":"云浮市",
            "0768":"潮州市",
            "0769":"东莞市",
            "0660":"汕尾市",
            "0661":"潮阳市",
            "0662":"阳江市",
            "0663":"揭西市",
            "028":"成都市",
            "0810":"涪陵市",
            "0811":"重庆市",
            "0812":"攀枝花",
            "0813":"自贡市",
            "0814":"永川市",
            "0816":"绵阳市",
            "0817":"南充市",
            "0818":"达县市",
            "0819":"万县市",
            "0825":"遂宁市",
            "0826":"广安市",
            "0827":"巴中市",
            "0830":"泸州市",
            "0831":"宜宾市",
            "0832":"内江市",
            "0833":"乐山市",
            "0834":"西昌市",
            "0835":"雅安市",
            "0836":"康定市",
            "0837":"马尔康",
            "0838":"德阳市",
            "0839":"广元市",
            "0840":"泸州市",
            "0730":"岳阳市",
            "0731":"长沙市",
            "0732":"湘潭市",
            "0733":"株州市",
            "0734":"衡阳市",
            "0735":"郴州市",
            "0736":"常德市",
            "0737":"益阳市",
            "0738":"娄底市",
            "0739":"邵阳市",
            "0743":"吉首市",
            "0744":"张家界",
            "0745":"怀化市",
            "0746":"永州冷",
            "0370":"商丘市",
            "0371":"郑州市",
            "0372":"安阳市",
            "0373":"新乡市",
            "0374":"许昌市",
            "0375":"平顶山",
            "0376":"信阳市",
            "0377":"南阳市",
            "0378":"开封市",
            "0379":"洛阳市",
            "0391":"焦作市",
            "0392":"鹤壁市",
            "0393":"濮阳市",
            "0394":"周口市",
            "0395":"漯河市",
            "0396":"驻马店",
            "0398":"三门峡",
            "0870":"昭通市",
            "0871":"昆明市",
            "0872":"大理市",
            "0873":"个旧市",
            "0874":"曲靖市",
            "0875":"保山市",
            "0876":"文山市",
            "0877":"玉溪市",
            "0878":"楚雄市",
            "0879":"思茅市",
            "0691":"景洪市",
            "0692":"潞西市",
            "0881":"东川市",
            "0883":"临沧市",
            "0886":"六库市",
            "0887":"中甸市",
            "0888":"丽江市",
            "0550":"滁州市",
            "0551":"合肥市",
            "0552":"蚌埠市",
            "0553":"芜湖市",
            "0554":"淮南市",
            "0555":"马鞍山",
            "0556":"安庆市",
            "0557":"宿州市",
            "0558":"阜阳市",
            "0559":"黄山市",
            "0561":"淮北市",
            "0562":"铜陵市",
            "0563":"宣城市",
            "0564":"六安市",
            "0565":"巢湖市",
            "0566":"贵池市",
            "0951":"银川市",
            "0952":"石嘴山",
            "0953":"吴忠市",
            "0954":"固原市",
            "0431":"长春市",
            "0432":"吉林市",
            "0433":"延吉市",
            "0434":"四平市",
            "0435":"通化市",
            "0436":"白城市",
            "0437":"辽源市",
            "0438":"松原市",
            "0439":"浑江市",
            "0440":"珲春市",
            "0770":"防城港",
            "0771":"南宁市",
            "0772":"柳州市",
            "0773":"桂林市",
            "0774":"梧州市",
            "0775":"玉林市",
            "0776":"百色市",
            "0777":"钦州市",
            "0778":"河池市",
            "0779":"北海市",
            "0851":"贵阳市",
            "0852":"遵义市",
            "0853":"安顺市",
            "0854":"都均市",
            "0855":"凯里市",
            "0856":"铜仁市",
            "0857":"毕节市",
            "0858":"六盘水",
            "0859":"兴义市",
            "029":"西安市",
            "0910":"咸阳市",
            "0911":"延安市",
            "0912":"榆林市",
            "0913":"渭南市",
            "0914":"商洛市",
            "0915":"安康市",
            "0916":"汉中市",
            "0917":"宝鸡市",
            "0919":"铜川市",
            "0971":"西宁市",
            "0972":"海东市",
            "0973":"同仁市",
            "0974":"共和市",
            "0975":"玛沁市",
            "0976":"玉树市",
            "0977":"德令哈",
            "0890":"儋州市",
            "0898":"海口市",
            "0899":"三亚市",
            "0891":"拉萨市",
            "0892":"日喀则",
            "0893":"山南市",

        }
        if code in codelist.keys():
            return codelist[code]
        else:
            return code
    except:
        return code

# print(to_datetime('2019/05/02 14:06:22'))