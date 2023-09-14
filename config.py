import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')

default = {
    'username': '',
    'password': '',
    'autostart': False,
    'autologin': False,
    'disableproxy': False,
}

def get(name):
    if name not in default:
        raise NameError
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, dict):
                if name in data:
                    value = data[name]
                else:
                    value =  default[name]
            else:
                raise ValueError('config.json error!')
    else:
        value = default[name]
    return value

def set(name, value):
    if name not in default:
        raise NameError
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}
    data[name] = value
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)