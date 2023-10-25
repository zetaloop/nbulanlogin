import os, sys, webbrowser
from core import getstate, login, logout
from config import get, set
from version import vertxt


def update_state():
    status_var.set("正在查询状态")
    root.update()
    msg = {
        "Connected": "已登录",
        "Login": "未登录",
        "Unknown": "服务器状态异常",
        "NetworkError": "连不上服务器",
    }
    sta = msg[getstate()]
    status_var.set(sta)
    if sta == "未登录" and get("autologin"):
        login_btn()


def login_btn():
    status_var.set("正在登录")
    root.update()
    url = getstate()
    match url:
        case "Login":
            result = login(url.more, username_var.get(), password_var.get())
            if result == "Success":
                sta = "登录成功"
            else:
                sta = f"登录失败：{result.more}"
        case "Connected":
            sta = "登录已经完成：无需重复登录"
        case "Unknown":
            sta = "登录失败：未知服务器状态"
        case "NetworkError":
            sta = "登录失败：连不上服务器"
    status_var.set(sta)


def logout_btn():
    status_var.set("正在退出")
    root.update()
    url = getstate()
    match url:
        case "Connected":
            result = logout()
            if result == "Success":
                sta = "退出成功"
            else:
                sta = f"退出失败：{result.more}"
        case "Login":
            sta = "退出已经完成：无需重复退出"
        case "Unknown":
            sta = "退出失败：未知服务器状态"
        case "NetworkError":
            sta = "退出失败：连不上服务器"
    status_var.set(sta)


def settings_btn():
    import tkinter as tk
    from tkinter import ttk

    # 创建一个新的顶层窗口
    settings = tk.Toplevel(root)
    settings.withdraw()
    settings.title("设置")
    settings.iconbitmap("lanlogin.ico")
    settings.resizable(False, False)
    settings.bind("<Control-w>", lambda _: settings.destroy())
    settings.bind("<Escape>", lambda _: settings.destroy())

    # 间距
    frm = ttk.Frame(settings)
    frm.pack(padx=10, pady=5, fill="x", expand=True)

    ttk.Label(settings, justify="center", text=f"宁大宽带登录器 NBU LAN Login {vertxt}").pack(
        pady=5, padx=20
    )
    ttk.Label(
        settings, justify="center", text="让宿舍宽带使用更加高效", style="small.TLabel"
    ).pack(pady=5, padx=20)
    ttk.Label(
        settings, justify="center", text="Designed by Zetaloop", style="small.TLabel"
    ).pack(pady=5, padx=20)
    ttk.Label(
        settings,
        justify="center",
        text="github.com/zetaloop/nbulanlogin",
        style="verysmall.TLabel",
    ).pack(pady=5, padx=20)

    # 创建一个框架来存放复选框
    frm = ttk.Frame(settings)
    frm.pack(padx=20, pady=10, fill="x", expand=True)

    # 创建变量来存储复选框的状态
    global autostart_var, autologin_var, autorefresh_var, refreshtime_var
    autostart_var = tk.BooleanVar(value=get("autostart"))
    autologin_var = tk.BooleanVar(value=get("autologin"))
    autorefresh_var = tk.BooleanVar(value=get("autorefresh"))
    refreshtime_var = tk.StringVar(value=get("refreshtime"))
    autostart_var.trace_add("write", autosave("autostart", autostart_var))
    autostart_var.trace_add("write", lambda *_: root.after(0, set_startup))
    autologin_var.trace_add("write", autosave("autologin", autologin_var))
    autorefresh_var.trace_add("write", autosave("autorefresh", autorefresh_var))
    autorefresh_var.trace_add("write", lambda *_: root.after(0, set_refresh))
    refreshtime_var.trace_add("write", autosave("refreshtime", refreshtime_var))
    refreshtime_var.trace_add("write", lambda *_: root.after(0, lambda: set_refresh(0)))

    # 创建复选框
    autostart_cb = ttk.Checkbutton(frm, text="开机启动", variable=autostart_var)
    autologin_cb = ttk.Checkbutton(frm, text="自动登录", variable=autologin_var)
    autorefresh_cb = ttk.Checkbutton(frm, text="定时重登", variable=autorefresh_var)
    refreshtime_frm = ttk.Frame(frm)
    refreshtime_validator = settings.register(lambda P: P == "" or P.isdigit())
    # ttk.Label(refreshtime_frm, text="间隔").grid(row=0, column=0, padx=5, pady=0, sticky="w")
    ttk.Entry(
        refreshtime_frm,
        textvariable=refreshtime_var,
        width=4,
        validate="key",
        validatecommand=(refreshtime_validator, "%P"),
    ).grid(row=0, column=1, padx=5, pady=0, sticky="w")
    ttk.Label(refreshtime_frm, text="h").grid(
        row=0, column=2, padx=5, pady=0, sticky="w"
    )
    autostart_cb.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    autologin_cb.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    autorefresh_cb.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    refreshtime_frm.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    # 创建按钮
    frm = ttk.Frame(settings)
    frm.pack(padx=20, pady=0, fill="x", expand=True)
    ttk.Button(frm, text="宽带登录页面", command=origlogin_btn).grid(
        row=0, column=0, padx=10, pady=5, sticky="ew"
    )
    ttk.Button(frm, text="宽带管理页面", command=origmanage_btn).grid(
        row=0, column=1, padx=10, pady=5, sticky="ew"
    )
    ttk.Button(frm, text="关闭", command=settings.destroy, style="Accent.TButton").grid(
        row=1, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew"
    )
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(1, weight=1)

    # 间距
    frm = ttk.Frame(settings)
    frm.pack(padx=10, pady=10, fill="x", expand=True)

    # 使窗口成为模态窗口
    settings.transient(root)
    settings.grab_set()

    # 启动窗口
    settings.update()
    settings.deiconify()

    # 修复按钮状态，只有deiconify后延时去除alternate状态才是有效的
    root.after(0, lambda: autostart_cb.state(["!alternate"]))
    root.after(0, lambda: autologin_cb.state(["!alternate"]))


def origlogin_btn():
    """打开原版登录网页"""
    webbrowser.open("http://10.36.100.2:8181/")


def origmanage_btn():
    """打开原版管理网页"""
    webbrowser.open("http://10.36.100.1:8080/")


def set_startup():
    sysname = sys.platform.replace("win32", "windows").replace("darwin", "macos")
    if get("autostart"):
        if sysname == "windows":  # 将自身快捷方式放入开机自启文件夹
            set_startup_win()
        else:
            from tkinter import messagebox

            messagebox.showwarning(
                "开机自启暂不支持",
                "自动设置开机自启目前仅支持 Windows 系统，" f"当前系统 {sysname} 暂不支持，" "请自行寻找设置开机自启的方法",
            )
    else:
        if sysname == "windows":
            del_startup_win()


def set_startup_win():
    # 获取自身路径
    if getattr(sys, "frozen", False):
        target_path = sys.executable
    else:
        target_path = os.path.abspath(__file__)
    # 定义快捷方式路径
    startup_path = (
        os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\Startup"
    )
    shortcut_path = os.path.join(startup_path, "NBU LAN Login.lnk")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
    # 创建快捷方式
    from win32com.client import Dispatch

    shortcut = Dispatch("WScript.Shell").CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.Description = "宁大宽带登录器"
    shortcut.save()
    status_var.set("开机自启已保存到系统")


def del_startup_win():
    startup_path = (
        os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\Startup"
    )
    shortcut_path = os.path.join(startup_path, "NBU LAN Login.lnk")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
    status_var.set("开机自启已从系统删除")


refresh_tasks = []


def set_refresh(update=True):
    if update and get("autorefresh"):
        logout_btn()
        root.update()
        login_btn()
        root.update()
    if not get("autorefresh"):
        while refresh_tasks:
            try:
                root.after_cancel(refresh_tasks.pop())
            except:
                pass
    if update and get("autorefresh"):
        hours = get("refreshtime")
        if hours.isdigit():
            hours = int(hours)
        else:
            hours = 0
            refreshtime_var.set("0")
        if hours > 0:
            ms = hours * 60 * 60 * 1000
            root.after(ms, set_refresh)


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
    root.iconbitmap("lanlogin.ico")
    root.resizable(False, False)
    root.bind("<Control-w>", lambda e: root.destroy())
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Control-r>", lambda e: update_state())
    sv_ttk.set_theme("light")

    if __name__ == "__main__" and len(sys.argv) > 1:  # 支持命令行参数登录和退出
        if sys.argv[1] == "help":
            print("USAGE: lanlogin.exe [login/logout]")
            sys.exit()
        elif sys.argv[1] == "login":
            root.after(300, login_btn)
            root.after(2000, root.destroy)
        elif sys.argv[1] == "logout":
            root.after(300, logout_btn)
            root.after(2000, root.destroy)
        else:
            print("Invalid command line argument")
            sys.exit()

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
    username_var = tk.StringVar(value=get("username"))
    password_var = tk.StringVar(value=get("password"))
    username_var.trace_add("write", autosave("username", username_var))
    password_var.trace_add("write", autosave("password", password_var))
    ttk.Label(frm, text="账号").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(frm, text="密码").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    username_entry = ttk.Entry(frm, textvariable=username_var)
    password_entry = ttk.Entry(frm, textvariable=password_var, show="*")
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    username_entry.bind("<Return>", lambda e: login_btn())
    password_entry.bind("<Return>", lambda e: login_btn())
    frm.grid_columnconfigure(1, weight=1)

    # 创建按钮
    frm = ttk.Frame(root)
    frm.pack(padx=20, pady=0, fill="x", expand=True)
    ttk.Button(frm, text="登录", command=login_btn, style="Accent.TButton").grid(
        row=0, column=0, padx=10, pady=0, sticky="ew"
    )
    ttk.Button(frm, text="退出", command=logout_btn).grid(
        row=0, column=1, padx=10, pady=0, sticky="ew"
    )
    ttk.Button(frm, text="· · ·", command=settings_btn).grid(
        row=0, column=2, padx=10, pady=0, sticky="ew"
    )

    # 设置列权重，使按钮可以拉长
    frm.grid_columnconfigure(0, weight=1)
    frm.grid_columnconfigure(1, weight=1)
    frm.grid_columnconfigure(2, weight=1)

    # 创建状态栏
    global status_var
    status_var = tk.StringVar()
    status_var.set("")
    status_bar = ttk.Label(
        root, textvariable=status_var, anchor="center", style="small.TLabel"
    )
    status_bar.pack(fill="x", padx=25, pady=20)
    status_bar.bind("<Button-1>", lambda e: update_state())
    root.after(0, update_state)

    # 启动窗口
    root.update()
    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    ui()
