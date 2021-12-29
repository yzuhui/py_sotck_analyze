import time
from auxiliary_lib.ConfigLoader import ConfigLoader
import datetime

sevenDaySecs = 604800
now = time.time()

print(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)))
print(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now - sevenDaySecs)))

d1 = datetime.datetime(2020,9,1)   # 第一个日期
d2 = datetime.datetime.now()   # 第二个日期
print(d2)
interval = d2 - d1
print(interval.days)

list = [1, 2, 3, 4, 5]
for i in range(0, len(list)):
    ma = list[i:len(list)]
    print(ma, "|", min(ma))

print(list[::-1])

l1 = [1, 2, 3]
l2 = []
l2 += l1
print(l2)

l3 = [0x000]
code = 0x000
if code in l3:
    print('==')