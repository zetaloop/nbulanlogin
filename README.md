## NBU LAN Login 宁大宽带登录器

![image](https://github.com/zetaloop/nbulanlogin/assets/36418285/f65101e2-e14d-4e69-87d2-5f3d36a3104c)

## 功能

- 一键登录和退出
- 记住账号密码
- 开机启动（仅 Windows）
- 未登录时自动登录
- 定时退出重新登录
- 可命令行调用
- 忽略本机代理设定
- 主体功能跨平台

## 下载

*Windows 可下载已打包的 exe，其他系统运行原脚本或自行打包*

v2.8 20240620 [GitHub Releases](https://github.com/zetaloop/nbulanlogin/releases/latest)

## 直接使用源码

### Requirements: 
```
pip install -U requests sv_ttk
# 若在 windows 上运行：
pip install -U pywin32
# 若需要打包：
pip install -U pyinstaller
```
然后运行 `LANLogin.py` 打开主界面

## 技术细节

UI: tkinter, sv-ttk

API: 参考 [NBU_Auto_Connect](https://github.com/BytePrince/NBU_Auto_Connect) 有改动

GPL 3.0 开源
