# -*- coding: utf-8 -*-
# @Time : 2022/3/26 14:17
# @Author : Hanhaha

import json
import sys
import time

import other.seri

import binascii

from crypto.SM4_CBC import sm4_cbc_de

from other.user import global_name
from other import globalvar


# 16进制数转字符串(utf-8)
def hex2char(data):
    output = binascii.unhexlify(data)
    string = str(output, 'UTF-8')
    return string


def recv_msg(flag):
    # flag为0时，用于认证
    serObject = other.seri.open_ser()
    print("——开始接收报文——")
    j = 0
    while 1:

        j = j + 1
        time.sleep(2)
        if serObject.ser.in_waiting:
            str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
            # print(str1)

        else:
            continue

        recv = str1.split('\n')

        for i in range(len(recv)):
            if recv[i][0:6] == "$BDTXR":
                break
        if j > 3 and flag == 1:
            break
        if recv[i][0:6] != "$BDTXR":
            print("该2s内未接收到消息")
            continue
        recv_all = recv[i].split(',')
        # 发方信息
        sender = recv_all[2]
        print("发送方卡号：", sender)
        # 报文内容
        str1 = str(recv_all[5][0:-4])
        print("报文内容:", str1)
        if not flag:
            print("北斗接收返回值[0],[1]：", recv_all[5][4:6], recv_all[5][6:-4])
            return recv_all[5][4:6], recv_all[5][6:-4]
        else:  # flag==1:发报文的返回
            if j > 3:
                return [True, ]
            else:
                return [False, recv_all[5][6:-4]]


# 为线程定义一个函数
'''
stop_threads = False时，北斗报文收线程启动
'''


def recv_thread_msg():
    serObject = other.seri.open_ser()
    print("——开始接收报文——")

    vardict = globalvar.globalvar()

    while (1):

        if vardict.get_value("stop_threads"):
            return

        time.sleep(2)
        if serObject.ser.in_waiting:
            str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
            print(str1)

        else:
            continue

        recv = str1.split('\n')

        for i in range(len(recv)):
            if (recv[i][0:6] == "$BDTXR"):
                break
        if recv[i][0:6] != "$BDTXR":
            print("该2s内未接收到消息")
            continue
        recv_all = recv[i].split(',')
        # 发方信息
        sender = recv_all[2]
        print("发送方卡号：", sender)
        # 报文内容
        str1 = str(recv_all[5][0:-4])
        print("报文内容:", str1)
        beidou_msg_handle(recv_all[5][2:-4])
    '''
    报文---
    '''
def beidou_msg_handle(MSG):
    if MSG[0:2] == '04':
        # 错误信息，都需要一个弹窗
        if MSG[2:4] == '02':
            # 发报文给服务器之后,服务器的返回值,不在线程内
            print(bytes.fromhex(MSG[2:-1]).decode("UTF-8"))
            # return [False, bytes.fromhex(recv_all[4:-1]).decode("UTF-8")]
        if MSG[2:4] == '01':
            '''
            将要接收的报文过长,无法用北斗接收,需要一个弹窗
            '''
            print(bytes.fromhex(MSG[2:-1]).decode("UTF-8"))
            # return [False, bytes.fromhex(recv_all[4:-1]).decode("UTF-8")]

    if MSG[0:2] != '03':
        return [False, "返回值接收错误"]

    T = int(MSG[18:26], 16)
    timeArray = time.localtime(T)
    Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    sender = str(MSG[2:18])
    while True:
        if sender[0:2] == '00':
            sender = sender[2:]
            # print("sender",sender)
        else:
            break
    # sender = bytes.fromhex(MSG[2:18]).decode("UTF-8")
    # print("sssender:",sender)
    sender = bytes.fromhex(sender).decode("UTF-8")

    full_path = sys.path[0] + '/' + "main.json"
    with open(full_path, 'r') as file:
        js = json.load(file)
    key = js["session_key"]

    iv = js["tag"].encode("UTF-8")
    key = bytes.fromhex(key)
    recv_msg = bytes.fromhex(MSG[26:154])

    # msg = msg.encode("UTF-8")
    recv_msg = sm4_cbc_de(iv, key, recv_msg)

    print("报文内容str:", recv_msg)
    '''
    这里要判断是否已经获取到过这个信息
    '''

    full_path = sys.path[0] + '/' + js["username"] + "msg.json"
    # print("full_path：",full_path)
    with open(full_path, 'r') as file:
        js1 = json.load(file)
    sum = js1["sum"]

    num = sum + 1

    if sender in js1.keys():
        temp = js1[sender]
        temp[Time] = recv_msg
        js1[sender] = temp
        # js1[sender] = temp.update({T: recv_msg})
    else:
        js1[sender] = {Time: recv_msg}

    js1["sum"] = num
    with open(full_path, 'w') as file:
        json.dump(js1, file, indent=4, ensure_ascii=False)
    file.close()
    # return [True, ]

# recv_msg()
# 创建线程
# try:
#     thread = threading.Thread(target=recv_msg, args='1')
#     thread.start()
# except:
#     print ("Error: unable to start thread")

# print("thread！！！")
