# coding = utf-8

import os
import sys
import ADBAction
import time
import threading
import cv2
import schedule
from PropertiesUtil import Properties
import random

# 加载app主界面图片
imgAppMain = cv2.imread("pict/main.jpg", 0)
imgAppUpdate = cv2.imread("pict/update.jpg", 0)

# 加载properties配置
configProps = Properties("../Properties/mayi.properties").getProperties()



def swipe(device):
    ADBAction.swipeXY(device, 648, 1246, 648, 904)


def checkAPPUI(device):
    # 检测是否进入应用
    currentActivity = ADBAction.getCurrentActivity(device)
    if currentActivity.find("com.cashnews.spicy/.news.activity.MainActivity") >= 0:
        print("[设备]-" + device + " 设备还在app界面........")
        return
    elif currentActivity.find("com.cashnews.spicy/.news.activity.MainActivity") >= 0:
        print("[设备]-" + device + " 设备还在app界面........")
        return
    else:
        print("[设备]-" + device + " 设备没有打开app，开始启动app.........")
        # 获取设备信息
        ADBAction.getDevicesInfo(device)
        # 打开应用
        ADBAction.clickXY(device, 164, 1375)


def rewardClick(device):
    ADBAction.clickXY(device, 171, 154)


def clickAD2(device):
    ADBAction.clickXY(device, 538, 1045)


def swipeNews(device):
    ADBAction.swipeXY(device, 648, 1246, 648, 904)


def commontNews(device):
    i = range(5)
    if i == 2:
        ADBAction.clickXY(device, 592, 1825)
        ADBAction.clickXY(device, 314, 1828)
        print("[设备]-" + device + " 评论新闻中.........")
        ADBAction.inputText(device, "VeryGood")
        ADBAction.clickXY(device, 982, 1698)
        ADBAction.actionBack(device)
        ADBAction.clickXY(device, 943, 1765)


def clickNews(device):
    # 初始化阅读时间
    readNewsTime = int(configProps.get("readNewsTime"))
    # 点击新闻
    ADBAction.clickXY(device, 648, 1246)
    # 等待2s的加载时间 防止卡顿
    time.sleep(2)
    # 设定起始阅读时间
    startTime = time.time()
    # 阅读30s新闻
    while (time.time() - startTime) < readNewsTime:
        print("[设备]-" + device + " 观看" + str(time.time() - startTime) + "新闻中.........")
        randomNum = random.randint(100, 300)
        ADBAction.swipeXY(device, 916, 1000+randomNum, 916, 904)
        ADBAction.swipeXY(device, 916, 904, 916, 1000+randomNum)
        ADBAction.clickXY(device, 471, 154)
    time.sleep(2)
    # 返回主界面
    ADBAction.actionBack(device)


def init():
    # 检测设备 返回设备列表
    devices = ADBAction.getDevices()
    if len(devices) == 0:
        print("当前无设备链接!")
        return
    else:
        return devices


def start(device):
    if (ADBAction.getScreenStatus(device) == True):
        # 强制点亮屏幕 并且解锁设备
        print("[设备]-" + device + " 设备在锁屏界面，开始解锁.........")
        ADBAction.lightDevice(device)
    # 检测是否进入应用
    currentActivity = ADBAction.getCurrentActivity(device)
    if currentActivity.find("com.cashnews.spicy/.news.activity.MainActivity") < 0:
        print("[设备]-" + device + " 设备没有打开app，开始启动app.........")
        # 获取设备信息
        ADBAction.getDevicesInfo(device)
        # 打开应用
        ADBAction.clickXY(device, 164, 1375)

    # 此延迟时间根据手机性能 自行配置
    time.sleep(3)
    ADBAction.getSceenSnapshot(device)


def cv(device):
    time.sleep(2)
    # opencv检测当前状态 之前利用uiautomator的xml 被app封锁 抓取率不高
    # 匹配当前状态 1，广告 2，主界面 3，其他干扰
    # 将模板读取灰度
    imgGrey = cv2.imread("screen.jpg", 0)
    # 匹配广告1
    ret = cv2.matchTemplate(imgGrey, imgAppUpdate, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
    min_val = round(min_val, 3)
    print(min_val)
    if min_val < 0.1:
        print("[设备]-" + device + " 出现升级页面，处理中.........")
        ADBAction.clickXY(device, 490, 1263)

    # # 匹配广告2
    # ret = cv2.matchTemplate(imgGrey, imgAd2, cv2.TM_SQDIFF_NORMED)
    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
    # min_val = round(min_val, 3)
    # if min_val < 0.01:
    #     print("[设备]-" + device + " 出现广告2，处理中.........")
    #     ADBAction.clickXY(device, 529, 1546)

def running(device):
    # run之前，无论如何强制返回主界面
    ADBAction.clickXY(device, 147, 1865)
    time.sleep(1)
    # 签到
    ADBAction.clickXY(device, 742, 514)
    ADBAction.clickXY(device, 497, 373)
    ADBAction.actionBack(device)
    # 开始刷流程
    schedule.every(20).minutes.do(rewardClick, device)
    schedule.every(3).minutes.do(checkAPPUI, device)
    while True:
        schedule.run_pending()
        startTime = time.time()
        # 阅读5s大类
        while (time.time() - startTime) < 3:
            swipeNews(device)
            print("[设备]-" + device + " 阅读主界面" + str(time.time() - startTime) + "中.........")
            count = 0
            if count == 0:
                ADBAction.clickXY(device, 125, 1579)
                ADBAction.actionBack(device)
            count = count + 1
            if count == 10:
                count = 0

        time.sleep(1)
        clickNews(device)

# 程序主方法
def mainExcute(device):
    # 改为每一个手机单独开启线程 并发执行
    print("[设备]-" + device + " 线程启动.........")
    start(device)
    cv(device)
    running(device)


def prints(str):
    print(str)
    time.sleep(1)


if __name__ == '__main__':
    devices = init()
    threads = []
    for device in devices:
        threads.append(threading.Thread(target=mainExcute, args=(device,)))

    for t in threads:
        t.start()
