import argparse
import time
import datetime
from core import getstate, login, logout


def main():
    parser = argparse.ArgumentParser(description="[== NBU LAN Login ==]")
    parser.add_argument(
        "action",
        nargs="?",
        default="login",
        choices=["login", "logout", "relogin"],
        help="the action to perform (default: %(default)s)",
    )
    parser.add_argument(
        "-u",
        "--username",
        required=True,
        metavar="MyName",
        help="network account username",
    )
    parser.add_argument(
        "-p",
        "--password",
        required=True,
        metavar="aBc123",
        help="network account password",
    )
    args = parser.parse_args()

    if args.action == "logout":
        logout()
        print("已登出")
    elif args.action == "relogin":
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
    print(datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
    main()
