from core import getstate, login, logout

username = "NAME"
password = "PSWD"

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
