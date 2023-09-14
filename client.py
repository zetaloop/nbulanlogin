from playwright.sync_api import sync_playwright
from proxy import disable_proxy, restore_proxy
from log import debug, realtime

headless = True  # 无窗口模式
timeout = 1000  # 连接超时

class _xstr(str):
    "带附件的字符串"
    def __new__(cls, value, more=None):
        obj = super().__new__(cls, value)
        obj.more = more
        return obj
    def __lshift__(self, more):
        self.more = more
        return self

class _xstr_factory:
    "附件字符串创建器"
    def __mul__(self, string):
        return _xstr(string)
xstr = _xstr_factory()

class viewer:
    "网页访问器基类"
    playwright = None
    browser = None
    context = None

    def __init__(self, function):
        self.function = function

    @classmethod
    def close(cls):
        if cls.playwright:
            debug('Stop chromium')
            cls.playwright.stop()
        restore_proxy()
        cls.context = cls.browser = cls.playwright = None


    def __call__(self, *args, **kwargs):
        if not viewer.browser:
            debug('Launch chromium')
            disable_proxy()
            viewer.playwright = sync_playwright().__enter__()
            viewer.browser = viewer.playwright.chromium.launch(headless=headless)
            viewer.context = viewer.browser.new_context()
        return self.function(viewer.context, *args, **kwargs)

close = viewer.close

def getstate(context):
    '获取当前网关状态'
    debug('Getstate start')
    page = context.new_page()
    try:
        page.goto('http://10.36.100.2:8181/', timeout=timeout)
    except Exception as exception:
        debug('Getstate: Network Err')
        return xstr* 'NetworkError' << exception
    url = page.url
    if 'success.jsp' in url:
        debug('Getstate: success.jsp')
        return 'Success'
    elif 'index.jsp' in url:
        debug('Getstate: index.jsp')
        return 'Login'
    else:
        debug(f'Getstate: Unknown URL ({page.url})')
        return xstr* 'UnknownURL' << url
getstate = viewer(getstate)

def login(context, username, password):
    '进行登录操作'
    debug('Login start')
    page = context.new_page()
    # 连接网站
    try:
        debug('Login: load http://10.36.100.2:8181/')
        page.goto('http://10.36.100.2:8181/', timeout=timeout)
    except Exception as exception:
        debug('Login: Network Err')
        return xstr* 'NetworkError' << exception

    # 查找输入框并输入用户名和密码
    debug('Login: fill #username')
    page.fill("#username", username)
    debug('Login: click #pwd_tip')
    page.click("#pwd_tip")
    debug('Login: fill #pwd')
    page.fill("#pwd", password)

    # 点击登录按钮
    debug('Login: click #loginLink')
    page.click("#loginLink")

    # 刷新结果
    page = context.new_page()
    debug('Login: load http://10.36.100.2:8181/')
    page.goto('http://10.36.100.2:8181/', timeout=timeout)
    if "success.jsp" in page.url:
        debug('Login: success.jsp')
        return 'Success'
    else:
        debug(f'Login: unknown ({page.url})')
        return 'Failed'
login = viewer(login)

def logout(context):
    '进行退出操作'
    debug('Logout start')
    page = context.new_page()
    # 连接网站
    try:
        debug('Logout: load http://10.36.100.2:8181/')
        page.goto('http://10.36.100.2:8181/', timeout=timeout)
    except Exception as exception:
        debug('Login: Network Err')
        return xstr* 'NetworkError' << exception

    # 点击退出按钮
    debug('Logout: click #toLogOut')
    page.click("#toLogOut")
    debug('Logout: click #sure')
    page.click("#sure")

    # 刷新结果
    page = context.new_page()
    debug('Logout: load http://10.36.100.2:8181/')
    page.goto('http://10.36.100.2:8181/', timeout=timeout)
    if "index.jsp" in page.url:
        debug('Login: index.jsp')
        return 'Success'
    else:
        debug(f'Login: unknown ({page.url})')
        return 'Failed'
logout = viewer(logout)