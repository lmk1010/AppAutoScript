# coding = utf-8

import os
import sys
from lxml import etree

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


# 2，获取当前设备的分辨率以及密度 根据不同的分辨率进行不同的配置模拟xy点击
def getDevicesInfo(devicesList):

    for device in devicesList:
        deviceInfo = str(os.popen("adb -s " + device + " shell getprop ro.product.model").read())
        deviceSize = str(os.popen("adb -s " + device + " shell wm size").read())
        deviceDensity = str(os.popen("adb -s " + device + " shell wm density").read())
        # 格式化
        deviceInfo = deviceInfo.strip()
        deviceSize = deviceSize[deviceSize.find(":")+1:].strip()
        deviceDensity = deviceDensity[deviceDensity.find(":") + 1:].strip()
        print("设备名称：" + str(deviceInfo) + " 设备分辨率：" + str(deviceSize) + " 设备DPI：" + str(deviceDensity))


# 3，获取所有第三方应用名称



# 4，获取当前activities 实际每5s刷新检测
def getCurrentActivities(devicesList):
    for device in devicesList:
        deviceCurrentActivity = str(os.popen("adb -s " + device + " shell dumpsys activity activities | grep mFocusedActivity").read())
        # 格式化
        deviceCurrentActivity = deviceCurrentActivity.strip()
        print("设备："+device+" 当前Activity："+deviceCurrentActivity)


# 5，调起activity 目前默认群控
def startActivity(activityName):
    for device in devicesList:
        deviceInfo = str(os.popen("adb -s " + device + " shell am start -n "+activityName).read())

# 6，截取当前屏幕 存储 分析
def getSceenSnapshot():
    for device in devicesList:
        result = str(os.popen("adb -s " + device + " exec-out screencap -p > "+device+".png").read())
        print(result)

# 7，获取当前界面的xml布局文件
def getCurrentActivityXml():
    if devicesList.__sizeof__()==0:
        return
    for device in devicesList:
        xmlFileName = device+"Layout.xml"
        createUIXml = str(os.popen("adb -s " + device + " shell uiautomator dump /sdcard/"+xmlFileName).read())
        pushUIXMLToPC = str(os.popen("adb -s " + device + " pull /sdcard/"+xmlFileName).read())
        print(pushUIXMLToPC)
        # 开始解析
        xmlTree = etree.parse(xmlFileName)

if __name__ == '__main__':
    devicesList = getDevices()
    getCurrentActivities(devicesList)
    getCurrentActivityXml()