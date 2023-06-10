# -*- codeing = utf-8 -*-
# @Time : 2022/4/12 0:50
# @Author : jszmwq
# @File : get_port_list.py
# @Software: PyCharm

import serial.tools.list_ports
# 获取可用串口列表
# 暂且将次作为北斗设备连接正常的函数
# 如果存在其他串口，可能会存在问题


def get_port_list():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        print('无可用串口')
        return '无可用串口'
    else:
        return port_list
