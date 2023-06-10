# -*- codeing = utf-8 -*-
# @Time : 2022/3/26 17:14
# @Author : jszmwq
# @File : generate_XOR.py
# @Software: PyCharm

def generate_XOR(str1):
    yihuo = 0
    for s in str1[1:]:
        byt = s.encode('gbk')
        yihuo ^= byt[0]
    str2 = str(hex(yihuo)).upper()[2:]
    if len(str2) == 1:
        str2 = '0' + str2
    return "$" + str1 + "*" + str2 + "\r\n"
