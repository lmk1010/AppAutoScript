# coding = utf-8


import os
import sys
import ADBAction
import time
import threading
import cv2
import math


imgAppMain = cv2.imread("main.jpg", 0)
imgAd1 = cv2.imread("ad1.jpg", 0)
imgGrey = cv2.imread("screen.jpg", 0)


# 开始匹配
ret = cv2.matchTemplate(imgGrey, imgAppMain, cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
min_val = round(min_val, 3)
if min_val < 0.01:
    print("asdasd")