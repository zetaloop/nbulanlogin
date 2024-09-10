import os, sys


def hide_console():
    """隐藏命令行窗口"""
    if sys.platform == "win32":
        import ctypes

        print("正在启动窗口，请稍等...")
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
            ctypes.windll.kernel32.CloseHandle(hwnd)


def win32_create_startup():
    # 获取环境变量
    appdata = os.getenv("APPDATA")
    assert appdata is not None
    # 获取自身路径
    if getattr(sys, "frozen", False):
        target_path = sys.executable
    else:
        target_path = os.path.abspath(__file__)
    # 定义快捷方式路径
    startup_path = appdata + r"\Microsoft\Windows\Start Menu\Programs\Startup"
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
    return "已创建开机自启快捷方式"


def win32_remove_startup():
    appdata = os.getenv("APPDATA")
    assert appdata is not None
    startup_path = appdata + r"\Microsoft\Windows\Start Menu\Programs\Startup"
    shortcut_path = os.path.join(startup_path, "NBU LAN Login.lnk")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        return "已删除开机自启快捷方式"
    else:
        return "未找到开机自启快捷方式"


PLIST_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.zetaloop.nbulanlogin</string>
    <key>ProgramArguments</key>
    <array>
        <string>{target_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""


def darwin_create_startup():
    target_path = os.path.abspath(__file__)
    plist_path = os.path.expanduser(
        "~/Library/LaunchAgents/com.zetaloop.nbulanlogin.plist"
    )
    if os.path.exists(plist_path):
        os.remove(plist_path)
    with open(plist_path, "w") as plist_file:
        plist_file.write(PLIST_TEMPLATE.format(target_path=target_path))
    os.system(f"launchctl load {plist_path}")

    return "已创建 plist 开机自启文件"


def darwin_remove_startup():
    plist_path = os.path.expanduser(
        "~/Library/LaunchAgents/com.zetaloop.nbulanlogin.plist"
    )
    if os.path.exists(plist_path):
        os.system(f"launchctl unload {plist_path}")
        os.remove(plist_path)
        return "已删除 plist 开机自启文件"
    else:
        return "未找到 plist 开机自启文件"


SYSTEMD_TEMPLATE = """[Unit]
Description=nbulanlogin auto start service

[Service]
ExecStart={target_path}
Restart=always

[Install]
WantedBy=default.target
"""


def linux_create_startup():
    target_path = os.path.abspath(__file__)
    systemd_path = os.path.expanduser("~/.config/systemd/user/nbulanlogin.service")
    if os.path.exists(systemd_path):
        os.remove(systemd_path)
    with open(systemd_path, "w") as systemd_file:
        systemd_file.write(SYSTEMD_TEMPLATE.format(target_path=target_path))
    os.system(f"systemctl --user enable nbulanlogin.service")
    os.system(f"systemctl --user start nbulanlogin.service")

    return "已创建 systemd 开机自启服务"


def linux_remove_startup():
    systemd_path = os.path.expanduser("~/.config/systemd/user/nbulanlogin.service")
    if os.path.exists(systemd_path):
        os.system(f"systemctl --user stop nbulanlogin.service")
        os.system(f"systemctl --user disable nbulanlogin.service")
        os.remove(systemd_path)
        return "已删除 systemd 开机自启服务"
    else:
        return "未找到 systemd 开机自启服务"


def default_create_startup():
    from tkinter import messagebox  # type: ignore

    messagebox.showwarning(
        "开机自启暂不支持",
        "当前系统暂不支持设置开机自启，请自行操作",
    )
    return None


def default_remove_startup():
    return None


match sys.platform:
    case "win32":
        create_startup = win32_create_startup
        remove_startup = win32_remove_startup
    case "darwin":
        create_startup = darwin_create_startup
        remove_startup = darwin_remove_startup
    case "linux":
        create_startup = linux_create_startup
        remove_startup = linux_remove_startup
    case default:
        create_startup = default_create_startup
        remove_startup = default_remove_startup
