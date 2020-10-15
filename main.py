from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter import font,messagebox
from compile.semantic import syntax_parse
from compile.lex import scan
file_text=''
def pre_interface():
    global root
    global code
    global analysis
    # file_text=StringVar()
    root = Tk()
    # ft = font.Font(size=12)
    code = Text(root, width=50, height=25, font=20)
    analysis = Text(root, width=35, height=25, font=10,relief=SUNKEN)
    # analysis = Text(root, width=115, height=35, font=ft,relief=SUNKEN)
    label_frame=Frame(root)
    label_frame.config(width=300,height=30)
    label_1=Label(label_frame,text="Pascal 源代码",font=15)
    # label_1.pack(side=LEFT,padx=150)
    label_1.pack(side=LEFT,padx=100)
    label_2=Label(label_frame,text="生成三地址码",font=15)
    label_2.pack(side=RIGHT,padx=350)
    button_frame=Frame(root)
    button_frame.config(width=300)
    # syntax_analyse = Button(button_frame, text='语法分析',  font=15,relief=SOLID,command=syntax_connect)
    # semantic_analyse = Button(button_frame, text='语义分析',  font=15,relief=SOLID,command=semantic_connect)
    # report = Button(button_frame, text='保存错误',  font=15,relief=SOLID,command=save_file)
    # syntax_analyse.pack(side=LEFT,padx=100)
    # semantic_analyse.pack(side=LEFT,padx=100)
    # report.pack(side=RIGHT,padx=100)
    Analysis = Button(button_frame, text='语义分析',  font=15,command=connect,relief=SOLID)
    Analysis.pack(side=LEFT,padx=150)
    load = Button(button_frame, text='保存错误信息', font=15,command=save_file,relief=SOLID)
    load.pack(side=LEFT,padx=350,pady=10)
    label_frame.pack(side=TOP,pady=10)
    button_frame.pack(side=BOTTOM,pady=10)
    root.title("Pascal语义分析器")
    code.pack(side=LEFT,padx=50)
    analysis.pack(side=RIGHT,padx=150)
    root.mainloop()

def connect():
    global file_text
    raw=code.get(1.0,END)
    token=scan(raw)
    output_1,error_report,error_flag=syntax_parse(token)
    file_text=error_report
    if error_flag!=0:
        messagebox.showerror('语义分析错误','可导出查看')
    analysis.delete(1.0,END)
    analysis.insert(1.0,output_1)

def save_file():
    global file_text
    file_path=''
    file_path = filedialog.asksaveasfilename(title=u'保存文件')
    print('保存文件：', file_path)
    print(file_text)
    if file_path is not None:
        with open(file=file_path, mode='w', encoding='utf-8') as file:
            file.write(file_text)
        code.delete('1.0', END)
        dialog.Dialog(None, {'title': 'File Modified', 'text': '保存完成', 'bitmap': 'warning', 'default': 0,
               'strings': ('OK', 'Cancle')})
    print('保存完成')
def main():
    pre_interface()


if __name__ == '__main__':
    main()