# -*- coding: utf-8 -*-
# @Time : 2022/4/20 13:23
# @Author : Hanhaha
import base64
import json
import os
import sys

from other.net_state import net_state
from other.post import post_1
from other.send import send_msg_beidou
from other.timestamp import time_stamp

'''
未测试
'''
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

        ddl = int(issuetime/1000) + usingtime
        #ddl = int(ddl / 1000)
        t_stamp_1 = time_stamp()

        if t_stamp_1 +100 <= ddl:
            u_Token[name] = js[name]

    if u_Token:
        return [True, u_Token]#{username:token}
    else:
        return [False, ]


def Token_login(Token):
    '''
    :param Token:
    :return: [BOOL, errmsg]
    '''
    if net_state():
        r_post = "/user/authens"
        data = dict()
        data['Token'] = Token
        res = post_1(r_post, data)
        errcode = res.json()["errorcode"]
        if errcode == 0:
            return [True, ]
        else:
            return [False, res.json()["errormsg"]]
    else:#应该判断北斗信号好不好
        result = send_msg_beidou("0202", base64.b64decode(Token).hex(), 0, None)
        if result[0]:
            return [True, ]
        else:
            return [False, result[1]]
