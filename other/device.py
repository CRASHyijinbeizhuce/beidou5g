# -*- coding: utf-8 -*-
# @Time : 2022/3/26 12:24
# @Author : Hanhaha

import base64
import json
import os
import sys
import requests
from ecdsa import ECDH, SECP256k1

from crypto import SM3
from crypto.SM3 import byte2hex
from crypto.SM4_ECB import SM4Cipher
from crypto.ecdh_2 import get_secret, get_PK
from crypto.xor import xor_1
from other.Get_id import get_cardid
from other.PUF import get_mac_address
from other.get_random import get_random_str
from other.net_state import net_state
from other.post import post_1
from other.send import send_msg_beidou
from other.timestamp import time_stamp


def devi():

    puf = SM3.Hash_sm3(get_mac_address(), 1)
    # 判断主密钥是否存在
    filename = r'./main.json'
    id = get_cardid()
    tag = id[0] + "/" + id[1]

    full_path = sys.path[0] + '/' + "main.json"
    js = {}
    js["tag"] = tag
    if not os.path.exists(filename):
        with open(full_path, 'w') as file:
            json.dump(js, file, indent=4, ensure_ascii=False)
        file.close()

    # str1="0194533/02097151"
    data = {}

    with open(full_path, 'r') as file:
        js = json.load(file)
    file.close()

    if 'main_key' not in js.keys():
        # 开始注册
        if len(tag) == 16:
            if not net_state():
                return [False, "网络信号差，无法进行设备注册"]

            r_post = "/device/register"
            data['TAG'] = tag
            data['puf'] = puf
            try:
                result = post_1(r_post, data)
            except requests.exceptions.ConnectionError:
                return [False, '与服务器连接失败']
            errcode = result.json()["errorcode"]
            if errcode == 0:
                full_path = sys.path[0] + '/' + "main.json"

                str1 = bytes(tag, 'UTF-8').hex()
                key = bytes.fromhex(str1)
                sm4 = SM4Cipher(key)

                mainkey = result.json()["mainkey"]
                # 十六进制字符串
                ServerPublicKey = result.json()["ServerPublicKey"]

                main_key = bytes.fromhex(mainkey)

                main_key = sm4.decrypt(main_key).hex()

                js = {}
                main_key = xor_1(main_key, tag)
                with open(full_path, 'r') as file:
                    js = json.load(file)
                file.close()

                with open(full_path, 'w') as file:
                    js["main_key"] = base64.b64encode(main_key.encode("UTF-8")).decode("UTF-8")
                    print(base64.b64encode(main_key.encode("UTF-8")).decode("UTF-8"))
                    js["SeverPublicKey"] = ServerPublicKey
                    json.dump(js, file, indent=4, ensure_ascii=False)
                file.close()

            else:
                return [False, result.json()["errormsg"]]

        else:
            return [False, "本设备不可访问服务器"]

    # 设备认证

    t_stamp = time_stamp()
    R_1 = get_random_str(32)
    H_1 = R_1 + str(t_stamp) + puf + tag

    authenparam = SM3.Hash_sm3(H_1)
    # 获取主密钥
    full_path = sys.path[0] + '/' + "main.json"
    js = {}
    with open(full_path, 'r') as file:
        js = json.load(file)
        SK = js["main_key"]
        remote_public_key = js["SeverPublicKey"]
    file.close()

    SK = base64.b64decode(SK).hex()
    print("RK0=",SK)

    '''
    tag:str
    t_stamp:int
    authenparam:str
    encnum:bytes
    '''
    if net_state():
        with open(full_path, 'r') as file:
            js = json.load(file)
        file.close()
        FLAG = 0
        # FLAG=1时需要获取新token
        if 'device_token' in js.keys():
            t = base64.b64decode(js["device_token"])
            a = bytearray(t)
            issuetime = byte2hex(a[17:25])
            usingtime = byte2hex(a[25:29])

            issuetime = int(issuetime, 16)
            usingtime = int(usingtime, 16)

            ddl = int(issuetime) + usingtime
            t_stamp_1 = time_stamp()

            print("t_stamp_1",t_stamp_1)
            print("ddl", ddl)
            if t_stamp_1 <= ddl:
                r_post = "/device/authens"
                data = dict()
                data['Token'] = js["device_token"]

                try:
                    res = post_1(r_post, data)
                except requests.exceptions.ConnectionError:
                    return [False, '与服务器连接失败']

                errcode = res.json()["errorcode"]
                print("errcode:",errcode)
                if errcode == 1:
                    FLAG = 1
                else:
                    # FLAG = 2
                    return [True, ]
            else:
                FLAG = 1
        if (not ('device_token' in js.keys())) or FLAG == 1:
            '''
            棘轮
            '''
            ecdh = ECDH(curve=SECP256k1)
            result = get_PK(ecdh)
            ecdh = result[0]
            ClientPublicKey = result[1]

            result = get_secret(ecdh,remote_public_key)
            ecdh = result[0]
            secret = result[1]

            RK = SM3.Hash_sm3_1(SK+secret)[0:32]
            CK = SM3.Hash_sm3_1(SK+secret)[32:64]

            CK_1 = SM3.Hash_sm3_1(CK)[0:32]
            A1 = SM3.Hash_sm3_1(CK)[32:64]

            key = bytes.fromhex(A1)
            sm4 = SM4Cipher(key)
            R = bytes.fromhex(R_1)
            encnum = sm4.encrypt(R)

            r_post = "/device/authen"
            data = dict()
            data['TAG'] = tag
            t_stamp = str(t_stamp)
            data['timestamp'] = t_stamp
            data['authenparam'] = base64.b64encode(authenparam.encode("UTF-8"))
            data['encnum'] = base64.b64encode(encnum)
            data['PKc'] = ClientPublicKey

            res = post_1(r_post, data)

        # print(res.text)
        errcode = res.json()["errorcode"]
        # if FLAG == 2:
        #     return [True, ]
        if errcode == 0:
            device_token = res.json()["device_token"]

            full_path = sys.path[0] + '/' + "main.json"
            with open(full_path, 'r') as file:
                js = json.load(file)
            file.close()
            js["device_token"] = device_token
            js["SendKey"] = CK_1
            js["ServerPublicKey"] = res.json()["ServerPublicKey"]

            #hash(RK||secret)
            # 前面是下一个RK，后面是recvkey
            result = get_secret(ecdh,res.json()["ServerPublicKey"])
            secret = result[1]
            ecdh = result[0]
            js["RK"] = SM3.Hash_sm3_1(RK + secret)[0:32]
            js["ReceiveKey"] = SM3.Hash_sm3_1(RK + secret)[32:64]

            ecdh = result[0]
            with open(full_path, 'w') as file:
                json.dump(js, file, indent=4, ensure_ascii=False)
            file.close()
            # session_key.append(s_k)

            return [True, ]
        else:
            return [False, res.json()["errormsg"]]

    # 通过北斗进行设备认证
    else:
        print("通过北斗进行设备认证")
        with open(full_path, 'r') as file:
            js = json.load(file)
        file.close()
        FLAG = 0
        # FLAG=1时需要获取新token
        if "device_token" in js.keys():
            # 用token进行认证
            t = base64.b64decode(js["device_token"])
            a = bytearray(t)
            issuetime = byte2hex(a[17:25])
            usingtime = byte2hex(a[25:29])

            issuetime = int(issuetime, 16)
            usingtime = int(usingtime, 16)

            ddl = issuetime + usingtime
            ddl = int(ddl / 1000)

            t_stamp_1 = time_stamp()
            print("当前时间：",t_stamp_1)
            print("DDL=", ddl)
            if t_stamp_1 <= ddl:
                # 发token，收错误代码
                result = send_msg_beidou("0102", byte2hex(t), 0, None)
                if result[0]:
                    return [True, ]
                else:
                    return [False, result[1]]
                # result = recv_msg(0)
                #
                # if result[0] == '03':
                #     print("errormsg:",bytes.fromhex(result[1]).decode("UTF-8"))
                #     print("收到了03！")
                #     FLAG = 1
                # if result[0] == '05':
                #     print("errormsg:", bytes.fromhex(result[1]).decode("UTF-8"))
                #     FLAG = 1
                # if result[0] == '06':
                #     return [True, ]
            else:
                print("?")
                FLAG = 1

        # print("flag=",FLAG)
        if "device_token" not in js.keys() or FLAG == 1:

            CK_1 = SM3.Hash_sm3_1(js["SendKey"])[0:32]
            A1 = SM3.Hash_sm3_1(js["SendKey"])[32:64]
            key = bytes.fromhex(A1)
            sm4 = SM4Cipher(key)
            R = bytes.fromhex(R_1)
            encnum = sm4.encrypt(R)

            TAG = bytes(tag, 'gbk').hex()
            t_stamp = str(hex(t_stamp)[2:]).zfill(16)
            result = send_msg_beidou("0101", TAG + t_stamp + authenparam + encnum.hex(), 0, None)
            if not result[0]:
                return [False, result[-1]]
            print("北斗设备认证发送成功")
            device_token = base64.b64encode(result[1])
            full_path = sys.path[0] + '/' + "main.json"
            with open(full_path, 'r') as file:
                js = json.load(file)
            file.close()
            print("设备token：",device_token)
            js["device_token"] = device_token.decode("UTF-8")
            js["SendKey"] = CK_1

            with open(full_path, 'w') as file:
                json.dump(js, file, indent=4, ensure_ascii=False)
            file.close()
            return [True, ]
