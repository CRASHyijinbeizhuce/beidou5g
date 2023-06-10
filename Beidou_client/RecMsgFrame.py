# -*- codeing = utf-8 -*-
# @Time : 2022/3/22 19:03
# @Author : jszmwq
# @File : RecMsgFrame.py
# @Software: PyCharm
# 尚未实现


import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from other.recvmsg_net import get_netmsg
import tkinter.font as tkFont
import json
import sys
'''
持续接收北斗报文
添加按钮:从网络上获取报文(为了避免请求过快可以限制请求间隔大于5s(几秒都行))
网络获取:get_netmsg()
北斗获取:recv_msg()
'''


class RecMsgFrame(ttk.Frame):  # 继承Frame类
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.recMsgInfo = ttk.StringVar()
        self.recMsgInfo.set('尚未收到消息')
        self.msgbox = ttk.Label
        full_path = sys.path[0] + '/' + "main.json"
        with open(full_path, 'r') as file:
            js = json.load(file)
        self.name = js["username"]

        self.createPage()

    def createPage(self):
        self.root.update()
        max_x = self.root.winfo_width()
        max_y = self.root.winfo_height()
        ttk.Label(self, font=30).grid(row=0, stick='W', pady=max_y // 20)

        self.beirec = ttk.Labelframe(self,text="短报文收件箱", bootstyle=INFO, width=max_x // 3, height=20)
        self.beirec.grid(row=1, column=0,)
        # self.netrec = ttk.Labelframe(text="网络收件箱", bootstyle=INFO, width=max_x / 3, height=max_y / 3)
        # self.netrec.grid(row=1, column=1,)
        self.st = ScrolledText(self.beirec, padding=5, height=20, autohide=True,font=('',20,))
        self.st.pack(fill=BOTH, expand=YES)
        ttk.Button(self, width=30, text='从网络获取', command=self.refechnet, bootstyle=PRIMARY).grid(row=2, column=0, stick=E)
        self.refreshMsg()
        #self.refechnet()
        # self.msgbox = ttk.Label(self, textvariable=self.recMsgInfo, width=max_x // 15)
        # self.msgbox.configure(font=30)
        # self.msgbox.grid(row=1, column=0, columnspan=2, pady=max_y // 40)

    def refreshMsg(self):
        self.st.after(1000, self.refreshMsg)
        full_path_user = sys.path[0] + '/' + self.name + "msg.json"
        with open(full_path_user, 'r') as file:
            self.js1 = json.load(file)

        self.st.delete('1.0', END)
        list_name=list(self.js1.keys())
        for i in list_name[1:]:
            self.st.insert(END,'发件人 : '+str(i)+'\n')
            for j in self.js1.get(i).items():
                self.st.insert(END, str(j)+'\n')


    def refechnet(self):
        #self.st.after(5000, self.refechnet)
        get_netmsg()
