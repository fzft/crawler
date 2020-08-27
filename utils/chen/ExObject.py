import json
import re
class ExObject():
    def __init__(self, default=None):
        if (type(default) is list 
        or type(default) is dict 
        or type(default) is tuple 
        or type(default) is str  
        or type(default) is set):
            self.defaultIter=iter(default)
        self.default = default
    def __getitem__(self, key):
        if not self.default:
            return ExObject()
        if len(key)>5 and key[0:5]=="null_":
            key="?"+key[5:]
        if type(self.default) is list or type(self.default) is tuple:
            if key[:1]=="?":
                try:
                    key=key[1:]
                    if(int(key)<=len(self.default)-1):
                        return ExObject(self.default[int(key)])
                    else:
                        return ExObject()
                except KeyError:
                    return ExObject()
            else:
                return ExObject(self.default[int(key)])
        if type(key) is slice:
            #如果是分片索引
            return self.default[key]
        if key[:1]=="?":
            try:
                key=key[1:]
                if hasattr(self.default,key):
                    return ExObject(self.default.__getitem__(key))
                elif key in self.default.keys():
                    return ExObject(self.default[key])
                else:
                    return ExObject()
            except:
                return ExObject()
        else:
            return ExObject(self.default.__getitem__(key))

    def __getattr__(self, name):
        return self.__getitem__(name)
    def __str__(self):
        return str(self.default)
    def __repr__(self):
        return str(self.default)
    def __add__(self,value):
        if self.ToString():
            return self.ToString()+value
        else:
            return value
    def __bool__(self):
        if self.default:
            return True
        else:
            return False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return ExObject(self.defaultIter.__next__())
        except:
            raise StopIteration()

    def __len__(self):
        return len(self.default)

    def ToString(self,defaultValue=""):
        if self.default:
            return str(self.default)
        return defaultValue

    def ToOriginal(self):
        return self.default

    def Where(self,func):
        if type(self.default) is list or type(self.default) is tuple or type(self.default) is dict or type(self.default) is set:
            r=[]
            for item in self:
                if func(item):
                    r.append(item)
            return ExObject(r)
        return ExObject()
    
    def Select(self,func):
        if type(self.default) is list or type(self.default) is tuple or type(self.default) is dict or type(self.default) is set:
            r=[]
            for item in self.defaultIter:
                r.append(func(item))
            return ExObject(r)
        return ExObject()

    @staticmethod
    def loadJson(jsonStr):
        try:
            jitem=json.loads(jsonStr)
            return ExObject(jitem)
        except:
            return ExObject()
            
    @staticmethod
    def regex(pattern,string,flags=0):
        """正则匹配并转换为ExObject类型"""
        try:
            return ExObject(re.findall(pattern,string,flags))
        except Exception as e:
            return ExObject()

    @staticmethod
    def regexOne(pattern,string):
        """获得默认第一个匹配字符串,没有匹配则返回空字符串"""
        return ExObject.regex(pattern,string)["?0"].ToString()