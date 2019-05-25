# coding = utf-8

# 测试ADB实验
import os
import sys


# 作为脚本 1，获取当前设备
def getDevices():
    devices = os.popen("adb devices").read()
    devicesList = []
    for device in devices.split("\n")[1:]:
        index = device.find("device")
        if index>=0:
            device = device[:index]
            print("当前连接设备:"+str(device))
            devicesList.append(device)
    print("当前设备已连接设备数量："+str(len(devicesList)))
    return devicesList


# 2，获取当前设备的分辨率以及密度 根据不同的分辨率进行不同的配置模拟xy点击
def getDevicesInfo(devicesList):
    for device in devicesList:
        deviceInfo = os.popen("adb -s "+device+" shell getprop ro.product.model").read()
        deviceSize = os.popen("adb -s "+device+" shell wm size").read()
        print("设备名称："+str(deviceInfo)+"设备分辨率："+str(deviceSize))


if __name__ == '__main__':
    devicesList = getDevices()
    getDevicesInfo(devicesList)