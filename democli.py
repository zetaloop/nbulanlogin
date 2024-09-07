#from core import getstate, login, logout

#username = "NAME"
#password = "PSWD"

#state = getstate()
#match state:
#    case "Connected":
#        print("当前已登录")
#    case "Login":
#        print("当前未登录")
#        match login(state.more, username, password):
#            case "Success":
#                print("登录成功")
#            case "Failed":
#                print(f"登录失败: {state.more}")
#            case "NetworkError":
#                print("连接失败")
#    case "Unknown":
#        print(f"数据异常: {state.more[:400]}")
#    case "NetworkError":
#        print("网络连接失败")

import argparse
import time
import datetime
from core import getstate, login, logout

def main():
    parser = argparse.ArgumentParser(description="nbulogging")
    parser.add_argument('action', nargs='?', default='login', help="login(default) logout relogin")
    parser.add_argument('--username', '-u', required=True, help="username")
    parser.add_argument('--password', '-p', required=True, help="password")
    args = parser.parse_args()

    if args.action == 'logout':
        logout()
        print("已登出")
    elif args.action == 'relogin':
        logout()
        print("已登出，正在重新登录...")
        time.sleep(3)
        perform_login(args.username, args.password)
    else:
        perform_login(args.username, args.password)

def perform_login(username, password):
    state = getstate()
    match state:
        case "Connected":
            print("当前已登录")
        case "Login":
            print("当前未登录")
            match login(state.more, username, password):
                case "Success":
                    print("登录成功")
                case "Failed":
                    print(f"登录失败: {state.more}")
                case "NetworkError":
                    print("连接失败")
        case "Unknown":
            print(f"数据异常: {state.more[:400]}")
        case "NetworkError":
            print("网络连接失败")

if __name__ == "__main__":
	print(datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S'))
	main()
