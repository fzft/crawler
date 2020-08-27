import  datetime
import time
import calendar
from dateutil.relativedelta import relativedelta


print(range(0,-6,-1))
for i in range(0,-6,-1):
    print(i)

print(relativedelta(years=3))
print(datetime.datetime.now()+relativedelta(years=3))

print(datetime.date.today().year)
print(datetime.date.today().month)
print(datetime.date.today().day)
print(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
print(time.strftime("%Y%m%d%H%M%S.%f"))

print(datetime.datetime.now())

print(datetime.timedelta(days=10))
print(datetime.timedelta(days=10))


print(int(time.time()))
print(int(round(time.time()*1000)))

print(calendar.monthrange(2018,10)[1])

