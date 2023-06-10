# -*- coding: utf-8 -*-
# @Time : 2022/3/29 20:03
# @Author : Hanhaha
import base64
import json
import os
import sys
import time

from crypto import SM3
from crypto.SM3 import Hash_sm3, str2byte, byte2hex, hex2byte
from crypto.SM4_ECB import SM4Cipher
import other.device

from other.get_random import get_random_str
from other.net_state import net_state
from other.post import post_1

from other.timestamp import time_stamp

global_name = None
#session_key在json文件里是16进制数

def user_Token():
    '''
    :return: [BOOL, {username:token}]
    '''

    full_path = sys.path[0] + '/' + "user.json"
    filename = r'./user.json'
    if not (os.path.exists(filename) or os.path.getsize(filename)):
        return [False, ]
    with open(full_path, 'r') as file:
        js = json.load(file)
    file.close()
    u_Token = {}
    for name in js:
        #检查token是否过期
        t = base64.b64decode(js[name])
        a = bytearray(t)
        issuetime = a[17:25].hex()
        usingtime = a[25:29].hex()

        issuetime = int(issuetime, 16)
        usingtime = int(usingtime, 16)

        ddl = int(issuetime) + usingtime#除1000后没有返回值
        #ddl = int(ddl / 1000)
        t_stamp_1 = time_stamp()

        if t_stamp_1 +100 <= ddl:
            u_Token[name] = js[name]
    #username = list(u_Token.keys())
    if u_Token:
        #return [True, u_Token]#{username:token}
        return list(u_Token.keys())
    else:
        #return [False, ]
        return None


def post_login(name, secret):
    full_path_main = sys.path[0] + '/' + "main.json"
    with open(full_path_main, 'r') as file:
        js = json.load(file)
    file.close()

    tag = js["tag"]

    full_path = sys.path[0] + '/' + "user.json"
    # with open(full_path, 'w') as file:
    #     # js_user = json.load(file)
    #     file.close()

    token = js["device_token"]
    secret = Hash_sm3(secret)
    t_stamp = time_stamp()
    R_1 = get_random_str(32)  # 16字节的随机数
    H_1 = str(R_1) + str(t_stamp) + secret + token
    print("hash前：", H_1)
    # 认证参数
    authenparam = bytes.fromhex(Hash_sm3(H_1))
    # 用会话密钥加密
    CK_1 = SM3.Hash_sm3_1(js["SendKey"])[0:32]
    A1 = SM3.Hash_sm3_1(js["SendKey"])[32:64]
    key = bytes.fromhex(A1)
    sm4 = SM4Cipher(key)
    # key = bytes.fromhex(s_k)
    # print("key44::", base64.b64encode(key))
    # sm4 = SM4Cipher(key)

    R = bytes.fromhex(R_1)
    encnum = sm4.encrypt(R) + sm4.encrypt(bytearray(name, "UTF-8"))
    print("encnum=", encnum.hex())
    if net_state():
        filename = r'./user.json'
        FLAG = 0

        if not os.path.exists(filename):
            with open(full_path, 'w') as file:
                js_user = {"admin":"Token"}
                json.dump(js_user, file, indent=4, ensure_ascii=False)
                file.close()

        if os.path.exists(filename):
            with open(full_path, 'r') as file:
                js_user = json.load(file)
            file.close()
            # FLAG=1时需要获取新token
            if name in js_user.keys():
                t = base64.b64decode(js_user[name])
                a = bytearray(t)
                issuetime = byte2hex(a[17:25])
                usingtime = byte2hex(a[25:29])

                issuetime = int(issuetime, 16)
                usingtime = int(usingtime, 16)

                #ddl = issuetime + usingtime
                #ddl = int(ddl / 1000)
                ddl = int(issuetime) + usingtime

                t_stamp_1 = time_stamp()

                print(ddl)
                print(t_stamp_1)

                if t_stamp_1 <= ddl:
                    r_post = "/user/authens"
                    data = dict()
                    data['Token'] = js_user[name]
                    res = post_1(r_post, data)
                    errcode = res.json()["errorcode"]
                    if errcode == 1:
                        FLAG = 1
                    else:
                        FLAG = 2
                else:
                    FLAG = 1

        if (not name in js_user.keys()) or FLAG == 1:
            data = {}
            data['TAG'] = tag
            data['timestamp'] = t_stamp
            data['authenparam'] = base64.b64encode(authenparam)
            print("认证参数：", base64.b64encode(authenparam))
            # print("加密后长度:",len(encnum))
            data['encnum'] = base64.b64encode(encnum)

            r_post = "/user/authen"
            res = post_1(r_post, data)

            # with open(full_path, 'r') as file:
            #     js_user = json.load(file)
            # file.close()

            errcode = res.json()["errorcode"]
            if errcode == 0:
                js_usr = {}
                js_usr[name] = res.json()["user_token"]
                js["SendKey"] = CK_1
                with open(full_path, 'w') as file:
                    json.dump(js_usr, file, indent=4, ensure_ascii=False)
                file.close()

                with open(full_path_main, 'w') as file:
                    json.dump(js, file, indent=4, ensure_ascii=False)
                file.close()
                # global global_name
                global_name = name
                return [True, ]
            else:
                return [False, res.json()["errormsg"]]
        if FLAG == 2:
            print("用户Token验证成功!")
            return [True, ]

    else:
        print("通过北斗进行设备认证")
        # 用北斗发
        TAG = tag  # 16
        TAG = TAG.encode("UTF-8").hex()

        R_1 = get_random_str(16)  # 8字节的随机数
        H_1 = str(R_1) + str(t_stamp) + secret + token
        authenparam = Hash_sm3(H_1)  # 32

        str1 = bytes.fromhex(R_1) + name.encode("UTF-8")
        # str1 = bytearray(bytes.fromhex(R_1)) + bytearray(name, "UTF-8")
        print("加密前长度（字节）:", len(str1))
        encnum = sm4.encrypt(str1)

        # isNone = 0
        filename = r'./user.json'
        if not os.path.exists(filename):
            with open(full_path, 'w') as file:
                js_user = {"admin":"token"}
                json.dump(js_user, file, indent=4, ensure_ascii=False)
                file.close()


        with open(full_path, 'r') as file:
            js_user = json.load(file)
        file.close()
        FLAG = 0

        # FLAG=1时需要获取新token
        # if js_user[name] is not None:
        if name in js_user.keys():
            # 用token进行认证
            t = base64.b64decode(js_user[name])
            a = bytearray(t)
            issuetime = byte2hex(a[17:25])
            usingtime = byte2hex(a[25:29])

            issuetime = int(issuetime, 16)
            usingtime = int(usingtime, 16)

            ddl = issuetime + usingtime
            ddl = int(ddl / 1000)

            t_stamp_1 = time_stamp()
            if t_stamp_1 <= ddl:
                # 发token，收错误代码
                from other.send import send_msg_beidou
                result = send_msg_beidou("0202", byte2hex(a), 0, None)
                if  result[0]:
                    return [True, ]
                else:
                    return [False, result[1]]
                # result = recv_msg(0)
                # if result == "03":
                #     errmsg = bytes.fromhex(result[1]).decode("UTF-8")
                #     return [False, errmsg]
                # if result == "05":
                #     FLAG = 1
                # if result == "06":
                #     return [True, ]
            else:
                FLAG = 1

        if name not in js_user.keys() or FLAG == 1:
            t_stamp = time_stamp()
            t_stamp = str(hex(t_stamp)[2:]).zfill(16)
            # authenparam, encnum.hex()
            from other.send import send_msg_beidou
            result = send_msg_beidou("0201", TAG + t_stamp + authenparam + encnum.hex(), 0, None)
            if not result[0]:
                return [False, result[-1]]
            # 存入token
            # msg是十六进制，要转为base64形式
            user_token = base64.b64encode(result[1])
            with open(full_path_main, 'r') as file:
                js = json.load(file)
            file.close()
            js["SendKey"] = CK_1
            with open(full_path_main, 'w') as file:
                json.dump(js, file, indent=4, ensure_ascii=False)
            file.close()

            with open(full_path, 'r') as file:
                js_user = json.load(file)
            file.close()
            js_user[name] = user_token.decode("UTF-8")
            # print("usertoken=",user_token)
            # print("type:",type(user_token))
            with open(full_path, 'w') as file:
                json.dump(js_user, file, indent=4, ensure_ascii=False)
            file.close()


            return [True, ]


def post_phonenum(phonenum):
    # key = bytes.fromhex(session_key[0])
    # print("设备会话密钥::", base64.b64encode(key))
    full_path = sys.path[0] + '/' + "main.json"
    # file = open(full_path)
    with open(full_path, 'r') as file:
        js = json.load(file)
        tag = js["tag"]

    CK_1 = SM3.Hash_sm3_1(js["SendKey"])[0:32]
    A1 = SM3.Hash_sm3_1(js["SendKey"])[32:64]
    key = bytes.fromhex(A1)
    sm4 = SM4Cipher(key)

    phonenum = str(phonenum).encode("UTF-8")
    encnum = sm4.encrypt(phonenum)

    if not net_state():
        return [False, "网络状态不佳，无法进行手机号验证"]
    r_post = "/user/register/firsts"
    data = {}
    data['TAG'] = tag
    data['phonenumber'] = base64.b64encode(encnum)
    res = post_1(r_post, data)

    errcode = res.json()["errorcode"]
    errmsg = res.json()["errormsg"]
    if errcode == 0:
        js["SendKey"] = CK_1
        with open(full_path, 'w') as file:
            json.dump(js, file, indent=4, ensure_ascii=False)
        file.close()
        return [True, errmsg]
    else:
        return [False, errmsg]


def post_register(name, secret, phonenum, vercode):
    # key = bytes.fromhex(other.device.session_key[0])
    # print("key::", base64.b64encode(key))
    full_path = sys.path[0] + '/' + "main.json"
    with open(full_path, 'r') as file:
        js = json.load(file)
    file.close()


    CK_1 = SM3.Hash_sm3_1(js["SendKey"])[0:32]
    A1 = SM3.Hash_sm3_1(js["SendKey"])[32:64]
    key = bytes.fromhex(A1)
    sm4 = SM4Cipher(key)


    secret = Hash_sm3(secret)

    name = name.encode("UTF-8")
    enname = sm4.encrypt(name)

    # print("len=",len(secret))
    secret1 = bytes.fromhex(secret[0:32])
    secret2 = bytes.fromhex(secret[32:])
    ensecret = bytearray(sm4.encrypt(secret1)) + bytearray(sm4.encrypt(secret2))

    phonenum = phonenum.encode("UTF-8")
    enphonenum = sm4.encrypt(phonenum)

    full_path = sys.path[0] + '/' + "main.json"
    # file = open(full_path)
    with open(full_path, 'r') as file:
        js = json.load(file)
        token = js["device_token"]
        print(token)
    # file.close()

    if net_state():
        r_post = "/user/register/seconds"
        data = dict()  # Post请求发送的数据，字典格式
        data['username'] = base64.b64encode(enname)
        data['password'] = base64.b64encode(ensecret)
        data['phonenumber'] = base64.b64encode(enphonenum)
        data['TAG'] = js["tag"]
        data['vercode'] = vercode
        data['Token'] = token
        res = post_1(r_post, data)  # 这里使用post方法，参数和get方法一样

        errcode = res.json()["errorcode"]
        print("----", res.text)

        if errcode == 0:
            # token = res.json()["token"]
            # 更新密钥
            js["SendKey"] = CK_1
            with open(full_path, 'w') as file:
                json.dump(js, file, indent=4, ensure_ascii=False)
            file.close()
            return [True, ]
        else:
            errmsg = res.json()["errormsg"]
            return [False, errmsg]
    else:
        return [False, "网络状态不佳，无法进行用户注册"]


def post_phonenum_forget(phonenum):
    full_path = sys.path[0] + '/' + "main.json"
    with open(full_path, 'r') as file:
        js = json.load(file)
    file.close()

    CK_1 = SM3.Hash_sm3_1(js["SendKey"])[0:32]
    A1 = SM3.Hash_sm3_1(js["SendKey"])[32:64]
    key = bytes.fromhex(A1)
    sm4 = SM4Cipher(key)

    phonenum = str(phonenum).encode("UTF-8")
    encnum = sm4.encrypt(phonenum)

    if not net_state():
        return [False, "网络状态不佳，无法进行手机号验证"]
    r_post = "/user/changesecret/firsts"
    data = {}
    data['TAG'] = js["tag"]
    data['phonenumber'] = base64.b64encode(encnum)
    res = post_1(r_post, data)

    errcode = res.json()["errorcode"]
    errmsg = res.json()["errormsg"]
    if errcode == 0:
        # 更新密钥
        js["SendKey"] = CK_1
        with open(full_path, 'w') as file:
            json.dump(js, file, indent=4, ensure_ascii=False)
        file.close()
        return [True, errmsg]
    else:
        return [False, errmsg]

def post_register_forget(secret, phonenum, vercode):
    # key = bytes.fromhex(other.device.session_key[0])
    # print("key::", base64.b64encode(key))

    full_path = sys.path[0] + '/' + "main.json"
    with open(full_path, 'r') as file:
        js = json.load(file)
    key = bytes.fromhex(js["session_key"])

    sm4 = SM4Cipher(key)
    secret = Hash_sm3(secret)

    # print("len=",len(secret))
    secret1 = bytes.fromhex(secret[0:32])
    secret2 = bytes.fromhex(secret[32:])
    ensecret = bytearray(sm4.encrypt(secret1)) + bytearray(sm4.encrypt(secret2))

    phonenum = phonenum.encode("UTF-8")
    enphonenum = sm4.encrypt(phonenum)

    # file = open(full_path)
    with open(full_path, 'r') as file:
        js = json.load(file)
        token = js["device_token"]
    file.close()

    if net_state():
        r_post = "/user/changesecret/seconds"
        data = dict()  # Post请求发送的数据，字典格式
        data['password'] = base64.b64encode(ensecret)
        data['phonenumber'] = base64.b64encode(enphonenum)
        data['TAG'] = js["tag"]
        data['vercode'] = vercode
        data['Token'] = token
        res = post_1(r_post, data)  # 这里使用post方法，参数和get方法一样

        errcode = res.json()["errorcode"]
        print("----", res.text)

        if errcode == 0:
            return [True, ]
        else:
            errmsg = res.json()["errormsg"]
            return [False, errmsg]
    else:
        return [False, "网络状态不佳，无法进行密码修改"]