# coding=gbk

import ttkbootstrap as ttk

from ttkbootstrap.dialogs import Messagebox

from ttkbootstrap.constants import *
from other.device import devi
from other import get_port_list
from other import seri
from Beidou_client import LoginPage
from other.user import user_Token


class StartPage(object):
    def __init__(self, master=None,**kwargs):
        self.root = master  # 定义内部变量root
        self.Errornum = 0
        self.root.title("星讯安客户端")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (w, h))
        self.root.f = ttk.Frame(bootstyle=SUCCESS)
        self.root.f.pack(side=TOP, padx=10)
        #label = ttk.Label(self.root.f, text="北斗客户端", font=("华文行楷", 40))
        #label.pack(fill=BOTH, expand=YES,side=TOP)
        self.get_port = ttk.StringVar()
        # self.root.geometry('%dx%d' % (600, 400))  # 设置窗口大小


        self.page = ttk.Frame(self.root)  # 创建Frame


        #self.get_port = ttk.StringVar()
        self.createPage()

        portx = str(get_port_list.get_port_list()[0])
        serObject = seri.open_ser(portx)
        j1 = 0
        j2 = 0
        # 检查北斗组件是否正常工作
        judge1 = True
        while judge1:
            if portx:#'Prolific USB-to-Serial Comm Port' in portx:
                j1 = 1
                judge1 = False
            else:
                Messagebox.show_error(title='警告', message='请检查北斗组件是否连接正确')
                judge1 = False

        # 检查设备是否注册
        judge2 = True
        while judge2:
            # try:
            device_state = devi()
            # print("device_state=", device_state)
            if not device_state[0]:
                Messagebox.show_error(title='警告', message='%s' % device_state[1])
                judge2 = False
            else:
                j2=1
                judge2 = False
        print(j1,j2)
        if j1 == 1 and j2 == 1:
            self.page.destroy()
            LoginPage.LoginPage(self.root)
        else:
            self.Errornum+=1



    def createPage(self):
        self.page.pack(side=LEFT,anchor='center',expand=YES,fill=NONE)
        # s = ttk.Style()
        # s.configure('my_style', font=('宋体',25))
        max_x = self.root.winfo_width()/3
        max_y = self.root.winfo_height()/3
        self.root.update()
        #tk.Label(self.page).grid(row=0, stick='W', pady=max_y / 8)
        ttk.Label(self.page,  text='当前北斗器件使用的串口是:',font=('',20,)).grid(row=1, column=0, stick='W', pady=15, padx=30)
        # port_box = ttk.Combobox(self.page, textvariable=self.get_port)  # 初始化
        ttk.Label(self.page,  text=get_port_list.get_port_list()[0],font=('',20,)).grid(row=1, column=1, stick='W', pady=15,
                                                                               padx=30)
        # port_box["values"] = get_port_list.get_port_list()
        # port_box.grid(row=1, column=1, columnspan=5, pady=15)
        self.a=ttk.Button(self.page, width=45,text='重试',  bootstyle=(PRIMARY, OUTLINE), command=self.run,)
        self.a.grid(row=2, column=0,pady=15)
        #self.a.config(font=("宋体", 20))
        ttk.Button(self.page, width=45, text='退出', bootstyle=(PRIMARY, OUTLINE), command=self.exit,).grid(row=2,
                                                                                                         column=1,
                                                                                                         pady=15)

    def run(self):
        if self.Errornum>5:
            Messagebox.show_error(title='警告', message='连接次数过多，请稍后重试')
            time = 300
            self.ct_down1(time)
            self.Errornum=0
        portx =str(get_port_list.get_port_list()[0])
        print(portx)
        serObject = seri.open_ser(portx)
        j1=0
        j2=0
        # 检查北斗组件是否正常工作
        judge1 = True
        while judge1:
            if portx:#'Prolific USB-to-Serial Comm Port' in portx:
                j1=1
                judge1 = False
            else:
                Messagebox.show_error(title='警告', message='请检查北斗组件是否连接正确')
                judge1 = False

        # 检查设备是否注册
        judge2 = True
        while judge2:
            # try:
            device_state = devi()
            # print("device_state=", device_state)
            if not device_state[0]:
                Messagebox.show_error(title='警告', message='%s' % device_state[1])
                judge2 = False
            else:
                j2=1
                judge2 = False
        #print(j1,j2)
        if j1==1 and j2==1:
            self.page.destroy()
            LoginPage.LoginPage(self.root)
        else:
            self.Errornum += 1

    def exit(self):
        quit()
        self.root.destroy()

    def ct_down1(self, m):  # 倒计时函数
        m = m - 1  # 每次减少一个，减少几个随便
        self.id1 = self.root.after(1000, self.ct_down1, m)
        # 调用after方法自己呼叫自己，有点递归的意思有after方法的组件就可以调用计时器，我直接用self.master了，为什么赋值给id，
        if m != 0:  # 如果倒计时没有结束
            dead_minutes = m // 60 % 60
            dead_seconds = m % 60
            s='%d分%d秒后重试'%(dead_minutes,dead_seconds)

            self.a['text'] = s  # 改变按钮文字
            self.a['state'] = 'disabled'
        else:  # 倒计时结束

            self.root.after_cancel(self.id1)  # 在这里利用id取消回调
            self.a['text'] = '重试'
            self.a['state'] = 'normal'