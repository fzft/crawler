import time
import datetime
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from utils.chen.TimeSpan import *
class DateTime(object):
    """DateTime CodeStyle Like DotNet"""
    _dateTime=datetime.datetime.now()

    def __init__(self,year=1971,month=1,day=1,hour=0,minute=0,second=0,datetimeParam=None):
        self._dateTime=datetime.datetime(year,month,day,hour,minute,second)
        if datetimeParam:
            self._dateTime=datetimeParam

        self.Day=self._dateTime.day
        self.Month=self._dateTime.month
        self.Year=self._dateTime.year
        self.Hour=self._dateTime.hour
        self.Minute=self._dateTime.minute
        self.Second=self._dateTime.second
        self.Millisecond=self._dateTime.microsecond

    def AddDays(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(days=count))
    
    def AddMonths(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(months=count))

    def AddYears(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(years=count))

    def AddHours(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(hours=count))

    def AddMinutes(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(minutes=count))

    def AddSeconds(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(seconds=count))

    def AddMilliseconds(self,count):
        return DateTime(datetimeParam=self._dateTime+relativedelta(microseconds=count*1000))

    def Date(self):
        """仅获得日期部分"""
        return DateTime(self.Year,self.Month,self.Day)

    def MonthFirstDay(self):
        return DateTime(self.Year,self.Month)

    def MonthLastDay(self):
        return DateTime(self.Year,self.Month).AddMonths(1).AddDays(-1)

    def ToString(self,formatStr="yyyy-MM-dd HH:mm:ss"):
        """以指定格式序列化DateTime对象,默认为yyyy-MM-dd HH:mm:ss yyyy=年份 MM=月 dd=日期 HH=24小时制时 hh=12小时制时 mm=分钟 ss=秒"""
        if formatStr=="r":
            GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT+0800 (CST)'
            return self._dateTime.strftime(GMT_FORMAT)
        result=formatStr
        if "yyyy" in result:
            result=result.replace("yyyy",str(self._dateTime.year))
        if "MM" in result:
            result=result.replace("MM",str(self._dateTime.month).zfill(2))
        if "dd" in result:
            result=result.replace("dd",str(self._dateTime.day).zfill(2))
        if "HH" in result:
            result=result.replace("HH",str(self._dateTime.hour).zfill(2))
        if "hh" in result:
            _hour=self._dateTime.hour
            if _hour>12:
                result=result.replace("hh",str(self._dateTime.hour-12).zfill(2))
            else:
                result=result.replace("hh",str(self._dateTime.hour).zfill(2))
        if "mm" in result:
            result=result.replace("mm",str(self._dateTime.minute).zfill(2))
        if "ss" in result:
            result=result.replace("ss",str(self._dateTime.second).zfill(2))
        return result

    def TimeStamp(self):
        """获得DateTime对象时间的时间戳"""
        return str(int(self._dateTime.timestamp()*1000))

    def TimeStampLong(self):
        """获得DateTime对象时间的时间戳"""
        return int(self._dateTime.timestamp()*1000)

    def TotalMillisecond(self):
        return int(self._dateTime.timestamp()*1000)

    def __str__(self):
        return self.ToString()
    def __repr__(self):
        return self.ToString()
    def __lt__(self,value):
        return self.TotalMillisecond()<value.TotalMillisecond()
    def __gt__(self,value):
        return self.TotalMillisecond()>value.TotalMillisecond()
    def __le__(self,value):
        return self.TotalMillisecond()<=value.TotalMillisecond()
    def __ge__(self,value):
        return self.TotalMillisecond()>=value.TotalMillisecond()
    def __eq__(self,value):
        return self.TotalMillisecond()==value.TotalMillisecond()
    def __ne__(self,value):
        return self.TotalMillisecond()!=value.TotalMillisecond()
    def __add__(self,value):
        if type(value) is TimeSpan:
            return self.AddMilliseconds(value.TotalMillisecond)
        else:
            raise Exception("不是TimeSpan类型!")
    def __sub__(self,value):
        if type(value) is TimeSpan:
            return self.AddMilliseconds(-value.TotalMillisecond)
        elif type(value) is DateTime:
            if value>self:
                r=value.TotalMillisecond()-self.TotalMillisecond()
                return TimeSpan(Millisecond=r)
            else:
                r=self.TotalMillisecond()-value.TotalMillisecond()
                return TimeSpan(Millisecond=r)
        else:
            raise Exception("不是TimeSpan类型!")

    @staticmethod
    def Now():
        """获得当前时间的DateTime对象"""
        return DateTime(datetimeParam=datetime.datetime.now())

    @staticmethod
    def Today():
        """获得当前时间的DateTime对象"""
        return DateTime(datetimeParam=datetime.datetime.now()).Date()

    @staticmethod
    def DaysInMonth(year,month):
        """获得指定月份的天数"""
        return DateTime(year,month).AddMonths(1).AddDays(-1).Day

    @staticmethod
    def DaysInYear(year):
        """获得指定年份的天数"""
        total=0
        for i in range(1,13):
            total+=DateTime.DaysInMonth(year,i)
        return total
