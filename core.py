import json
from random import randint
import requests

timeout = 1  # 连接超时

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

def getstate():
    '''获取当前网关状态'''
    session = requests.Session()
    session.trust_env = False
    try:
        data = session.get('http://10.36.100.2:8181/', timeout=timeout, headers={'Accept-Encoding':''}).text
    except:
        return 'NetworkError'
    if '登录成功' in data[:256]:
        return 'Connected'
    elif data.startswith("<script>top.self.location.href="):
        return xstr* 'Login' << data.split("'")[1]
    else:
        return xstr* 'Unknown' << data

def login(url, acc, pswd):
    '''进行登录操作'''
    session = requests.Session()
    session.trust_env = False
    loginurl = 'http://10.36.100.2:8181/eportal/InterFace.do?method=login'
    headers={
    'Accept':'*/*',
    'Accept-Encoding':'',
    'Accept-Language':'zh-CN',
    'Connection':'Keep-Alive',
    'Content-Length': '420',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent':f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{randint(70, 110)}.0.0.0',
    'Host': '10.36.100.2:8181',
    'Referer':url}
    queryString = url.split('?')[-1].replace('=', '%3D').replace('&', '%26')
    data = f'userId={acc}&password={pswd}'
    data += f'&service=&queryString={queryString}'
    data += '&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false'
    resp = session.post(loginurl, headers=headers, data=data, timeout=timeout)
    resp.encoding = 'utf-8'
    result = json.loads(resp.text)
    if result['result'] == 'success':
        return 'Success'
    else:
        return xstr* 'Fail' << result['message']

def logout():
    '''进行退出操作'''
    session = requests.Session()
    session.trust_env = False
    logouturl = 'http://10.36.100.2:8181/eportal/InterFace.do?method=logout'
    resp = session.get(logouturl, timeout=timeout)
    resp.encoding = 'utf-8'
    result = json.loads(resp.text)
    if result['result'] == 'success':
        return 'Success'
    else:
        return xstr* 'Fail' << result['message']