# -*- coding: utf-8 -*-
# @Time : 2022/4/7 21:52
# @Author : Hanhaha
import json
import sys

from crypto import SM3
from crypto.SM4_CBC import sm4_cbc_en
from other.post import post_1
from other.timestamp import time_stamp


def send_net_msg(rcvr, msg):
    data = {}

    full_path = sys.path[0] + '/' + "main.json"
    with open(full_path, 'r') as file:
        js = json.load(file)
    file.close()

    '''
    msg在这里加密
    还要发其他的一系列的加密......
    '''
    t_stamp = time_stamp()

    CK_1 = SM3.Hash_sm3_1(js["SendKey"])[0:32]
    A1 = SM3.Hash_sm3_1(js["SendKey"])[32:64]
    key = bytes.fromhex(A1)


    iv = js["tag"].encode("UTF-8")
    msg = msg.encode("UTF-8")
    en_msg = sm4_cbc_en(iv, key, msg)   # bytes


    r_post='/msg/receiver'
    data['Msg'] = en_msg.hex()
    data['TAG'] = js["tag"]
    data['username'] = rcvr
    data['timestamp'] = t_stamp

    res = post_1(r_post, data)
    errcode = res.json()["errorcode"]
    if errcode==0:
        js["SendKey"] = CK_1
        with open(full_path, 'w') as file:
            json.dump(js, file, indent=4, ensure_ascii=False)
        file.close()
        return [True,en_msg.hex()]
    else:
        return [False, res.json()["errormsg"]]

# result = send_net_msg("abc", "hello")
# if result[0]:
#     print("发送成功")
# else:
#     print(result[1])
