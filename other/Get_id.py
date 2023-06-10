# -*- coding: utf-8 -*-
# @Time : 2022/3/26 13:59
# @Author : Hanhaha

# @QUESTION 这个序列号是设备的序列号吗
import time
from other import seri


def get_cardid():
    serObject = seri.open_ser()
    result = serObject.ser.write("$CCICA,0,00*7B\r\n".encode("gbk"))
    # result = ser.write("$CCICA,0,00*7B\r\n".encode("gbk"))
    print("写总字节数:", result)

    time.sleep(1)
    if serObject.ser.in_waiting:
        str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
        # print(str1)
        # print("卡号为：", str1[7:14])
        # print("设备序列号为：", str1[15:23])
        # print("---------------")
        print("获取卡号成功")
        return str1[7:14], str1[15:23]


if __name__ == '__main__':
    serObject = seri.open_ser('COM3')
    print(get_cardid())