# -*- coding: utf-8 -*-
# @Time : 2022/3/22 20:02
# @Author : Hanhaha

# 假的PUF
import uuid


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    # return mac.upper()
    # return ":".join([mac[e:e+2] for e in range(0,11,2)])

    yihuo = 0
    for s in mac:
        byt = s.encode('gbk')
        yihuo ^= byt[0]
    str2 = str(hex(yihuo)).upper()[2:]
    if (len(str2) == 1):
        str2 = '0' + str2
    return (mac + str2).upper()

# print(get_mac_address())
