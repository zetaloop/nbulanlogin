import winreg as reg
from config import get

issaved = False

proxy_state = 0
proxy_server = ''
key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

def getproxy():
    if not get('disableproxy'): return
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
    value = reg.QueryValueEx(reg_key, "ProxyEnable")[0]
    return value

def getproxyserver():
    if not get('disableproxy'): return
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
    value =  reg.QueryValueEx(reg_key, "ProxyServer")[0]
    return value

def disable():
    if not get('disableproxy'): return
    global proxy_state, proxy_server, issaved
    proxy_state = getproxy()
    if proxy_state and not issaved:
        proxy_server = getproxyserver()
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, 0)
        reg.CloseKey(reg_key)
        issaved = True

def restore():
    if not get('disableproxy'): return
    global proxy_state, proxy_server, issaved
    if proxy_state and issaved:
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "ProxyEnable", 0, reg.REG_DWORD, proxy_state)
        reg.SetValueEx(reg_key, "ProxyServer", 0, reg.REG_SZ, proxy_server)
        reg.CloseKey(reg_key)
        issaved = False

class NoProxy:
    def __enter__(self):
        disable()
    def __exit__(self, exc_type, exc_value, traceback):
        restore()
noproxy = NoProxy()