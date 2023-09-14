level = 1  # 0 release, 1 debug, 2 realtime

def debug(obj, *args, **kwargs):
    if level >= 1:
        print(f'[debug] {obj}', *args, **kwargs)

def realtime(obj, *args, **kwargs):
    if level >= 2:
        print(f'[realtime] {obj}', *args, **kwargs)