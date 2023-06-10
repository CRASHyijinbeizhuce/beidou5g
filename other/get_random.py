# -*- coding: utf-8 -*-
# @Time : 2022/3/28 15:40
# @Author : Hanhaha
from random import choice


def get_random_str(num):
    letter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    str = ''
    for i in range(num):  # 16字节,循环32次
        a = choice(letter)  # random.choice()可以从序列中获取一个随机元素；choice() 方法返回一个（列表，元组或字符串中的）随机项。
        str = str + a

    return str
