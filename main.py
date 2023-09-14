import client as c
from config import get, set

def update_state():
    status_var.set('加载中...')
    root.update()
    msg = {
        'Success': '已登录',
        'Login': '未登录',
        'UnknownURL': '宽带服务器地址异常',
        'NetworkError': '无法连接到宽带服务器',
        }
    sta = msg[c.getstate()]
    status_var.set(sta)

def ui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    import sv_ttk

    # 创建主窗口
    global root
    root = tk.Tk()
    root.title("宁大宽带登录")
    sv_ttk.set_theme("light")

    # 设置字体
    style = ttk.Style()
    style.configure("TEntry", font=("Microsoft YaHei UI", 10))
    style.configure("TButton", font=("Microsoft YaHei UI", 10))
    style.configure("TLabel", font=("Microsoft YaHei UI", 9))

    # 创建一个frame来存放输入框和标签
    frm = ttk.Frame(root)
    frm.pack(pady=20, padx=20, fill="x", expand=True)

    # 添加用户名和密码标签和输入框
    ttk.Label(frm, text="账号").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username_entry = ttk.Entry(frm)
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frm, text="密码").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry = ttk.Entry(frm, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    frm.grid_columnconfigure(1, weight=1)

    login=logout=manage=lambda:None

    # 创建按钮
    frm = ttk.Frame(root)
    frm.pack(padx=20, pady=0, fill='x', expand=True)
    ttk.Button(frm, text="登录", command=login).grid(row=0, column=0, padx=5, pady=0, sticky='ew')
    ttk.Button(frm, text="登出", command=logout).grid(row=0, column=1, padx=5, pady=0, sticky='ew')
    ttk.Button(frm, text="打开管理界面", command=manage).grid(row=0, column=2, padx=5, pady=0, sticky='ew')

    # 设置列权重，使按钮可以拉长
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(1, weight=1)
    frm.grid_columnconfigure(2, weight=1)

    # 创建状态栏
    global status_var
    status_var = tk.StringVar()
    status_var.set("")
    status_bar = ttk.Label(root, textvariable=status_var, anchor="center")
    status_bar.pack(fill="x", padx=25, pady=20)
    root.after(0, update_state)

    # 启动窗口
    root.mainloop()


if __name__ == '__main__':
    ui()
    exit()

state = c.getstate()
match state:
    case 'Success':
        print('当前已登录')
        match c.logout():
            case 'Success':
                print('退出成功')
            case 'Failed':
                print('退出失败')
            case 'NetworkError':
                print(f'连接失败: {state.more}')
    case 'Login':
        print('当前未登录')
        match c.login(username, password):
            case 'Success':
                print('登录成功')
            case 'Failed':
                print('登录失败')
            case 'NetworkError':
                print(f'连接失败: {state.more}')
    case 'UnknownURL':
        print(f'网址异常: {state.more}')
    case 'NetworkError':
        print(f'连接失败: {state.more}')

c.close()

restore_proxy()