# -*- coding: utf-8 -*-
# @Time : 2022/3/26 15:24
# @Author : Hanhaha
import time
import other.seri


# 定位申请
from other.Thread_operation import thread_closed, thread_on


def get_position():
    '''
    中断北斗收线程
    '''
    thread_closed()

    print("北斗获取定位")
    serObject = other.seri.open_ser()
    num = 0
    while 1:


        result = serObject.ser.write("$CCDWA,0000000,V,1,L,,0,,,0*65\r\n".encode("gbk"))
        print("写总字节数:", result)
        time.sleep(3)
        if serObject.ser.in_waiting:
            str = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")


            opt = str.split()
            print(opt)
            if opt[0][11] == 'N':
                if opt[0][19:21] == "00":
                    print("信号不佳，定位失败")
                    num += 1
                else:
                    result_error = '请在%s秒后尝试重新发送' % opt[0][19:21]
                    return result_error

            if num == 3:
                return "信号不佳，定位失败"

            if opt[0][11] == "Y":
                result = ''
                for i in range(len(opt)):
                    if opt[i][0:6] == "$BDDWR":
                        result = opt[i]
                        break

                if result == '':
                    continue

                print("定位信息：", result)
                # 对收到的信息进行拆解
                position = result.split(',')
                p_str = ""
                # position="$BDDWR,1,0242286,021549.65,2240.4051,N,11402.5601,E,47,M,-3,M,1,V,V,L*1F\r\n".split(',')
                if position[5] == "N":
                    print("北纬：%s" % str(round(float(position[4]) / 100, 6)))
                    p_str = p_str + str(round(float(position[4]) / 100, 6)) + "N;"
                else:
                    print("南纬：%s" % str(round(float(position[4]) / 100, 6)))
                    p_str = p_str + str(round(float(position[4]) / 100, 6)) + "S;"
                if position[7] == "E":
                    print("东经：%s" % str(round(float(position[6]) / 100, 6)))
                    p_str = p_str + str(round(float(position[6]) / 100, 6)) + "E;"
                else:
                    print("西经：%s" % str(round(float(position[6]) / 100, 6)))
                    p_str = p_str + str(round(float(position[6]) / 100, 6)) + "W;"
                print("大地高度：{}m".format(position[8]))
                p_str = p_str + position[8] + "m;"
                print("---------------")

                '''
                北斗继续接收报文
                '''
                thread_on()

                return p_str


# 获取时间
def get_time():
    '''
    中断北斗收线程
    '''
    thread_closed()

    print("北斗获取时间")
    serObject = other.seri.open_ser()
    serObject.ser.flushInput()

    result = serObject.ser.write("$CCRMO,ZDA,2,0*21\r\n".encode("gbk"))
    print("写总字节数:", result)

    time.sleep(1)
    if serObject.ser.in_waiting:
        str1 = serObject.ser.read(serObject.ser.in_waiting).decode("gbk")
        # print(str)



        timing = str1.split(',')
        # print(timing)
        # 时分秒
        str2 = "{}:{}:{}:{}".format(int(timing[2][0:2]) - int(timing[6]), timing[2][2:4], timing[2][4:6], timing[2][7:])
        print(str2)
        # 日期
        str3 = "{}年{}月{}日\n".format(timing[5], timing[4], timing[3])
        print(str3)
        print("---------------")

        '''
        北斗继续接收报文
        '''
        thread_on()

        return str3 + "\n" + str2
    else:
        return '时间获取失败'
