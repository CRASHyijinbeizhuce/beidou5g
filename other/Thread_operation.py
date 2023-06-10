# -*- coding: utf-8 -*-
# @Time : 2022/4/19 15:42
# @Author : Hanhaha
import threading

from other import globalvar
from other.recv import recv_thread_msg

global thread_1

def thread_on():
    global thread_1
    # print("线程开始1")
    vardict = globalvar.globalvar()
    vardict.set_value("stop_threads", False)
    thread_1 = threading.Thread(target=recv_thread_msg)
    # thread_1 = threading.Thread(target=run, args='1')
    thread_1.start()
    # print("开始thread", thread_1)
    # vardict.set_value("thread_1", thread_1)
    # print("线程开始2")
    return


def thread_closed():
    global thread_1
    # print("线程关闭1")
    vardict = globalvar.globalvar()
    vardict.set_value("stop_threads", True)
    # thread_1 = vardict.get_value("thread_1")
    # print("关闭thread", thread_1)
    thread_1.join()
    # print("线程关闭2")
    return