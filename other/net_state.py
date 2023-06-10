# -*- coding: utf-8 -*-
# @Time : 2022/3/20 11:21
# @Author : Hanhaha
from datetime import time
import time
import os
import subprocess
import platform
from other import seri
# !/usr/bin/env python
# coding:utf-8
from other.post import IP


def net_state():
    fnull = open(os.devnull, 'w')
    if platform.system().lower() == 'linux':
        # 注意 树莓派中终端 对ping需要加入次数，否则会无限获取
        return1 = subprocess.run('ping -c 10 www.baidu.com', shell=True, stdout=fnull)
        # return1 = subprocess.run('ping -c 10 '+IP, shell=True, stdout=fnull)
    else:
        # 但是上述命令在windows下适用
        return1 = subprocess.run('ping www.baidu.com', shell=True, stdout=fnull)
        # return1 = subprocess.run('ping '+IP, shell=True, stdout=fnull)
    if return1.returncode:
        # 'ping fail'
        fnull.close()
        return False
    else:
        # 'ping ok'
        fnull.close()
        return True


def beidou_state():
    serObject = seri.open_ser()
    # 检测信号状态
    result = serObject.ser.write("$CCRMO,BSI,2,0*26\r\n".encode("gbk"))
    print("写总字节数:", result)

    time.sleep(1)
    if serObject.ser.in_waiting:
        str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
        print(str1)
        str1 = str1[1:-5].split(',')
        for i in str1[3:]:
            if i == '4':
                # print("当前信号良好，可以使用")
                return True

    # print("当前信号差，无法使用")
    return False


# print(net_state())
