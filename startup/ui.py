#import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
import runner

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.l = Label(self, 
            text='输入需要修改的excel',    # 标签的文字
            bg='lavender',     # 背景颜色
            font=('Arial', 20),     # 字体和字体大小
            width=25, height=2  # 标签长宽
            )
        self.l.pack()    # 固定窗口位置
        
        self.nameInput = Entry(self, font=('Arial', 20))
        self.nameInput.pack()
        self.alertButton = Button(self, text='转换重复的地址和身份证', font=('Arial', 20),  width=20, height=3,
                                    bg='mint cream', fg="red", command=self.change)
        self.alertButton.pack()
        
        self.splitButton = Button(self, text='分解省市区', font=('Arial', 20),  width=20, height=3,
                                    bg='mint cream', fg="blue", command=self.split)
        self.splitButton.pack()
        
        self.quitButton = Button(self, fg="grey", text='点我退出', height=2, command=self.quit)
        self.quitButton.pack(side="bottom")

    def change(self):
        name = self.nameInput.get() or 'aaa.xlsm'
        done = runner.remove_addr_and_id_dup(name)
        if done:
            messagebox.showinfo('Message', '地址转化成功: %s 文件名haha.xlsm' % name) 
        else:
            messagebox.showinfo('Message', '警告：地址转化失败: %s！请联系蘑菇小弟！' % name) 
            
    def split(self):
        name = self.nameInput.get() or 'addr_replace.xls'
        done = runner.split_addr(name)
        if done:
            messagebox.showinfo('Message', '分省市区转化成功: %s 文件名splitted.xlsm' % name) 
        else:
            messagebox.showinfo('Message', '警告：分省市区失败: %s！请联系蘑菇小弟！' % name) 

app = Application()                       
app.master.title('华夏快递公司自动化工具')    
app.master.geometry("500x300")
app.mainloop()