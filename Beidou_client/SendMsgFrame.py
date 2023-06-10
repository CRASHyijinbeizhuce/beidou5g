# -*- codeing = utf-8 -*-
# @Time : 2022/3/22 18:48
# @Author : jszmwq
# @File : SendMsgFrame.py
# @Software: PyCharm
# 尚未实现
# （1）待添加发送加密函数、编码等函数
"""
1、需要添加计时器，发送成功后，倒计时60s，倒计时结束前不可进行操作
2、发送计时器与定位计时器同步
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from other.net_state import net_state
from other.send import send_msg_beidou
from other.sendmsg_net import send_net_msg
from other import globalvar


class SendMsgFrame(ttk.Frame):  # 继承Frame类
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.recvname = ttk.StringVar()
        self.message = ttk.StringVar()
        self.send_button = ttk.Button()
        self.vardict = globalvar.globalvar()
        self.vardict.set_value('tim', 60)
        self.msgbox = ttk.Text
        self.createPage()
        self.name= ttk.StringVar()
        self.msg= ttk.StringVar()

    def foo(self):
        clock = self.send_button.after(1000, self.foo)  # 延迟调用foo，每1000毫秒一次
        self.vardict.set_value('tim', self.vardict.get_value('tim') - 1)  # 倒计时
        if self.vardict.get_value('tim') == 0:  # 如果倒计时为零时
            self.send_button.config(text="发送")  # 按钮文字显示再次发送
            self.vardict.set_value('tim', 60)  # 全局变量复原
            self.send_button.after_cancel(clock)  # 取消after时钟函数
            self.send_button.config(state="normal")  # 让按钮可用
            self.root.update()
        else:
            self.send_button.config(state="disabled")  # 让按钮在倒计时期间不可用
            self.send_button.config(text="请在%s秒后发送" % self.vardict.get_value('tim'))
            self.root.update()

    def sendMsg(self):


        # 获取text中的文本信息
        print(self.msgbox.get('1.0', 'end'))
        # state = send.send_msg_beidou("0301", self.msgbox.get('1.0', 'end'), 1, str(self.recvname.get()) )
        if net_state():
            state = send_net_msg(str(self.recvname.get()), self.msgbox.get('1.0', 'end')+' ')
        else:
            # 北斗发送不保证有返回值，这里代码的含义：只要通过北斗模块发出，无论服务器是否收到都返回True
            state = send_msg_beidou("03", self.msgbox.get('1.0', 'end'), 1, str(self.recvname.get()))

        if not state[0]:
            print(state[1])
            Messagebox.show_error(title='警告', message=state[1])
        else:
            # Messagebox.show_info('成功', message='发送成功')
            self.send_button.after(1000, self.foo)

        name_content = "发件人:" + self.recvname.get() + "\n"
        ming_content = "明  文:" + self.msgbox.get("1.0", END) + "\n"
        mi_content = "密  文:" + state[1]
        self.st.delete('1.0', END)
        self.st.insert(END, name_content)
        self.st.insert(END, ming_content)
        self.st.insert(END, mi_content)

    def createPage(self):
        self.root.update()
        max_x = self.root.winfo_width()
        max_y = self.root.winfo_height()
        #ttk.Label(self, font=30, text='发送短报文').grid(row=1, stick='W')
        ttk.Label(self, font=('',10,), text='收件人').grid(row=1,column=0, stick='W',pady=10,)
        ttk.Label(self, font=('',10,), text='正文').grid(row=2,column=0, stick='W')
        self.recvname = ttk.Entry(self, width=max_x // 17)
        self.recvname.configure(font=('',10,))
        self.recvname.grid(row=1,column=1, stick='E',ipady=10,pady=10,)
        self.msgbox = ttk.Text(self,width=max_x // 17)
        self.msgbox.configure(font=('',10,))
        self.msgbox.grid(row=2, column=1)#, columnspan=2
        self.send_button = ttk.Button(self, width=30, text='发送', command=self.sendMsg)
        self.send_button.grid(row=3, column=1, padx=30,pady=10,stick='W')
        ttk.Button(self, width=30, text='清空内容', command=self.clearText).grid(row=3, column=1, padx=30,stick='E')

        # name_content="发件人"+self.recvname.get()
        # ming_content="明  文"+self.msgbox.get()

        #暂时删除
        self.lf = ttk.Labelframe(self,text="该部分仅做加密展示，不作为实用前端",  width=max_x // 17, height=60)
        self.lf.grid(row=5, column=1)
        self.st = ScrolledText(self.lf, padding=5, height=10, autohide=True)
        self.st.pack(fill=BOTH, expand=YES)

        # self.st.delete('1.0', END)
        # self.st.insert(END, name_content)
        # self.st.insert(END, ming_content)


    def clearText(self):
        self.msgbox.delete('1.0', 'end')

