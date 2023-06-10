# -*- coding: utf-8 -*-
# @Time : 2022/4/4 15:21
# @Author : Hanhaha


import requests
import os
import subprocess


# def gaode(addr):
#     para = {
#         'key': 'f24778015c673c5847bdead4ac852365',  # 高德地图开放平台申请的key
#         'address': addr,  # 传入地址参数
#     }
#     url = 'https://restapi.amap.com/v3/geocode/geo?'  # 高德地图API接口
#     req = requests.get(url, para)
#     req = req.json()
#     print('-' * 30)
#     m = req['geocodes'][0]['location']
#     location = m.split(',')
#     location[0] = location[0] + 'E'
#     location[1] = location[1] + 'N'
#     # print(location)
#     return location
#
#
# position = gaode(addr="西安电子科技大学南校区")
# print(position)


def ip_position():
    fnull = open(os.devnull, 'w')
    return1 = subprocess.run('curl -s -L ip.tool.lu', shell=True, stdout=subprocess.PIPE)
    if return1.returncode:
        return [False, '获取IP地址定位失败']
    else:
        answer = return1.stdout.decode('utf-8')
        print()
        return [True, answer.split('\n')[1]]
