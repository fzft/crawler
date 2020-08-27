class TimeSpan(object):
    """表示一个时间范围"""
    _totalMillisecond=0
    def __init__(self,hour=0,minute=0,second=0,Millisecond=0,day=0):
        self._totalMillisecond+=hour*60*60*1000
        self._totalMillisecond+=minute*60*1000
        self._totalMillisecond+=second*1000
        self._totalMillisecond+=Millisecond
        self._totalMillisecond+=day*24*60*60*1000
        self.TotalSecond=int(self._totalMillisecond/1000)
        self.TotalMinute=int(self.TotalSecond/60)
        self.TotalHour=int(self.TotalMinute/60)
        self.TotalDay=int(self.TotalHour/24)
        self.TotalMillisecond=self._totalMillisecond
        pass

    def AddDays(self,count):
        return TimeSpan(Millisecond=self._totalMillisecond+count*24*60*60*1000)

    def AddHours(self,count):
        return TimeSpan(self._totalMillisecond+count*60*60*1000)

    def AddMinutes(self,count):
        return TimeSpan(self._totalMillisecond+count*60*1000)
    
    def AddSeconds(self,count):
        return TimeSpan(self._totalMillisecond+count*1000)

    def AddMilliseconds(self,count):
        return TimeSpan(self._totalMillisecond+count)

    def __add__(self, obj):
        if type(obj) is TimeSpan:
            r=self._totalMillisecond + obj.TotalMillisecond
            return TimeSpan(Millisecond=r)
        else:
            raise Exception("不是TimeSpan类型!")
    
    def __sub__(self,obj):
        if type(obj) is TimeSpan:
            if obj.TotalMillisecond>self._totalMillisecond:
                raise Exception("结果是负的!")
            else:
                r=self._totalMillisecond - obj.TotalMillisecond
                return TimeSpan(Millisecond=r)
        else:
            raise Exception("不是TimeSpan类型!")

    def __lt__(self,value):
        return self.TotalMillisecond<value.TotalMillisecond
    def __gt__(self,value):
        return self.TotalMillisecond>value.TotalMillisecond
    def __le__(self,value):
        return self.TotalMillisecond<=value.TotalMillisecond
    def __ge__(self,value):
        return self.TotalMillisecond>=value.TotalMillisecond
    def __eq__(self,value):
        return self.TotalMillisecond==value.TotalMillisecond
    def __ne__(self,value):
        return self.TotalMillisecond!=value.TotalMillisecond
