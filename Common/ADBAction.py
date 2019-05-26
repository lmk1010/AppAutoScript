# coding = utf-8

import os
import sys
from lxml import etree
import cv2
import numpy
import time
import datetime
import random
import threading

# 作为脚本 1，获取当前设备
def getDevices():
    devices = os.popen("adb devices").read()
    devicesList = []
    for device in devices.split("\n")[1:]:
        index = device.find("device")
        if index >= 0:
            device = device[:index]
            print("当前连接设备:" + str(device))
            devicesList.append(device.strip())
    print("当前设备已连接设备数量：" + str(len(devicesList)))
    return devicesList


def getDeviceSize(device):
    deviceSize = str(os.popen("adb -s " + device + " shell wm size").read())
    return deviceSize.strip()


def lightDevice(device):
    # 查看屏幕是否熄灭
    os.system("adb -s " + device + " shell input keyevent 224")
    os.system("adb -s " + device + " shell input swipe 300 1700 300 200 500")


# 2，获取当前设备的分辨率以及密度 根据不同的分辨率进行不同的配置模拟xy点击
def getDevicesInfo(device):
    deviceDict = {}
    deviceInfo = str(os.popen("adb -s " + device + " shell getprop ro.product.model").read())
    deviceSize = str(os.popen("adb -s " + device + " shell wm size").read())
    deviceDensity = str(os.popen("adb -s " + device + " shell wm density").read())
    # 格式化
    deviceInfo = deviceInfo.strip()
    deviceSize = deviceSize[deviceSize.find(":") + 1:].strip()
    deviceDensity = deviceDensity[deviceDensity.find(":") + 1:].strip()
    print("设备名称：" + str(deviceInfo) + " 设备分辨率：" + str(deviceSize) + " 设备DPI：" + str(deviceDensity))

# 3，获取所有第三方应用名称


# 4，获取当前activity 实际每5s刷新检测
def getCurrentActivity(device):
    deviceCurrentActivity = str(
        os.popen("adb -s " + device + " shell dumpsys activity activities | findstr mFocusedActivity").read())
    # 格式化
    deviceCurrentActivity = deviceCurrentActivity.strip()
    print("设备-" + device + " 当前Activity：" + deviceCurrentActivity)
    return deviceCurrentActivity


# 5，调起activity 目前默认群控
def startActivity(activityName, devicesList):
    for device in devicesList:
        deviceStart = str(os.popen("adb -s " + device + " shell am start -n " + activityName).read())
        if deviceStart.find("Starting") >= 0:
            print("[设备]-"+device + " 正在开启app........")
        else:
            print("[设备]-"+device + " 开启app失败........")

def getScreenStatus(device):
    res = str(os.popen("adb -s " + device + " shell dumpsys window policy | findstr mShowingLockscreen").read()).strip()
    if res.find("mShowingLockscreen=true") >= 0:
        return True
    elif res.find("mShowingLockscreen=false") >= 0:
        return False

def startActivitySingleDevice(activityName, device):
    os.system("adb -s " + device + " shell am start -n " + activityName)


# 6，截取当前屏幕 存储 分析
def getSceenSnapshot(device):
    # win10 adb版本不支持 mac可以支持
    # result = str(os.popen("adb -s " + device + " exec-out screencap -p > "+sceenName).read())
    # 创建快照
    os.system("adb -s " + device + " shell screencap -p /sdcard/screen.jpg")
    os.system("adb -s " + device + " pull /sdcard/screen.jpg")


# 7，获取当前界面的xml布局文件 此方法行不通了 改用opencv
def getCurrentActivityXml(device):
    xmlFileName = str(random.randint(0, 1000)) + "Layout.xml"
    print(xmlFileName)
    createUIXml = str(os.popen("adb -s " + device + " shell uiautomator dump /sdcard/" + xmlFileName).read())
    pushUIXMLToPC = str(os.popen("adb -s " + device + " pull /sdcard/" + xmlFileName).read())
    # 开始解析
    if os.path.exists(xmlFileName) == False:
       getCurrentActivityXml(device)
    xmlTree = etree.parse(xmlFileName)
    return xmlTree


# 8，点击指定位置xy的
def clickXY(device, x, y):
    os.system("adb -s " + device + " shell input tap " + str(x) + " " + str(y))


# 9，点击指定按键 返回键4 home键3 点亮屏幕224
def clickSystemKey(key, device):
    os.system("adb -s " + device + " shell input keyevent " + str(key))


# 10，滑动
def swipeXY(device, x, y, x1, y1):
    os.system("adb -s " + device + " shell input swipe " + str(x) + " " + str(y) + " " + str(x1) + " " + str(y1))

def actionBack(device):
    clickSystemKey(4, device)

def inputText(device, text):
    os.system("adb -s " + device + " shell input text " + str(text))

if __name__ == '__main__':
    devices = getDevices()
    for device in devices:
        getCurrentActivityXml(device)