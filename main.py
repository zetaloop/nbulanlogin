import os, webbrowser
from core import getstate, login, logout
from config import get, set
import proxy
from version import vertxt

def update_state():
    status_var.set('正在查询状态')
    root.update()
    proxy.disable()
    msg = {
        'Connected': '已登录',
        'Login': '未登录',
        'Unknown': '服务器状态异常',
        'NetworkError': '连不上服务器',
        }
    sta = msg[getstate()]
    status_var.set(sta)
    if sta == '未登录' and get('autologin'):
        login_btn()
    proxy.restore()

def login_btn():
    status_var.set('正在登录')
    root.update()
    proxy.disable()
    url = getstate()
    match url:
        case 'Login':
            result = login(url.more, username_var.get(), password_var.get())
            if result == 'Success':
                sta = '登录成功'
            else:
                sta = f'登录失败：{result.more}'
        case 'Connected':
            sta = '登录失败：不能重复登录'
        case 'Unknown':
            sta = '登录失败：未知服务器状态'
        case 'NetworkError':
            sta = '登录失败：连不上服务器'
    status_var.set(sta)
    proxy.restore()

def logout_btn():
    status_var.set('正在退出')
    root.update()
    proxy.disable()
    url = getstate()
    match url:
        case 'Connected':
            result = logout()
            if result == 'Success':
                sta = '退出成功'
            else:
                sta = f'退出失败：{result.more}'
        case 'Login':
            sta = '退出失败：不能重复退出'
        case 'Unknown':
            sta = '退出失败：未知服务器状态'
        case 'NetworkError':
            sta = '退出失败：连不上服务器'
    status_var.set(sta)
    proxy.restore()

def settings_btn():
    import tkinter as tk
    from tkinter import ttk

    # 创建一个新的顶层窗口
    settings = tk.Toplevel(root)
    settings.withdraw()
    settings.title("设置")
    settings.iconbitmap('lanlogin.ico')
    settings.resizable(False, False)
    settings.bind('<Control-w>', lambda _: settings.destroy())
    settings.bind('<Escape>', lambda _: settings.destroy())

    # 间距
    frm = ttk.Frame(settings)
    frm.pack(padx=10, pady=5, fill='x', expand=True)

    ttk.Label(settings, justify='center', text=f'宁大宽带登录器 NBU LAN Login {vertxt}').pack(pady=5, padx=20)
    ttk.Label(settings, justify='center', text='让寝室宽带使用更加高效', style='small.TLabel').pack(pady=5, padx=20)
    ttk.Label(settings, justify='center', text='Designed by Zetaloop', style='small.TLabel').pack(pady=5, padx=20)
    ttk.Label(settings, justify='center', text='github.com/zetaloop/nbulanlogin', style='verysmall.TLabel').pack(pady=5, padx=20)

    # 创建一个框架来存放复选框
    frm = ttk.Frame(settings)
    frm.pack(padx=20, pady=10, fill="x", expand=True)

    # 创建变量来存储复选框的状态
    autostart_var = tk.BooleanVar(value=get('autostart'))
    autologin_var = tk.BooleanVar(value=get('autologin'))
    disableproxy_var = tk.BooleanVar(value=get('disableproxy'))
    autostart_var.trace_add('write', autosave('autostart', autostart_var))
    autologin_var.trace_add('write', autosave('autologin', autologin_var))
    disableproxy_var.trace_add('write', autosave('disableproxy', disableproxy_var))

    # 创建复选框
    autostart_cb = ttk.Checkbutton(frm, text="开机启动", variable=autostart_var)
    autologin_cb = ttk.Checkbutton(frm, text="自动登录", variable=autologin_var)
    disableproxy_cb = ttk.Checkbutton(frm, text="自动关闭代理", variable=disableproxy_var)
    autostart_cb.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    autologin_cb.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    disableproxy_cb.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    # 创建按钮
    frm = ttk.Frame(settings)
    frm.pack(padx=20, pady=0, fill='x', expand=True)
    ttk.Button(frm, text="宽带登录页面", command=origlogin_btn).grid(row=0, column=0, padx=10, pady=5, sticky='ew')
    ttk.Button(frm, text="宽带管理页面", command=origmanage_btn).grid(row=0, column=1, padx=10, pady=5, sticky='ew')
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(1, weight=1)

    # 间距
    frm = ttk.Frame(settings)
    frm.pack(padx=10, pady=10, fill='x', expand=True)

    # 使窗口成为模态窗口
    settings.transient(root)
    settings.grab_set()

    # 启动窗口
    settings.update()
    settings.deiconify()

    # 修复按钮状态，只有deiconify后延时去除alternate状态才是有效的
    root.after(0, lambda:autostart_cb.state(['!alternate']))
    root.after(0, lambda:autologin_cb.state(['!alternate']))
    root.after(0, lambda:disableproxy_cb.state(['!alternate']))

def origlogin_btn():
    webbrowser.open('http://10.36.100.2:8181/')

def origmanage_btn():
    webbrowser.open('http://10.36.100.1:8080/')

def autosave(name, var):
    def callback(*_):
        set(name, var.get())
    return callback

def ui():
    import tkinter as tk
    from tkinter import ttk
    import sv_ttk

    # 更改当前工作目录到脚本所在的目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 创建主窗口
    global root
    root = tk.Tk()
    root.withdraw()
    root.title("宁大宽带登录器")
    root.iconbitmap('lanlogin.ico')
    root.resizable(False, False)
    root.bind('<Control-w>', lambda e: root.destroy())
    root.bind('<Escape>', lambda e: root.destroy())
    root.bind('<Control-r>', lambda e: update_state())
    sv_ttk.set_theme("light")

    # 设置字体
    style = ttk.Style()
    style.configure("TEntry", font=("Microsoft YaHei UI", 10))
    style.configure("TButton", font=("Microsoft YaHei UI", 10))
    style.configure("TCheckbutton", font=("Microsoft YaHei UI", 10))
    style.configure("TLabel", font=("Microsoft YaHei UI", 10))
    style.configure("big.TLabel", font=("Microsoft YaHei UI", 11))
    style.configure("small.TLabel", font=("Microsoft YaHei UI", 9))
    style.configure("verysmall.TLabel", font=("Microsoft YaHei UI", 8))

    # 创建一个frame来存放输入框和标签
    frm = ttk.Frame(root)
    frm.pack(pady=20, padx=20, fill="x", expand=True)

    # 添加用户名和密码标签和输入框
    global username_var, password_var
    username_var = tk.StringVar(value=get('username'))
    password_var = tk.StringVar(value=get('password'))
    username_var.trace_add('write', autosave('username', username_var))
    password_var.trace_add('write', autosave('password', password_var))
    ttk.Label(frm, text="账号").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(frm, text="密码").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    username_entry = ttk.Entry(frm, textvariable=username_var)
    password_entry = ttk.Entry(frm, textvariable=password_var, show="*")
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    username_entry.bind('<Return>', lambda e: login_btn())
    password_entry.bind('<Return>', lambda e: login_btn())
    frm.grid_columnconfigure(1, weight=1)

    # 创建按钮
    frm = ttk.Frame(root)
    frm.pack(padx=20, pady=0, fill='x', expand=True)
    ttk.Button(frm, text="登录", command=login_btn, style="Accent.TButton").grid(row=0, column=0, padx=10, pady=0, sticky='ew')
    ttk.Button(frm, text="退出", command=logout_btn).grid(row=0, column=1, padx=10, pady=0, sticky='ew')
    ttk.Button(frm, text="· · ·", command=settings_btn).grid(row=0, column=2, padx=10, pady=0, sticky='ew')

    # 设置列权重，使按钮可以拉长
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(1, weight=1)
    frm.grid_columnconfigure(2, weight=1)

    # 创建状态栏
    global status_var
    status_var = tk.StringVar()
    status_var.set("")
    status_bar = ttk.Label(root, textvariable=status_var, anchor="center", style='small.TLabel')
    status_bar.pack(fill="x", padx=25, pady=20)
    status_bar.bind('<Button-1>', lambda e: update_state())
    root.after(0, update_state)

    # 启动窗口
    root.update()
    root.deiconify()
    root.mainloop()

if __name__ == '__main__':
    ui()
    exit()