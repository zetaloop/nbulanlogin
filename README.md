## NBU LAN Login 宁大宽带登录器

![image](https://github.com/zetaloop/nbulanlogin/assets/36418285/f65101e2-e14d-4e69-87d2-5f3d36a3104c)

## 功能

- 一键登录和退出
- 记住账号密码
- 开机启动
- 定时退出重登
- 支持命令行参数
- 跨平台

## 下载

单文件打包 [Windows / Linux / macOS] * [x64 / arm64]

v3.1 20250511 [点击前往发行版下载](https://github.com/zetaloop/nbulanlogin/releases/latest)

## 使用源代码
### Python 依赖库
```bash
# 基础功能
pip install -U requests
# 图形界面依赖
pip install -U sv-ttk
# Windows创建快捷方式
pip install -U pywin32
# 打包
pip install -U pyinstaller
```
直接运行 `lanlogin.py` 可打开图形界面。

传入命令行参数可执行对应功能。

### 命令行参数

```
lanlogin.py [-h] [-u USERNAME] [-p PASSWORD] [{login,logout,relogin,check}]
```

- `-h` `--help` 显示帮助
- `-u` `--username` 账号
- `-p` `--password` 密码
- `login` 登录 / `logout` 退出 / `relogin` 重新登录 / `check` 检查登录状态

## 技术细节

UI: tkinter, sv-ttk

API: 参考 [NBU_Auto_Connect](https://github.com/BytePrince/NBU_Auto_Connect) 有改动

可爱地采用 GPL 3.0 开源
