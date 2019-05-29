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
import mayitoutiao
import qutoutiao


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
    print("结束线程")



if __name__ == '__main__':
    devices = qutoutiao.init()
    threads = []
    for device in devices:
        threads.append(threading.Thread(target=qutoutiao.mainExcute, args=(device,)))

    for t in threads:
        t.start()
        print("开启线程QuTou---")
    startTime = time.time()

    while 1:
        if (time.time() - startTime) > 60:
            for t in threads:
                stop_thread(t)

    for device in devices:
        threads.append(threading.Thread(target=mayitoutiao.mainExcute, args=(device,)))

    for t in threads:
        t.start()
        print("开启线程MaYi---")



