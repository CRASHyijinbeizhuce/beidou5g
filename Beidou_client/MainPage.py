# -*- codeing = utf-8 -*-
# @Time : 2022/3/21 17:27
# @Author : jszmwq
# @File : MainPage.py
# @Software: PyCharm

import ttkbootstrap as ttk
from Beidou_client import LocInfoFrame
from Beidou_client import PersonInfoFrame
from Beidou_client import RecMsgFrame
from Beidou_client import SendMsgFrame
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
from other.Thread_operation import thread_closed

PATH = Path(__file__).parent / 'assets'


class MainPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (w, h))
        # self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小

        image_files = {
            'mainp' : 'main.png',
            #'recMsg': 'inbox.png',
            # 'refresh':'refresh.png',
            #
            'fap':'fa.png',
            'shoup':'shou.png',
            'locationp':'location.png',
            'returnp':'return.png',
        }
        self.photoimages = []
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))


        # 功能面板按钮
        # self.buttonbar = ttk.Frame(self.root, style='primary.TFrame')
        self.root.f = ttk.Frame(self.root, bootstyle=PRIMARY)
        # self.root.f.place(x=10, y=10, width=w, height=h/7)
        # self.root.f.pack(side=TOP, padx=10)
        # label = ttk.Label(self.root.f, text="北斗客户端", font=("华文行楷", 30))
        # label.pack(side=LEFT, padx=10)
        # label.pack(side=LEFT, padx=10)

        self.buttonbar = ttk.Frame(self.root, width=w / 5, height=h)
        # self.buttonbar.pack(side=LEFT, padx=10)
        self.buttonbar.pack(side=LEFT, padx=10, )

        # 个人信息页面
        self.PersonInfoPage = PersonInfoFrame.PersonInfoFrame(self.root)
        # 发送短报文页面
        self.sendMsgPage = SendMsgFrame.SendMsgFrame(self.root)
        # 短报文收件箱页面
        self.recMsgPage = RecMsgFrame.RecMsgFrame(self.root)
        # 定位信息页面
        self.locIndoPage = LocInfoFrame.LocInfoFrame(self.root)
        # 创建不同Frame
        self.createPage()

    def createPage(self):
        # 个人信息页面
        btn = ttk.Button(
            master=self.buttonbar,
            image='mainp',
            text='个人信息',

            compound=TOP,
            command=self.personInfoData,
            #bootstyle=INFO
        )
        btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10,pady=10)
        # 发送短报文问页面
        btn = ttk.Button(
            master=self.buttonbar,
            text='发送短报文',

            image='fap',
            compound=TOP,
            command=self.sendMsgData,
            #bootstyle=INFO
        )
        btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10,pady=10)
        # 短报文收件箱
        btn = ttk.Button(
            master=self.buttonbar,
            text='短报文收件箱',

            image='shoup',
            compound=TOP,
            command=self.recMsgData,
            #bootstyle=INFO
        )
        btn.pack(side=TOP, ipadx=10, ipady=10,pady=10 )
        # 定位信息页面
        btn = ttk.Button(
            master=self.buttonbar,
            text='定位信息',

            image='locationp',
            compound=TOP,
            command=self.locInfoData,
            #bootstyle=INFO
        )
        btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10,pady=10)
        # 退出
        btn = ttk.Button(
            master=self.buttonbar,

            text='退出',
            image='returnp',

            compound=TOP,
            command=self.exit,
            #bootstyle=INFO
        )
        btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10,pady=10)

        self.PersonInfoPage.pack()  # 默认显示个人信息界面

    def personInfoData(self):
        self.PersonInfoPage.pack()
        self.sendMsgPage.pack_forget()
        self.recMsgPage.pack_forget()
        self.locIndoPage.pack_forget()

    def sendMsgData(self):
        self.PersonInfoPage.pack_forget()
        self.sendMsgPage.pack()
        self.recMsgPage.pack_forget()
        self.locIndoPage.pack_forget()

    def recMsgData(self):
        self.PersonInfoPage.pack_forget()
        self.sendMsgPage.pack_forget()
        self.recMsgPage.pack()
        self.locIndoPage.pack_forget()

    def locInfoData(self):
        self.PersonInfoPage.pack_forget()
        self.sendMsgPage.pack_forget()
        self.recMsgPage.pack_forget()
        self.locIndoPage.pack()

    def exit(self):
        thread_closed()#在关闭时先结束线程
        quit()
        self.root.destroy()
