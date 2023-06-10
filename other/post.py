# -*- coding: utf-8 -*-
# @Time : 2022/3/26 11:55
# @Author : Hanhaha

import requests
# IP = "192.168.43.24:8080"
IP = '192.168.1.104:8080'
# IP = '172.17.1.11:8080'
# IP = '172.17.17.2:26041'
#IP='10.198.102.69:8080'
#IP = '192.168.43.24:8080'
#IP='lib.gorio.top:26041'


def post_1(r_post, data):
    url = "http://" + IP + r_post
    # Post请求发送的数据，字典格式
    res = requests.post(url=url, data=data)  # 这里使用post方法，参数和get方法一样
    # print(res.text)
    return res
