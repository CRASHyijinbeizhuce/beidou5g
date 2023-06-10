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
        self.root = master  # �����ڲ�����root
        self.Errornum = 0
        self.root.title("��Ѷ���ͻ���")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (w, h))
        self.root.f = ttk.Frame(bootstyle=SUCCESS)
        self.root.f.pack(side=TOP, padx=10)
        #label = ttk.Label(self.root.f, text="�����ͻ���", font=("�����п�", 40))
        #label.pack(fill=BOTH, expand=YES,side=TOP)
        self.get_port = ttk.StringVar()
        # self.root.geometry('%dx%d' % (600, 400))  # ���ô��ڴ�С


        self.page = ttk.Frame(self.root)  # ����Frame


        #self.get_port = ttk.StringVar()
        self.createPage()

        portx = str(get_port_list.get_port_list()[0])
        serObject = seri.open_ser(portx)
        j1 = 0
        j2 = 0
        # ��鱱������Ƿ���������
        judge1 = True
        while judge1:
            if portx:#'Prolific USB-to-Serial Comm Port' in portx:
                j1 = 1
                judge1 = False
            else:
                Messagebox.show_error(title='����', message='���鱱������Ƿ�������ȷ')
                judge1 = False

        # ����豸�Ƿ�ע��
        judge2 = True
        while judge2:
            # try:
            device_state = devi()
            # print("device_state=", device_state)
            if not device_state[0]:
                Messagebox.show_error(title='����', message='%s' % device_state[1])
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
        # s.configure('my_style', font=('����',25))
        max_x = self.root.winfo_width()/3
        max_y = self.root.winfo_height()/3
        self.root.update()
        #tk.Label(self.page).grid(row=0, stick='W', pady=max_y / 8)
        ttk.Label(self.page,  text='��ǰ��������ʹ�õĴ�����:',font=('',20,)).grid(row=1, column=0, stick='W', pady=15, padx=30)
        # port_box = ttk.Combobox(self.page, textvariable=self.get_port)  # ��ʼ��
        ttk.Label(self.page,  text=get_port_list.get_port_list()[0],font=('',20,)).grid(row=1, column=1, stick='W', pady=15,
                                                                               padx=30)
        # port_box["values"] = get_port_list.get_port_list()
        # port_box.grid(row=1, column=1, columnspan=5, pady=15)
        self.a=ttk.Button(self.page, width=45,text='����',  bootstyle=(PRIMARY, OUTLINE), command=self.run,)
        self.a.grid(row=2, column=0,pady=15)
        #self.a.config(font=("����", 20))
        ttk.Button(self.page, width=45, text='�˳�', bootstyle=(PRIMARY, OUTLINE), command=self.exit,).grid(row=2,
                                                                                                         column=1,
                                                                                                         pady=15)

    def run(self):
        if self.Errornum>5:
            Messagebox.show_error(title='����', message='���Ӵ������࣬���Ժ�����')
            time = 300
            self.ct_down1(time)
            self.Errornum=0
        portx =str(get_port_list.get_port_list()[0])
        print(portx)
        serObject = seri.open_ser(portx)
        j1=0
        j2=0
        # ��鱱������Ƿ���������
        judge1 = True
        while judge1:
            if portx:#'Prolific USB-to-Serial Comm Port' in portx:
                j1=1
                judge1 = False
            else:
                Messagebox.show_error(title='����', message='���鱱������Ƿ�������ȷ')
                judge1 = False

        # ����豸�Ƿ�ע��
        judge2 = True
        while judge2:
            # try:
            device_state = devi()
            # print("device_state=", device_state)
            if not device_state[0]:
                Messagebox.show_error(title='����', message='%s' % device_state[1])
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

    def ct_down1(self, m):  # ����ʱ����
        m = m - 1  # ÿ�μ���һ�������ټ������
        self.id1 = self.root.after(1000, self.ct_down1, m)
        # ����after�����Լ������Լ����е�ݹ����˼��after����������Ϳ��Ե��ü�ʱ������ֱ����self.master�ˣ�Ϊʲô��ֵ��id��
        if m != 0:  # �������ʱû�н���
            dead_minutes = m // 60 % 60
            dead_seconds = m % 60
            s='%d��%d�������'%(dead_minutes,dead_seconds)

            self.a['text'] = s  # �ı䰴ť����
            self.a['state'] = 'disabled'
        else:  # ����ʱ����

            self.root.after_cancel(self.id1)  # ����������idȡ���ص�
            self.a['text'] = '����'
            self.a['state'] = 'normal'