# -*- codeing = utf-8 -*-
# @Time : 2022/3/23 1:48
# @Author : jszmwq
# @File : ForgetPasswdPage.py
# @Software: PyCharm
# 尚未完成
# （1）功能尚未实现
# 未添加接口
#经过美化，添加倒计时无法再次获取验证码

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from Beidou_client import LoginPage
from other.user import post_phonenum_forget, post_register_forget
from ttkbootstrap.constants import *


class ForgetPasswdPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        #self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry('%dx%d' % (w, h))  # 设置窗口大小
        self.page = ttk.Frame(self.root)  # 创建Frame

        self.username = ttk.StringVar()
        self.password = ttk.StringVar()
        self.repasswd = ttk.StringVar()
        self.phoneNum = ttk.StringVar()
        self.verCode = ttk.StringVar()

        self.createPage()

    def createPage(self):
        self.page.pack()
        self.root.update()
        max_x = self.root.winfo_width()
        max_y = self.root.winfo_height()
        ttk.Label(self.page).grid(row=0, stick='W', pady=max_y/9)
        ttk.Label(self.page).grid(row=0, stick='W')  # 空出一行的位置，更美观
        ttk.Label(self.page, font=('',20,), text='用户名: ').grid(row=1, stick='W', pady=15)
        ttk.Label(self.page, font=('',20,), text='由2-8个数字和字母组成，首位不为数字', bootstyle='secondary').grid(row=1, column=3,stick='W')
        ttk.Entry(self.page, font=('',20,), textvariable=self.username,bootstyle=PRIMARY,width=35).grid(row=1, column=2, stick='E')
        ttk.Label(self.page, font=('',20,), text='密码: ').grid(row=2, stick='W', pady=15)
        ttk.Label(self.page, font=('',20,), text='不小于8位 ', bootstyle='secondary').grid(row=2, column=3, stick='W')
        ttk.Entry(self.page, font=('',20,), textvariable=self.password,show='*',bootstyle=PRIMARY,width=35).grid(row=2, column=2, stick='E')
        ttk.Label(self.page, font=('',20,), text='确认密码: ').grid(row=3, stick='W', pady=15)
        ttk.Entry(self.page, font=('',20,), textvariable=self.repasswd,show='*',bootstyle=PRIMARY,width=35).grid(row=3, column=2, stick='E')
        ttk.Label(self.page, font=('',20,), text='手机号:').grid(row=4, stick='W', pady=15)
        ttk.Entry(self.page, font=('',20,), textvariable=self.phoneNum,bootstyle=PRIMARY,width=35).grid(row=4, column=2, stick='E')
        self.count = ttk.Button(self.page, text='获取验证码', command=self.sendVerCode)
        self.count.grid(row=4, column=3, padx=10, stick='W')
        ttk.Label(self.page, font=('',20,), text='验证码:', ).grid(row=5, stick='W', pady=15)
        ttk.Entry(self.page, font=('',20,), textvariable=self.verCode,  bootstyle=PRIMARY,width=35).grid(row=5, column=2,
                                                                                                   stick='E')
        self.out = ttk.Label(self.page,font=('',20,), text='未获取验证码', bootstyle='warning')
        self.out.grid(row=5, column=3, stick='W')
        # ttk.Button(self.page, text='获取验证码', command=self.sendVerCode).grid(row=4, column=3, padx=10)
        # ttk.Label(self.page, font=30, text='验证码:').grid(row=5, stick='W', pady=15)
        # ttk.Entry(self.page, font=30, textvariable=self.verCode).grid(row=5, column=2, stick='E')
        ttk.Button(self.page, text='返回登录界面', command=self.returnBack,bootstyle="secondary-link").grid(row=6, pady=15,stick='W')
        ttk.Button(self.page,  text='注册', command=self.sendRegister).grid(row=6, column=2,  pady=15,stick='E')

    def ct_down(self, n):  # 60s倒计时函数
        n = n - 1  # 每次减少一个，减少几个随便
        id = self.root.after(1000, self.ct_down, n)
        # 调用after方法自己呼叫自己，有点递归的意思有after方法的组件就可以调用计时器，我直接用self.master了，为什么赋值给id，
        if n != 0:  # 如果倒计时没有结束
            self.count['state'] = 'disabled'
            s='已发送，请在%d秒后重试'%n
            #self.root.title(str(n))  # 改变标题
            self.count['text'] = s  # 改变按钮文字
        else:  # 倒计时结束
            self.count['state'] ='normal'
            self.root.after_cancel(id)  # 在这里利用id取消回调
            #self.root.title('倒计时完成')
            self.count['text'] = '获取验证码'

    def ct_down1(self, m):  # 倒计时函数
        m = m - 1  # 每次减少一个，减少几个随便
        self.id1 = self.root.after(1000, self.ct_down1, m)
        # 调用after方法自己呼叫自己，有点递归的意思有after方法的组件就可以调用计时器，我直接用self.master了，为什么赋值给id，
        if m != 0:  # 如果倒计时没有结束
            dead_minutes = m // 60 % 60
            dead_seconds = m % 60
            s='验证码有效期剩余%d分%d秒'%(dead_minutes,dead_seconds)

            self.out['text'] = s  # 改变按钮文字
        else:  # 倒计时结束

            self.root.after_cancel(self.id1)  # 在这里利用id取消回调
            self.out['text'] = '上一个验证码已过期，请重新获取'


    def sendVerCode(self):
        if not (self.phoneNum.get().isdigit() and len(self.phoneNum.get()) == 11):
            Messagebox.show_error(title='wrong', message='发送验证码失败，请输入正确的11位手机号')
        else:
            result = post_phonenum_forget(self.phoneNum.get())
            if not result[0]:
                Messagebox.show_error(title='wrong', message=result[1])
            else:
                #Messagebox.show_info(title='successful', message=result[1])
                time_count = 60
                time = 300
                try:
                    self.root.after_cancel(self.id1)
                    self.ct_down(time_count)

                    self.ct_down1(time)
                except:
                    self.ct_down(time_count)

                    self.ct_down1(time)

    def sendRegister(self):
        if (len(self.username.get()) < 3) or len(self.username.get()) > 8:
            Messagebox.show_error(title='wrong', message='注册失败，用户名格式错误，必须由2-8个数字和字母组成')
        elif self.username.get()[0] in str([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
            Messagebox.show_error(title='wrong', message='注册失败，用户名格式错误，首个字符不能为数字')
        elif len(self.password.get()) != 8:
            Messagebox.show_error(title='wrong', message='注册失败，密码应为8位')
        elif self.password.get() != self.repasswd.get():
            Messagebox.show_error(title='wrong', message='注册失败，两次密码不相同')
        elif not (self.phoneNum.get().isdigit() and len(self.phoneNum.get()) == 11):
            Messagebox.show_error(title='wrong', message='发送失败，请输入正确的11位手机号')
        # elif self.verCode.get() != # 填入的验证码不等于服务器传回的验证码
        else:
            result = post_register_forget(self.password.get(), self.phoneNum.get(), self.verCode.get())
            if result[0]:
                Messagebox.show_info(title='successful', message='修改密码成功')
                self.page.destroy()
                LoginPage.LoginPage(self.root)
            else:
                Messagebox.show_error(title='wrong', message=result[1])
            # url = "http://172.17.1.43:8080/user/register"
            # # user="username="+names.get()+"password="+self.passwords.get()+"phone number="+self.phoneNum.get()
            # data = dict()  # Post请求发送的数据，字典格式
            # data['username'] = self.usernames.get()
            # data['password'] = self.passwords.get()
            # data['phonenumber'] = self.phoneNum.get()
            # res = requests.post(url=url, data=data)  # 这里使用post方法，参数和get方法一样
            # if res.text == "1":
            #
            # if 1:
            #     tk.messagebox.showinfo(title='successful', message='注册成功！欢迎您。新会员')
            #     self.page.destroy()
            #     LoginPage.LoginPage(self.root)
            # else:
            #     tk.messagebox.showerror(title='wrong', message='注册失败,server')

    def returnBack(self):
        self.page.destroy()
        LoginPage.LoginPage(self.root)
