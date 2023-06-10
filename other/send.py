# -*- coding: utf-8 -*-
# @Time : 2022/3/26 15:22
# @Author : Hanhaha
import json
import sys
import threading
import time
import other.seri
from ttkbootstrap.dialogs import Messagebox
import other.generate_XOR
from crypto import SM3
from crypto.SM4_CBC import sm4_cbc_en
# from other.device import tag
from other.Thread_operation import thread_closed, thread_on
from other.recv import recv_msg

from other.timestamp import time_stamp

beidounum = "0194393"

# def send_beidou_msg(rcvr, msg):  # 这里传的msg就是要传的字符串,在本方法里(转为bytes再)转为16进制
#     serObject = other.seri.open_ser()
#     recv_name = rcvr.encode("UTF-8").hex()
#     if recv_name > 16:
#         return [False, "收方用户名错误"]
#     '''
#     参数来源?
#     '''
#     iv = "".encode("UTF-8")
#     key =bytes.fromhex("")
#     msg = msg.encode("UTF-8")
#     if len(msg) > 128:
#         return [False, '发送报文长度应小于64字节']
#     en_msg = sm4_cbc_en(iv, key, msg)
#     encrypt_msg = bytes(en_msg, 'gbk').hex()
#     # 注意msg格式应为str形式，不为byte形式
#
#
#     encrypt_msg = bytes(msg, 'UTF-8').hex()
#     # print("报文的十六进制形式：", encrypt_msg)
#
#     print("报文的十六进制形式：", encrypt_msg)
#
#
#     str1 = "CCTXA," + beidounum + ",1,2,A4" + "0301" + recv_name.upper() + encrypt_msg.upper()
#
#     yihuo = 0
#     for s in str1:
#         byt = s.encode('UTF-8')
#         yihuo ^= byt[0]
#     str2 = str(hex(yihuo)).upper()[2:]
#
#     if len(str2) == 1:
#         str2 = '0' + str2
#
#     s_str = "$" + str1 + "*" + str2 + "\r\n"
#
#     # s_str = other.generate_XOR.generate_XOR(str1)
#     print(s_str)
#
#     while 1:
#         # result = ser.write("$CCTXA,0194393,1,1,68656C6C6FB1B1B6B7*09".encode("gbk"))
#         result = serObject.ser.write(s_str.encode("gbk"))
#
#         time.sleep(3)
#         if serObject.ser.in_waiting:
#             # 这个地方感觉不太对劲。。。。
#             str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
#             print(str1)
#             recv = str1.split('\n')
#             print(recv)
#             result1 = ''
#             for i in range(len(recv)):
#                 if recv[i][0:6] == "$BDFKI":
#                     result1 = recv[i]
#                     break
#             if result1 == '':
#                 continue
#             recv_all = result1.split(',')
#             if recv_all[2] == 'N':
#                 # print("发送失败")
#                 return [False, '发送失败，请等待%s秒后重新发送' % recv_all[5][0:4]]
#             else:
#                 # 下面两个句子暂不清楚含义
#                 # ser.flushInput()
#                 # str = ser.read_all()
#                 return [True, '发送成功']

True == True
# FLAG=1时,为用户发送报文
# head:
# 设备认证:01
#     01:首次认证   02:Token认证
# 用户认证:02
#     01:首次认证   02:Token认证
# 用户发报文:03
# 这里传的直接就是十六进制数
# 认证时rcvr为空
def send_msg_beidou(head, msg, FLAG, rcvr):
    # stop_threads = True
    print("北斗接收已关闭")
    serObject = other.seri.open_ser()
    if FLAG==1 :
        msg = msg.encode("UTF-8")
        recv_name = rcvr.encode("UTF-8").hex()
        if len(recv_name) > 16:
            return [False, "收方用户名错误"]
        if len(msg) > 64:#64字节??
            return [False, '发送报文长度应小于64字节']
        # from other.device import tag
        # iv = tag[0].encode("UTF-8")

        full_path = sys.path[0] + '/' + "main.json"
        with open(full_path, 'r') as file:
            js = json.load(file)
        file.close()

        iv = js["tag"].encode("UTF-8")
        # key = bytes.fromhex(js["session_key"])
        T = time_stamp()
        s_k = SM3.Hash_sm3(js["session_key"] + str(T))[0:32]
        key = bytes.fromhex(s_k)

        en_msg = sm4_cbc_en(iv, key, msg)
        encrypt_msg = en_msg.hex()

        recv_name = recv_name.zfill(16)

        str1 = "CCTXA," + beidounum + ",1,2,A4" + head + recv_name.upper() + str(hex(T))[2:].upper() + encrypt_msg.upper()


        '''
        中断北斗收线程
        '''
        thread_closed()

    else:
        str1 = "CCTXA," + beidounum + ",1,2,A4" + head + msg.upper()

    # 计算校验字节
    yihuo = 0
    for s in str1:
        byt = s.encode('UTF-8')
        yihuo ^= byt[0]
    str2 = str(hex(yihuo)).upper()[2:]

    if len(str2) == 1:
        str2 = '0' + str2
    s_str = "$" + str1 + "*" + str2 + "\r\n"
    print("发送报文",s_str)

    j = 0
    while (1):
        j = j + 1
        serObject.ser.flushInput()
        result = serObject.ser.write(s_str.encode("gbk"))
        time.sleep(2)
        if serObject.ser.in_waiting:
            str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
            recv = str1.split('\n')
            print(recv)

            result2 = ''
            for i in range(len(recv) + 1):
                if recv[i][0:6] == "$BDFKI":
                    result2 = recv[i]
                    break
            if result2 == "":
                continue
                # 后面可以通过检查当前是否可发送来取消/加入这个wait
                # time.sleep(40)
            recv_all = result2.split(',')

            # print("开始持续接受北斗消息")
            # from other.recv import recv_msg
            # try:
            #     stop_threads= False
            #     thread = threading.Thread(target=recv_msg, args='1')
            #     thread.start()
            # except:
            #     print("Error: unable to start thread")


            if recv_all[2] == 'N':
                print("发送失败")
                if FLAG ==1 :
                    '''
                    北斗继续接收报文
                    '''
                    thread_on()

                    return [False, '发送失败，请等待%s秒后重新发送' % recv_all[5][0:4]]
                if j > 30:
                    return [False,encrypt_msg ]
            else:
                # 发送成功
                print("北斗发送成功")
                if FLAG == 1:
                    # js["session_key"] = s_k
                    # full_path = sys.path[0] + '/' + "main.json"
                    # with open(full_path, 'w') as file:
                    #     json.dump(js, file, indent=4, ensure_ascii=False)
                    # file.close()
                    '''
                    北斗继续接收报文
                    '''
                    thread_on()

                    return [True, ]

                #接收服务器返回的消息
                # if head == '03':
                #     result = recv_msg(1)
                #     if not result[0] == '02':
                #         return

                result = recv_msg(0)
                print("FLAG=",FLAG)
                if result[0] == '03':
                    print("errormsg:",bytes.fromhex(result[1]).decode("UTF-8"))
                    return [False, '1', bytes.fromhex(result[1]).decode("UTF-8")]
                if result[0] == '04':#返回Token

                    print("errormsg:", bytes.fromhex(result[1]))
                    return [True, bytes.fromhex(result[1])]
                if result[0] == '05':
                    print("errormsg:", bytes.fromhex(result[1]).decode("UTF-8"))
                    return [False, '1']
                if result[0] == '06':
                    return [True, ]


