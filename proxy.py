import winreg as reg
from log import debug, realtime

proxy_feature = True

proxy_state = 0
proxy_server = ''
key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

def getproxy():
    if not proxy_feature: return
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
    value = reg.QueryValueEx(reg_key, "ProxyEnable")[0]
    debug(f'Proxy State: {value}')
    return value

def getproxyserver():
    if not proxy_feature: return
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
    value =  reg.QueryValueEx(reg_key, "ProxyServer")[0]
    debug(f'Proxy Server: {value}')
    return value

def disable_proxy():
    if not proxy_feature: return
    global proxy_state, proxy_server
    proxy_state = getproxy()
    if proxy_state:
        debug('Disable Proxy')
        proxy_server = getproxyserver()
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, 0)
        reg.CloseKey(reg_key)

def restore_proxy():
    if not proxy_feature: return
    if proxy_state:
        debug('Enable Proxy')
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, proxy_state)
        reg.SetValueEx(reg_key, "ProxyServer", 0, reg.REG_SZ, proxy_server)
        reg.CloseKey(reg_key)

class NoProxy:
    def __enter__(self):
        disable_proxy()
    def __exit__(self, exc_type, exc_value, traceback):
        restore_proxy()
noproxy = NoProxy()