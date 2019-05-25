# coding = utf-8


import os
import sys
import ADBAction
import time
import threading


def swipe(device):
    ADBAction.swipeXY(device, 648, 1246, 648, 904)

if __name__ == '__main__':
    # 1，检测设备
    devices = ADBAction.getDevices()
    time.sleep(1)
    ADBAction.lightDevice(devices)
    time.sleep(2)
    ADBAction.getDevicesInfo(devices)

    # 2，打开应用
    ADBAction.startActivity("com.jifen.qukan/com.jifen.qkbase.main.MainActivity", devices)
    time.sleep(10)

    # 3，截图匹配


    # 4，滑动
    while 1:
        for device in devices:
            for i in range(3):
                t1 = threading.Thread(target=swipe, args={device})
                t1.start()
                print("开始阅读.........")
                time.sleep(0.1)
                t1.join()







    # 3，回传xml分析判断当前界面
    # for device in devices:
    #     UIXml = ADBAction.getCurrentActivityXml(device)
    #     # 分析是否有干扰框
    #     result = UIXml.xpath("//node[@resource-id='com.jifen.qukan:id/t_']")
    #     if result == []:
    #         print("没有弹出无用对话框")
    #     else:
    #         ADBAction.clickSystemKey(4, device)
    #
    #     # ADBAction.getSceenSnapshot(device)
    #     # 分析是否有奖励框
    #
    #     # 开始滑动阅读
    #     while 1:
    #         ADBAction.swipeXY(device, 733, 2017, 733, 1098)
    #         time.sleep(0.2)
    #
    #
    #     # 4，点击指定坐标
    #     # for device in devices:
    #     #     ADBAction.clickXY(device, 1032, 947)
