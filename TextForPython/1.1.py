import random
import os
import time

times=0
b=0
while True:
    a = random.randint(1, 20)
    times += a
    os.system('adb shell input swipe 500 1500 500 500 300')
    print('滑动第{}次,{}s,共{}s'.format(b, a,times))
    time.sleep(a)
    b+=1



