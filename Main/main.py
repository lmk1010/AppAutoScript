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
import inspect
import ctypes

# ---加载properties配置
configProps = Properties("../Properties/common.properties").getProperties()


# ---复用函数集合
# -------------------Function:保持app前台ui----------------------------------
def maintain_app_ui(device, activityName):
    if (ADBAction.getScreenStatus(device) == True):
        # ---强制点亮屏幕 并且解锁设备
        print("[设备]-" + device + " 设备在锁屏界面，开始解锁.........")
        ADBAction.lightDevice(device)
        # ---检测是否进入应用
    if ADBAction.getCurrentActivity(device).find(activityName) < 0:
        print("[设备]-" + device + " 设备没有打开app，开始启动app.........")
        # ---获取设备信息
        ADBAction.getDevicesInfo(device)
        # ---打开应用
        ADBAction.startActivitySingleDevice(activityName, device)
# --------------------------------------------------------------------------

# -------------------Function:检测手机是否还在APP界面---------------------------
# ------------------(activityName:根据不同APP多个ACT检测)-----------------------
def checkAPPUI(device, appActName):
    # ---检测是否进入应用
    currentActivity = ADBAction.getCurrentActivity(device)
    # ---从配置文件读取 根据不同的app
    activityNames = configProps.get(appActName).split(",")
    # ---设置计数器
    count = 0
    for activityName in activityNames:
        if currentActivity.find(activityName) >= 0:
            print("[设备]-" + device + " 设备处于app界面"+count+"........")
            return
    # ---所属app的act列表中都未找到 表示此时设备已经退出app
    print("[设备]-" + device + " 设备不在app状态，开始重新启动app.........")
    # ---打开应用
    ADBAction.startActivitySingleDevice("com.jifen.qukan/com.jifen.qkbase.main.MainActivity", device)
    # ---执行打开后检测是否真的开启应用了
    resActivity = ADBAction.getCurrentActivity(device)
    while resActivity.find("com.jifen.qukan/com.jifen.qkbase.main.MainActivity", device) < 0:
        time.sleep(1)
        ADBAction.startActivitySingleDevice("com.jifen.qukan/com.jifen.qkbase.main.MainActivity", device)
    print("[设备]-" + device + " 设备已成功开启app.........")
# ---------------------------------------------------------------------------
# -------------------Function:定时奖励----------------------------------------
def rewardClick(device):
    # ---点击reward图标
    ADBAction.clickXY(device, 964, 157)
    # ---返回键
    ADBAction.clickSystemKey(4, device)
# ---------------------------------------------------------------------------



# ---加载第一个app逻辑 控制滑动时间 最大范围内控制 1小时
# ---趣头条
def app_qutoutiao(device):
    # -----------------------------开始---------------------------------
    # ---打开app界面
    maintain_app_ui(device, "com.jifen.qukan/com.jifen.qkbase.main.MainActivity")
    # ---此延迟时间根据手机性能 自行配置等待app加载时间 后期可以考虑使用opencv做验证
    time.sleep(10)
    # --------------------------CV检测广告-------------------------------
    # ---截取初始界面 用于检测广告
    ADBAction.getSceenSnapshot(device)
    # ---等待截图传回时间冗余
    time.sleep(3)
    # ---加载广告图片模板
    imgAppMain = cv2.imread("qutoutiao/img/main.jpg", 0)
    imgAd1 = cv2.imread("qutoutiao/img/ad1.jpg", 0)
    imgAd2 = cv2.imread("qutoutiao/img/ad2.jpg", 0)
    # ---opencv检测当前状态 之前利用uiautomator的xml 被app封锁 抓取率不高
    # ---匹配当前状态 1，广告 2，主界面 3，其他干扰
    # ---将模板读取灰度
    imgGrey = cv2.imread("screen.jpg", 0)
    # 匹配广告1
    ret = cv2.matchTemplate(imgGrey, imgAd1, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
    min_val = round(min_val, 3)
    # ---数值小于0.01基本判定为此广告
    if min_val < 0.01:
        print("[设备]-" + device + " 出现广告1，处理中.........")
        ADBAction.clickXY(device, 529, 1546)

    # 匹配广告2
    ret = cv2.matchTemplate(imgGrey, imgAd2, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
    min_val = round(min_val, 3)
    # ---数值小于0.01基本判定为此广告
    if min_val < 0.01:
        print("[设备]-" + device + " 出现广告2，处理中.........")
        ADBAction.clickXY(device, 529, 1546)

    # --------------------开始刷新闻-------------------------------
    # ---App打开时间戳
    app_time = time.time()
    # ---run之前，无论如何强制返回app主界面 保证正确率
    ADBAction.clickXY(device, 146, 1849)
    time.sleep(1)
    # ---签到
    ADBAction.clickXY(device, 722, 1835)
    ADBAction.clickXY(device, 920, 303)
    ADBAction.actionBack(device)
    ADBAction.clickXY(device, 146, 1849)
    # ---定时器任务集合
    # ---此为app定时奖励
    schedule.every(2).minutes.do(rewardClick, device)
    # ---定时检测当前是否还在app界面
    schedule.every(3).minutes.do(checkAPPUI, "qttActs")
    # ---定时忘记了。。。。。
    # schedule.every(30).minutes.do(refresh, device)

    while True:
        # ---开始定时器任务
        schedule.run_pending()
        # ---记录阅读新闻时间戳 每次循环刷新
        startTime = time.time()
        # ---阅读主界面3s，确保尽可能多的点击详细新闻 不错过任何一个新的新闻
        while (time.time() - startTime) < 3:
            # ---滑动主界面新闻
            ADBAction.swipeXY(device, 648, 1246, 648, 904)
            print("[设备]-" + device + " 阅读主界面" + str(time.time() - startTime) + "中.........")
        time.sleep(1)
        # ---初始化阅读时间60s
        readNewsTime = 60
        # ---点击新闻
        ADBAction.clickXY(device, 648, 1246)
        # ---等待2s的加载时间 防止卡顿
        time.sleep(2)
        # ---设定起始阅读时间
        startRTime = time.time()
        # ---阅读30s新闻
        while (time.time() - startRTime) < readNewsTime:
            print("[设备]-" + device + " 观看" + str(time.time() - startTime) + "新闻中.........")
            # ---滑动随机的距离 防止行为检测 增加滑动的随机性
            randomNum = random.randint(100, 300)
            # ---向下滑动新闻详情页
            ADBAction.swipeXY(device, 648, 1100 + randomNum, 648, 904)
            # ---向上滑动新闻详情页
            ADBAction.swipeXY(device, 648, 904, 648, 1246 + randomNum)
        # ---随机评论新闻 防止行为检测
        # commontNews(device)
        # ---歇2s
        time.sleep(2)
        # ---返回主界面 完成一个1分钟的流程
        ADBAction.actionBack(device)
        # ---检测如果此app刷新闻超过1小时 则退出死循环
        if (time.time() - app_time) > 60*60:
            break

# ---执行startACT 执行后台任务清理 跳转下一个app 进行签到等操作开始
def startACT(activitName, device):
    ADBAction.startActivitySingleDevice(activitName, device)

# ---加载第二个app逻辑
def app_mayi(device):
    # -----------------------------开始---------------------------------
    # ---打开app界面
    maintain_app_ui(device, "com.jifen.qukan/com.jifen.qkbase.main.MainActivity")
    # ---此延迟时间根据手机性能 自行配置等待app加载时间 后期可以考虑使用opencv做验证
    time.sleep(5)
    # --------------------------CV检测广告-------------------------------
    # ---加载广告图片模板
    imgAppMain = cv2.imread("mayitoutiao/img/main.jpg", 0)
    imgAppUpdate = cv2.imread("mayitoutiao/img/update.jpg", 0)
    # ---匹配当前状态 1，广告 2，主界面 3，其他干扰
    # ---将模板读取灰度
    imgGrey = cv2.imread("screen.jpg", 0)
    # ---匹配广告1
    ret = cv2.matchTemplate(imgGrey, imgAppUpdate, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ret)
    min_val = round(min_val, 3)
    print(min_val)
    if min_val < 0.1:
        print("[设备]-" + device + " 出现升级页面，处理中.........")
        ADBAction.clickXY(device, 490, 1263)

    # --------------------------开始刷新闻-------------------------------
    # ---run之前，无论如何强制返回主界面
    ADBAction.clickXY(device, 147, 1865)
    time.sleep(1)
    # ---签到
    ADBAction.clickXY(device, 742, 514)
    ADBAction.clickXY(device, 497, 373)
    ADBAction.actionBack(device)
    # ---开始刷流程
    # schedule.every(20).minutes.do(rewardClick, device)
    schedule.every(3).minutes.do(checkAPPUI, device, "mayiActs")
    while True:
        # ---开启定时任务
        schedule.run_pending()
        startTime = time.time()
        # ---阅读主界面3s
        while (time.time() - startTime) < 3:
            # ---在主界面滑动操作
            ADBAction.swipeXY(device, 648, 1246, 648, 904)
            print("[设备]-" + device + " 阅读主界面" + str(time.time() - startTime) + "中.........")
            count = 0
            if count == 0:
                ADBAction.clickXY(device, 125, 1579)
                ADBAction.actionBack(device)
            count = count + 1
            if count == 10:
                count = 0

        time.sleep(1)
        # ---初始化阅读时间 都是60s
        readNewsTime = 60
        # ---点击新闻详情
        ADBAction.clickXY(device, 648, 1246)
        # 等待2s的加载时间 防止卡顿
        time.sleep(2)
        # 设定起始阅读时间
        startRTime = time.time()
        # 阅读30s新闻
        while (time.time() - startRTime) < readNewsTime:
            print("[设备]-" + device + " 观看" + str(time.time() - startTime) + "新闻中.........")
            # ---模拟随机滑动
            randomNum = random.randint(100, 300)
            # ---向上滑动
            ADBAction.swipeXY(device, 916, 1000 + randomNum, 916, 904)
            # ---向下滑动
            ADBAction.swipeXY(device, 916, 904, 916, 1000 + randomNum)
            # ---针对60s的奖励，需要额外点击屏幕其他位置 来返回到新闻界面
            ADBAction.clickXY(device, 471, 154)
        time.sleep(2)
        # ---返回主界面
        ADBAction.actionBack(device)


# 执行startACT 执行后台任务清理 跳转下一个app 进行签到等操作开始

# 加载第三个app逻辑

# 执行startACT 执行后台任务清理 跳转下一个app 进行签到等操作开始

# 加载第四个app逻辑

# 执行startACT 执行后台任务清理 跳转下一个app 进行签到等操作开始

# 加载第五个app逻辑


# ---app脚本方法集合
def app_script_all(device):
    app_qutoutiao(device)
    app_mayi(device)


# ---开启设备查找
def device_start():
    print("待完成")


# ---核对设备完成
def device_recheck():
    # 检测设备 返回设备列表
    devices = ADBAction.getDevices()
    if len(devices) == 0:
        print("当前无设备链接!")
        return
    else:
        return devices


# ---开启多线程 执行main方法
def device_main():
    # ---核对设备完成
    devices = device_recheck()
    # ---初始化线程
    threads = []
    for device in devices:
        threads.append(threading.Thread(target=app_script_all, args=(device,)))

    for t in threads:
        t.start()
        print("开启线程---")


if __name__ == '__main__':
    device_main()
