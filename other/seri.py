# -*- coding: utf-8 -*-
# @Time : 2022/3/26 12:39
# @Author : Hanhaha

# 打开串口
import serial
import serial.tools.list_ports


class open_ser:
    _instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *portx):
        if open_ser.init_flag:
            return
        try:
            # 这个位置信息为固定值，实际情况会有变动，需要调整
            # 注意！！！从COM3变更为/dev/ttyUSB0, 具体情况需要
            # 获取端口号 python -m serial.tools.list_ports
            result = str(portx[0])
            result = result.split(' ')[0]
            self.portx = result
            print(self.portx)
            # self.portx = "/dev/ttyUSB0"
            self.bps = 115200
            self.timex = 5
            self.ser = serial.Serial(self.portx, self.bps, timeout=self.timex)
            self.ser.write("$CCICA,0,00*7B\r\n".encode("gbk"))
            # 如果存在串口， 那么创建这个单例成功，反之则需要重新创建
            open_ser.init_flag = True
        except Exception as e:
            print("---异常---：", e)
            '''
            异常时弹出错误提示框：串口连接失败
            '''
            return
        print("打开串口成功")

    # ser=open_ser()

    # 把get_port单独作为一个文件

