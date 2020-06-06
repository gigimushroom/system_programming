#import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
import addr_converter as ad

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.l = Label(self, 
            text='输入需要修改地址的excel',    # 标签的文字
            bg='lavender',     # 背景颜色
            font=('Arial', 20),     # 字体和字体大小
            width=25, height=2  # 标签长宽
            )
        self.l.pack()    # 固定窗口位置
        
        self.nameInput = Entry(self, font=('Arial', 20))
        self.nameInput.pack()
        self.alertButton = Button(self, text='转换地址！', font=('Arial', 20),  width=10, height=4,
                                    bg='mint cream', fg="red", command=self.hello)
        self.alertButton.pack()
        
        self.quitButton = Button(self, fg="grey", text='点我退出', command=self.quit)
        self.quitButton.pack(side="bottom")

    def hello(self):
        name = self.nameInput.get() or 'addr.xls'
        done = ad.run(name)
        if done:
            messagebox.showinfo('Message', '地址转化成功: %s' % name) 
        else:
            messagebox.showinfo('Message', '警告：地址转化失败: %s！请联系蘑菇小弟！' % name) 

app = Application()                       
app.master.title('华夏快递公司订单系统')    
app.master.geometry("500x300")
app.mainloop()