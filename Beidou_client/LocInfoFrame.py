# -*- codeing = utf-8 -*-
# @Time : 2022/3/22 19:04
# @Author : jszmwq
# @File : LocInfoFrame.py
# @Software: PyCharm
# 尚未完成
# （1）与树莓派对接还没实现，获取信号状态，获取定位， 获取时间
#由于时间显示问题，不判断直接显示，但不知道get_net_time、get_net_position有没有在其他函数调用

import threading
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
import time
from other import net_state
from other import position_time
from other import get_net_time
from other import get_net_position
from other import globalvar


class LocInfoFrame(ttk.Frame):  # 继承Frame类
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.locationInfo = ttk.StringVar()
        self.timeInfo = ttk.StringVar()
        self.stateInfo = ttk.StringVar()
        self.loc_button = ttk.Button()
        self.vardict = globalvar.globalvar()
        self.vardict.set_value('tim', 60)
        self.beidou_result = ''
        self.net_result = ''
        self.state_result = ''
        self.time1 = 0
        self.time2 = 0
        self.time3 = 0
        self.time4 = 0
        self.time5 = 0
        self.locationInfo.set('位置信息未知，请点击刷新位置按钮获取位置')
        self.timeInfo.set(str(self.getTime()))
        # if self.timeInfo.get() != '时间获取失败':
        #     self.judge_time()
        self.createPage()

    def set_time(self):
        self.root.after(200, self.set_time)
        # time.sleep感觉设置为1000不太好，就取一个200ms吧,可能会占用很大的内存
        self.time4 = time.time()
        # 转换成localtime
        time_local = time.localtime(self.time4 + self.time3)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        self.time5 = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        self.timeInfo.set(self.time5)
        self.root.update()

    def judge_time(self):
        dt = self.timeInfo.get()
        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        # 网络时间转换成时间戳
        self.time1 = int(time.mktime(timeArray))
        # 系统时间转换成时间戳
        self.time2 = int(time.time())
        # time3为系统时间与网络时间的差
        self.time3 = self.time1 - self.time2
        print(self.time3)
        self.set_time()

    def get_net_State(self):
        if net_state.net_state():
            return '5G网络状态良好'
        else:
            return '当前5G信号差，无法使用'

    def get_beidou_State(self):
        if net_state.beidou_state():
            return '北斗网络状态良好'
        else:
            return '当前北斗信号差，无法使用'

    def getLocation(self):
        location = position_time.get_position()
        return location

    def getTime(self):
        self.net_result = self.get_net_State()
        self.beidou_result = self.get_beidou_State()
        self.state_result = self.net_result + '\n' + self.beidou_result
        self.stateInfo.set(self.state_result)
        if self.net_result == '5G网络状态良好':
            dt = get_net_time.getBeijinTime()
        elif self.beidou_result == '北斗网络状态良好':
            dt = position_time.get_time()
        else:
            dt = '时间获取失败'
        return dt

    def refreshoth(self):

        self.up2=ttk.Floodgauge(self,bootstyle="success",font=("微软雅黑",10), #文本字体length=100,  #水尺长度
    maximum=10, #增加到10
    length=300,
    mode=INDETERMINATE, #来回不确定
    orient=HORIZONTAL, #放置垂直方向
    text="其他信息加载中，请稍后", #文本
                                )
        self.up2.grid(row=6, column=1, stick='W',ipady=5)
        self.up2.start()
        self.thread_on2()
        self.thread_12.join(1)

    def thread_on2(self):
        self.thread_12 = threading.Thread(target=self.refresh_other)
        #thread_11.setDaemon()
        self.thread_12.start()

    def refresh_other(self):
        self.timeInfo.set(str(self.getTime()))
        time1 = 60
        self.ct_down1(time1)
        if self.timeInfo.get() != '时间获取失败':
            self.judge_time()
        self.up2.grid_forget()

    # 倒计时函数
    # def foo(self):
    #     clock = self.loc_button.after(1000, self.foo)  # 延迟调用foo，每1000毫秒一次
    #     self.vardict.set_value('tim', self.vardict.get_value('tim') - 1)  # 倒计时
    #     if self.vardict.get_value('tim') == 0 or self.locationInfo.get() == "信号不佳，定位失败":  # 如果倒计时为零时
    #         self.loc_button.config(text="刷新定位信息")  # 按钮文字显示再次发送
    #         self.vardict.set_value('tim', 60)  # 全局变量复原
    #         self.loc_button.after_cancel(clock)  # 取消after时钟函数
    #         self.loc_button.config(state="normal")  # 让按钮可用
    #         self.root.update()
    #     else:
    #         self.loc_button.config(state="disabled")  # 让按钮在倒计时期间不可用
    #         self.loc_button.config(text="请在%s秒后重新定位" % self.vardict.get_value('tim'))
    #         self.root.update()

    def ct_down(self, n):  # 60s倒计时函数
        n = n - 1  # 每次减少一个，减少几个随便
        id = self.root.after(1000, self.ct_down, n)
        # 调用after方法自己呼叫自己，有点递归的意思有after方法的组件就可以调用计时器，我直接用self.master了，为什么赋值给id，
        if n != 0:  # 如果倒计时没有结束
            self.loc_button['state'] = 'disabled'
            s='已刷新，请在%d秒后重试'%n
            #self.root.title(str(n))  # 改变标题
            self.loc_button['text'] = s  # 改变按钮文字
            self.loc_button['bootstyle']='warning'

        else:  # 倒计时结束
            self.loc_button['state'] ='normal'
            self.root.after_cancel(id)  # 在这里利用id取消回调
            #self.root.title('倒计时完成')
            self.loc_button['text'] = '刷新定位信息'
            self.loc_button['bootstyle'] = 'PRIMARY'

    def ct_down1(self, n):  # 60s倒计时函数
        n = n - 1  # 每次减少一个，减少几个随便
        id1 = self.root.after(1000, self.ct_down1, n)
        # 调用after方法自己呼叫自己，有点递归的意思有after方法的组件就可以调用计时器，我直接用self.master了，为什么赋值给id，
        if n != 0:  # 如果倒计时没有结束
            self.oth_button['state'] = 'disabled'
            s='已刷新，请在%d秒后重试'%n
            #self.root.title(str(n))  # 改变标题
            self.oth_button['text'] = s  # 改变按钮文字
            self.oth_button['bootstyle']='warning'

        else:  # 倒计时结束
            self.oth_button['state'] ='normal'
            self.root.after_cancel(id1)  # 在这里利用id取消回调
            #self.root.title('倒计时完成')
            self.oth_button['text'] = '刷新其他信息'
            self.oth_button['bootstyle'] = 'PRIMARY'

    def refreshloc(self):

        self.up1=ttk.Floodgauge(self,bootstyle="success",font=("微软雅黑",10), #文本字体length=100,  #水尺长度
    maximum=10, #增加到10
    length=300,
    mode=INDETERMINATE, #来回不确定
    orient=HORIZONTAL, #放置水平方向
    text="地理位置加载中，请稍后", #文本
                                )
        self.up1.grid(row=5, column=1, stick='W')
        self.up1.start()
        self.thread_on1()
        self.thread_11.join(2)

    def thread_on1(self):
        self.thread_11 = threading.Thread(target=self.refresh_loc)
        #thread_11.setDaemon()
        self.thread_11.start()

    def refresh_loc(self):
        time = 60
        self.ct_down(time)

        self.net_result = self.get_net_State()
        self.beidou_result = self.get_beidou_State()
        self.state_result = self.net_result + '   ' + self.beidou_result
        self.stateInfo.set(self.state_result)

        if self.beidou_result == '北斗网络状态良好':
            self.locationInfo.set(str(self.getLocation()))
            #self.loc_button.after(1000, self.foo)
        elif self.net_result == '5G网络状态良好':
            self.locationInfo.set(get_net_position.ip_position()[1])
        else:
            self.locationInfo.set('当前无信号，无法获取位置信息')
            Messagebox.show_error('警告', message='当前无信号，无法获取位置信息')
        self.up1.grid_forget()



    def createPage(self):
        self.root.update()
        max_x = self.root.winfo_width()
        max_y = self.root.winfo_height()
        ttk.Label(self).grid(row=0, stick='W', pady=max_y / 20)
        #ttk.Label(self, font=40, width=50, text='定位信息').grid(row=1, stick='N', pady=max_y // 20)

        self.loc_button = ttk.Button(self, text='刷新定位信息', command=self.refreshloc)
        self.loc_button.grid(row=1, column=1, stick='W')
        # self.locup = ttk.Label(self, font=30, text='未获取验证码', bootstyle='warning')
        # self.locup.grid(row=1, column=2, stick='W')

        self.oth_button=ttk.Button(self, text='刷新其他信息', command=self.refreshoth)
        self.oth_button.grid(row=1, column=3, stick='E')
        # self.othup = ttk.Label(self, font=30, text='未获取验证码', bootstyle='warning')
        # self.othup.grid(row=1, column=4, stick='W')

        ttk.Label(self, font=('',15,), width=50, text='当前信号状态 :').grid(row=2, stick='W', pady=max_y // 20)
        ttk.Label(self, font=('',15,), width=50, textvariable=self.stateInfo).grid(row=2, stick='E', column=1,
                                                                             pady=max_y // 20)
        ttk.Label(self, font=('',15,), width=50, text='当前位置经纬度为 :').grid(row=3, stick='W', pady=max_y / 20)
        ttk.Label(self, font=('',15,), width=50, textvariable=self.locationInfo).grid(row=3, stick='E', column=1,
                                                                                pady=max_y // 20)
        ttk.Label(self, font=('',15,), width=50, text='当前时间为 :').grid(row=4, stick='W', pady=max_y / 20)
        ttk.Label(self, font=('',15,), width=50, textvariable=self.timeInfo).grid(row=4, stick='E', column=1,
                                                                            pady=max_y // 20)

