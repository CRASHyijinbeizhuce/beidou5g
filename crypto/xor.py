# -*- coding: utf-8 -*-
# @Time : 2022/3/27 10:47
# @Author : Hanhaha
'''
for s in str1:
    byt = s.encode('gbk')
    yihuo ^= byt[0]
str2=str(hex(yihuo)).upper()[2:]'''

def xor_1(str1,str2):#str1是解密后的值,str2是卡号/序列号
    if (len(str1) != 32) or (len(str2) != 16):
        return
    str22 = str2 + str2
    str1 = bytearray(str1, "UTF-8")
    str22 = bytearray(str22, "UTF-8")
    for i in range(0, 32):
        str22[i] ^= str1[i]
    return str22.decode("UTF-8")

# res = xor_1("41424444393538343431423246363031","0194533/02097151")
# print(res.encode("UTF-8"))
# print(len(res))
