# -*- coding: utf-8 -*-
# @Time : 2022/4/10 11:46
# @Author : Hanhaha
import base64
import json
import sys

import requests
import time

from crypto import SM3
from crypto.SM4_CBC import sm4_cbc_de
from crypto.ecdh_2 import get_secret
from other.post import IP


def get_netmsg():
    # global global_name
    # global tag
    full_path = sys.path[0] + '/' + "main.json"
    with open(full_path, 'r') as file:
        js = json.load(file)
    name = js["username"]


    # name = "qq"
    full_path = sys.path[0] + '/' + "user.json"
    with open(full_path, 'r') as file:
        js_user = json.load(file)
    file.close()
    user_token = js_user[name]

    r_post = "/msg/sender"
    url = "http://" + IP + r_post

    data = {}
    data["username"] = name
    data["token"] = user_token

    res = requests.get(url, headers = data)
    print(res.text)

    sum_total = len(res.json())
    # print("num=",num)
    full_path_user = sys.path[0] + '/' + name + "msg.json"
    with open(full_path_user, 'r') as file:
        js1 = json.load(file)
    num=0
    for i in range(sum_total):
        #sum = js1["sum"]
        #num = sum + 1
        num=num+1
        msg = res.json()["msg"+str(num)]

        T = int(msg["timestamp"])

        timeArray = time.localtime(T)
        Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        sender = msg["from_user"]

        print("ReceiveKey", js["ReceiveKey"])
        CK_1 = SM3.Hash_sm3_1(js["ReceiveKey"])[0:32]
        A1 = SM3.Hash_sm3_1(js["ReceiveKey"])[32:64]
        key = bytes.fromhex(A1)
        print("AAAAAAA1",A1)

        iv = js["tag"].encode("UTF-8")

        recv_msg = bytes.fromhex(msg["text"])

        recv_msg = sm4_cbc_de(iv, key, recv_msg)
        print("recv_msg:",recv_msg)

        if sender in js1.keys():
            temp = js1[sender]
            TYPE = type(temp)
            temp[Time] = recv_msg[0:-2]
            # js1[sender] = temp.update({Time: recv_msg})
            js1[sender] = temp
        else:
            js1[sender] = {Time: recv_msg}

        js1["sum"] = num
        with open(full_path_user, 'w') as file:
            json.dump(js1, file, indent=4, ensure_ascii=False)
        file.close()

        js["ReceiveKey"] = CK_1
        with open(full_path, 'w') as file:
            json.dump(js, file, indent=4, ensure_ascii=False)
        file.close()
    '''
    
    Map{msgid :map}
    map{
        timestamp:
        from_user:
        text:
        }
    '''

# get_netmsg()