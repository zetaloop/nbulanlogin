import os
import json
from log import debug, realtime

config_path = os.path.join(os.path.dirname(__file__), 'config.json')

default = {
    'username': '',
    'password': '',
    'startatboot': True,
    'headless': False,
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
                    debug(f'Read config ({name}): {value}')
                else:
                    value =  default[name]
                    debug(f'Read default ({name}): {value}')
            else:
                raise ValueError('config.json error!')
    else:
        value = default[name]
        debug(f'Read default ({name}): {value}')
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
    debug(f'Write config: {data}')
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)