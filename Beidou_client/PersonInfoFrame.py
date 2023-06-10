# -*- codeing = utf-8 -*-
# @Time : 2022/3/23 1:55
# @Author : jszmwq
# @File : PersonInfoFrame.py
# @Software: PyCharm
# 尚未解决
# （1）想要实现在个人资料页显示用户名username，但由于LoginPage中为局部变量，无法传入PersonInfoFrame中
#退出无法执行
import json
import tkinter as tk
import json

import ttkbootstrap as ttk
from other import Get_id
import sys
from ttkbootstrap.constants import *


class PersonInfoFrame(ttk.Frame):  # 继承Frame类
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.beidouNumber = ttk.StringVar()
        self.beidouNumber.set(str(self.getBeidouNumber()))
        self.createPage()

    def createPage(self):
        self.root.update()
        max_x = self.root.winfo_width()
        max_y = self.root.winfo_height()
        full_path = sys.path[0] + '/' + "main.json"
        with open(full_path, 'r') as file:
            js = json.load(file)
        name = js["username"]
        ttk.Label(self, font=50, width=30, text='').grid(row=1, stick='W', pady=max_y / 20)
        ttk.Label(self,font=('',20,), width=20, text=name+' : 欢迎您的使用',bootstyle=INFO).grid(row=1, stick='W', pady=max_y / 20)
        ttk.Label(self).grid(row=0, stick='W', pady=max_y / 20)
        ttk.Label(self, font=('',20,), width=20, text='北斗卡号',bootstyle=INFO).grid(row=2, stick='W', pady=max_y / 20)
        ttk.Label(self, font=('',20,), width=30, textvariable=self.beidouNumber).grid(row=2, stick='W', column=1, pady=max_y / 20)
        #ttk.Button(self, text='退出', command=self.exitt).grid(row=3, column=1, stick='W')#退不出去

    def getBeidouNumber(self):
        try:
            full_path = sys.path[0] + '/' + "main.json"
            with open(full_path, 'r') as file:
                js = json.load(file)
                tag = js["tag"]
            file.close()
            cardid = tag.split('/')[1]
            return cardid
        except:
            return '获取失败'
        # result = Get_id.get_cardid()[0]
        # if result:
        #     return result
        # else:
        #     return '获取失败'

    def exitt(self):
        self.destory()