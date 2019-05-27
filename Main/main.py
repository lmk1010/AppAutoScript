import os
import time
import ADBAction
import sys

roundTime = 60*60
while 1:
    # 设定起始阅读时间
    startTime = time.time()
    # 阅读30s新闻
    while (time.time() - startTime) < roundTime:
        os.system("python3 ../MaYi/mayitoutiao.py")

    time.sleep(5)

    # 设定起始阅读时间
    startTime1 = time.time()
    # 阅读30s新闻
    while (time.time() - startTime1) < roundTime:
        os.system("python3 ../QuTouTiao/qutoutiao.py")




