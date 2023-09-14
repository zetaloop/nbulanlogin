import client as c
from proxy import *

username = "NAME"
password = "PSWD"
c.headless = True  # 无窗口模式


state = c.getstate()
match state:
    case 'Success':
        print('当前已登录')
        exit()
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
