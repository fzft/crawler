import  execjs
import os

def GetRunPath():
    """获得脚本执行目录"""
    return os.getcwd()

def get_js(filename):
    filename=os.path.join(GetRunPath(),"core","encrypt_file",filename)
    # js_dir = os.path.join(get_root_path(__name__), 'encrypt_file', filename)
    f = open(filename, 'r', encoding='utf-8') # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr+line
        line = f.readline()

    if htmlstr[0:1]== "\ufeff":
        htmlstr = htmlstr[1:]
    f.close()
    return htmlstr

class js_encrypt():

    def __init__(self, filename):
        filename=os.path.join(GetRunPath(),"core","encrypt_file",filename)
        self.ctx = execjs.compile(get_js(filename))


    def enc(self,inputs,*args):
        try:
            distance = self.ctx.call(inputs, *args)
            return  distance
        except Exception as e:
            print(e)
            return ''

def enc(filename,inputs,*args):
    try:
        ctx = execjs.compile(get_js(filename))
        
        distance = ctx.call(inputs, *args)
        return  distance
    except Exception as e:
        print(e)
        return ''