# coding=gbk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Beidou_client import StartPage
from pathlib import Path
from ttkbootstrap.constants import *

from PIL import Image
from PIL import ImageTk

root = ttk.Window()#size=(1066,600)themename="morph"
#root.configure(inputbg='#bcdbdc')
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

root.geometry("%dx%d" %(w,h))
#root.wm_attributes('-transparentcolor', '#ab23ff')

def get_img(filename,wi,hei):
    im = Image.open(filename).resize((w, h))
    im=ImageTk.PhotoImage(im)
    return im
file_path = Path(__file__).parent /'global.jpg'
canvas_root = ttk.Canvas( width=w, height=h)
im_root = get_img(file_path, w, h)
canvas_root.create_image(w/2, h/2, image=im_root)
canvas_root.place(x=0,y=0)#side='top'
#bgl=ttk.Label(image=im_root1,compound=ttk.CENTER)
#bgl.pack(side='top')



'''
f= ttk.Frame(bootstyle=SUCCESS)
f.place(x=10,y=10,width=1800,height=100)

lf = ttk.Labelframe(bootstyle=PRIMARY,width=100,height=60)
lf.place(x=20,y=210,width=300,height=100)
ttk.Label(lf,text="标签").pack()

ttk.Label(f,text="北斗客户端").pack()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
print(w)
print(h)
root.geometry("%dx%d" %(w,h))
root.title("北斗客户端")
#root.attributes('-fullscreen', True)   # 全屏 没有工具栏

# root.state('zoomed')    # 最大化运行,树莓派中无此用法，报错！！！
#root.geometry('800x800')

root.update()
StartPage.StartPage(root)
#LoginPage.LoginPage(root)
root.mainloop()
'''


#bgg(root)
def loadingGif(root):
#图片太大且不随页面缩放

    numIdx = 12  # gif的帧数
    file_path = Path(__file__).parent / "bg3.gif"
    frames = [ttk.PhotoImage(file=file_path,)]# format='gif -index %i' % (i)) for i in range(numIdx)]


    def run(rate):
        frame = frames[rate]
        rate += 1
        gif_label.configure(image=frame)  # 显示当前帧的图片
        gif_label.configure(image=frames)
        gif_label.after(100, run, rate % numIdx)  # 0.1秒(100毫秒)之后继续执行函数(run)
    gif_label = ttk.Label(root)
    gif_label.pack(side='bottom',padx=0,ipadx=1)
    #run(0)
#loadingGif(root)

StartPage.StartPage(root)
root.mainloop()