# -*- codeing = utf-8 -*-
# @Time : 2022/3/26 17:15
# @Author : jszmwq
# @File : examine_XOR.py
# @Software: PyCharm

def examine_XOR(str1):
    yihuo = 0
    for s in str1[1:-5]:
        byt = s.encode('gbk')
        yihuo ^= byt[0]
    str2 = str(hex(yihuo)).upper()[2:]
    if len(str2) == 1:
        str2 = '0' + str2
    if str2 == str1[-4:-2]:
        return True
    else:
        return False
