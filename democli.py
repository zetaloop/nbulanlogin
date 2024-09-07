import argparse
import time
import datetime
from core import getstate, login, logout, _xstr as XStrType


def get_current_state():
    state = getstate()
    match state:
        case "Connected":
            print("当前已登录")
            return True, None
        case "Login":
            print("当前未登录")
            return False, state.more
        case "Unknown":
            raise ValueError(f"数据异常: {state.more[:400]}")
        case "NetworkError":
            raise ConnectionError("网络连接失败")
        case never:
            assert False


def get_login_result(url, username, password):
    print("正在登录...")
    if username is None or password is None:
        raise ValueError("无法登录: 请指定用户名和密码")
    state = login(url, username, password)
    match state:
        case "Success":
            print("登录成功")
            return True  # Online
        case "Failed":
            assert isinstance(state, XStrType)
            raise RuntimeError(f"登录失败: {state.more}")
        case never:
            assert False


def get_logout_result():
    print("正在退出...")
    state = logout()
    match state:
        case "Success":
            print("退出成功")
            return False  # Offline
        case "Failed":
            assert isinstance(state, XStrType)
            raise RuntimeError(f"退出失败: {state.more}")
        case never:
            assert False


def main():
    parser = argparse.ArgumentParser(description="[== NBU LAN Login ==]")
    parser.add_argument(
        "action",
        nargs="?",
        default="login",
        choices=["login", "logout", "relogin", "check"],
        help="the action to perform (default: %(default)s)",
    )
    parser.add_argument(
        "-u",
        "--username",
        metavar="MyName",
        help="network account username",
    )
    parser.add_argument(
        "-p",
        "--password",
        metavar="aBc123",
        help="network account password",
    )
    args = parser.parse_args()

    match args.action:
        case "check":
            get_current_state()
        case "login":
            online, url = get_current_state()
            if not online:
                get_login_result(url, args.username, args.password)
        case "logout":
            online, _ = get_current_state()
            if online:
                get_logout_result()
        case "relogin":
            online, url = get_current_state()
            if online:
                get_logout_result()
                online, url = get_current_state()
                if not online:
                    try:
                        get_login_result(url, args.username, args.password)
                    except RuntimeError:
                        print("3秒后重试...")
                        time.sleep(3)
                        get_login_result(url, args.username, args.password)
            else:
                get_login_result(url, args.username, args.password)


if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
    main()
