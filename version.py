ver = [2, 1]
vertxt = 'v' + '.'.join(map(str, ver))

'''
VERSION LOG

1.x 20230912:
    实现使用 playwright 模拟登录和退出操作
    增加保存配置的功能基础
    增加自动关闭和开启代理功能（仅 win 平台）
    增加调试输出
    实现 CLI 和 UI 版本的初步操作

2.0 20230913:
    参考 https://github.com/BytePrince/NBU_Auto_Connect
    完成了直接调用查询、登录、退出 api 的操作
    移除 playwright 相关功能
    移除调试输出以简化代码

2.1 20230914:
    实现主界面、设置界面
    适配了自动登录功能
    适配和优化自动关闭代理功能（仅 win 平台）
    适配了配置读取和保存功能
    开机自启功能尚未完成

'''