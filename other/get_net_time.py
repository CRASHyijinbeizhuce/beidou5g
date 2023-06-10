# -*- codeing = utf-8 -*-
# @Time : 2022/4/3 17:22
# @Author : jszmwq
# @File : get_net_time.py
# @Software: PyCharm

import requests
import time

def getBeijinTime():
    # HTTP客户端运行的浏览器类型的详细信息。通过该头部信息，web服务器可以判断到当前HTTP请求的客户端浏览器类别。
    hea = {'User-Agent': 'Mozilla/5.0'} #站点服务器认为自己（浏览器）兼容Moailla的一些标准
    # 设置访问地址，我们分析到的；
    url = r'http://time1909.beijing-time.org/time.asp'
    # 用requests get这个地址，带头信息的；
    r = requests.get(url=url, headers=hea)
    # 检查返回的通讯代码，200是正确返回；
    if r.status_code == 200:
        # 定义result变量存放返回的信息源码；
        result = r.text
        # 通过;分割文本；
        data = result.split(";")
        # 以下是数据文本处理：切割、取长度
        year = data[1][len("nyear") + 3: len(data[1])]
        month = data[2][len("nmonth") + 3: len(data[2])]
        day = data[3][len("nday") + 3: len(data[3])]
        # wday = data[4][len("nwday")+1 : len(data[4])-1]
        hrs = data[5][len("nhrs") + 3: len(data[5])]
        # hrs = data[5][len("nhrs") + 3: len(data[5]) - 1] #不需要减1
        minute = data[6][len("nmin") + 3: len(data[6])]
        sec = data[7][len("nsec") + 3: len(data[7])]
        # 这个也简单把切割好的变量拼到beijinTimeStr变量里；
        beijinTimeStr = "%s-%s-%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
        ltime = time.strptime(beijinTimeStr, "%Y-%m-%d %H:%M:%S") # 返回结果是一个结构体
        dat = "%u-%02u-%02u" % (ltime.tm_year, ltime.tm_mon, ltime.tm_mday)
        tm = "%02u:%02u:%02u" % (ltime.tm_hour, ltime.tm_min, ltime.tm_sec)
        currenttime = dat + " " + tm
        return currenttime
