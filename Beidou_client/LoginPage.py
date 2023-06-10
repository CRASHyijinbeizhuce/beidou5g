# -*- codeing = utf-8 -*-
# @Time : 2022/3/21 16:47
# @Author : jszmwq
# @File : LoginPage.py
# @Software: PyCharm
# 尚未完成
# （1）忘记密码功能还没做
import json
import os
import sys
import threading
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from Beidou_client import ForgetPasswdPage
from Beidou_client import MainPage
from Beidou_client import RegisterPage
from ttkbootstrap.constants import *
from other import globalvar
from other.Thread_operation import thread_on
from other.recv import recv_msg
# from other.recv import stop_threads
from other.user import post_login,user_Token



class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (w, h))
        self.Errornum=0
        #self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        self.page = ttk.Labelframe(self.root,text="用户登录",bootstyle=PRIMARY)  # 创建Frame
        # 用户名
        self.username = ttk.StringVar()
        # 密码
        self.password = ttk.StringVar()
        self.user_name=ttk.StringVar()
        self.createPage()

    def createPage(self):
        # self.s=ttk.Style()
        # self.s.configure('my_style',font=25)
        self.page.pack(pady=90,ipadx=20)#side=LEFT,anchor='center',expand=YES,fill=NONE
        self.root.update()
        max_x = self.root.winfo_width()
        max_y = self.root.winfo_height()
        ttk.Label(self.page).grid(row=0,column=2, pady=35)

        ttk.Label(self.page,  text='用户名: ',font=('',20,)).grid(row=1, column=2,pady=15,stick='W',ipadx=10)
        #ttk.Entry(self.page, font=35, textvariable=self.username, width=35,bootstyle=PRIMARY).grid(row=1, column=2)
        ttk.Label(self.page,  text='密码: ',font=('',20,)).grid(row=2, column=2,stick='W',)
        self.mm=ttk.Entry(self.page, font=60, textvariable=self.password, show='*',width=35,bootstyle=PRIMARY)
        self.mm.grid(row=2, column=3,pady=20)
        ttk.Button(self.page, text='注册新用户' ,command=self.register,bootstyle="secondary-link").grid(row=5, column=3, stick='W',padx=20, pady=20,ipadx=10)
        ttk.Button(self.page, text='忘记密码', command=self.forgetPasswd,bootstyle="secondary-link").grid(row=5, column=3, stick='E',padx=20,pady=20,ipadx=10,)


        self.loginn =ttk.Combobox(self.page,font=60, textvariable=self.username,width=33,bootstyle=PRIMARY)
        #ttk.Button(self.page, width=20, text='token认证登录', command=self.tokenloginCheck,bootstyle=PRIMARY)
        self.loginn.grid(row=1, column=3)
        try :
            self.loginn["values"] = user_Token()
        except:
            pass
        # 绑定下拉菜单事件
        self.loginn.bind("<<ComboboxSelected>>", self.func)

        self.lo=ttk.Button(self.page, width=30, text='登录', command=self.loginCheck, bootstyle=PRIMARY,)
        self.lo.grid(row=3,column=3, padx=20,pady=15)
        ttk.Button(self.page, width=30,text='退出', command=self.exit,bootstyle=(PRIMARY, OUTLINE)).grid(row=4, column=3,padx=30,pady=15)

    # def login(self):
    #     self.root.update()
    #     ttk.Label(self.page, font=35, text='密码: ').grid(row=2, column=1,stick='W',)
    #     ttk.Entry(self.page, font=35, textvariable=self.password, show='*',width=35,bootstyle=PRIMARY).grid(row=2, column=2,pady=20)
    #     self.loginn['text'] = '登录'
    #     self.loginn['command'] = self.loginCheck

    def func(self,event):
        self.mm.delete("0", "end")
        self.mm.insert( 'insert','zxcvasdf')



    def loginCheck(self):
        #self.root.update()
        name = self.username.get()
        secret = self.password.get()
        # if not secret:
        #     secret=1
        print(name,secret)
        # @TODO 改成自己的接口HTTP
        result = post_login(name, secret)

        # if name == '' and secret == '':
        if result[0]:
            #Messagebox.show_info(title='successful', message='登录成功')
            '''
            把用户名存入json文件
            '''
            full_path = sys.path[0] + '/' + "main.json"
            with open(full_path, 'r') as file:
                js = json.load(file)
            js["username"] = name
            with open(full_path, 'w') as file:
                json.dump(js, file, indent=4, ensure_ascii=False)
            file.close()

            '''
            创建消息json文件
            '''
            full_path = sys.path[0] + '/' + name + "msg.json"
            filename = full_path
            if not os.path.exists(filename):
                with open(full_path, 'w') as file:
                    js = {}
                    js["sum"] = 0
                    json.dump(js, file, indent=4, ensure_ascii=False)
                file.close()

            '''
            北斗收消息
            '''
            thread_on()

            '''
            网络收消息
            '''

            self.page.destroy()
            MainPage.MainPage(self.root)
        else:
            Messagebox.show_error(title='警告', message=result[1])
            self.Errornum+=1
            if self.Errornum > 5:
                Messagebox.show_error(title='警告', message='连接次数过多，请稍后重试')
                time = 300
                self.ct_down1(time)
                self.Errornum = 0

    # def tokenloginCheck(self):
    #     name = self.username.get()
    #     secret = "1"
    #
    #     # @TODO 改成自己的接口HTTP
    #     result = post_login(name, secret)
    #
    #     # if name == '' and secret == '':
    #     if result[0]:
    #         Messagebox.show_info(title='successful', message='登录成功')
    #         '''
    #         把用户名存入json文件
    #         '''
    #         full_path = sys.path[0] + '/' + "main.json"
    #         with open(full_path, 'r') as file:
    #             js = json.load(file)
    #         js["username"] = name
    #         with open(full_path, 'w') as file:
    #             json.dump(js, file, indent=4, ensure_ascii=False)
    #         file.close()
    #
    #         '''
    #         创建消息json文件
    #         '''
    #         full_path = sys.path[0] + '/' + name + "msg.json"
    #         filename = full_path
    #         if not os.path.exists(filename):
    #             with open(full_path, 'w') as file:
    #                 js = {}
    #                 js["sum"] = 0
    #                 json.dump(js, file, indent=4, ensure_ascii=False)
    #             file.close()
    #
    #         '''
    #         北斗收消息
    #         '''
    #         thread_on()
    #
    #         '''
    #         网络收消息
    #         '''
    #
    #         self.page.destroy()
    #         MainPage.MainPage(self.root)
    #     else:
    #         Messagebox.show_error(title='警告', message=result[1])

    def register(self):
        self.page.destroy()
        RegisterPage.RegisterPage(self.root)

    def forgetPasswd(self):
        self.page.destroy()
        ForgetPasswdPage.ForgetPasswdPage(self.root)

    def getusername(self):
        return self.username

    def exit(self):
        quit()
        self.root.destory()
    def ct_down1(self, m):  # 倒计时函数
        m = m - 1  # 每次减少一个，减少几个随便
        self.id1 = self.root.after(1000, self.ct_down1, m)
        # 调用after方法自己呼叫自己，有点递归的意思有after方法的组件就可以调用计时器，我直接用self.master了，为什么赋值给id，
        if m != 0:  # 如果倒计时没有结束
            dead_minutes = m // 60 % 60
            dead_seconds = m % 60
            s='%d分%d秒后重试'%(dead_minutes,dead_seconds)

            self.lo['text'] = s  # 改变按钮文字
            self.lo['state'] = 'disabled'
        else:  # 倒计时结束

            self.root.after_cancel(self.id1)  # 在这里利用id取消回调
            self.lo['text'] = '登录'
            self.lo['state'] = 'normal'