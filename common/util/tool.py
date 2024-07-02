import os
from typing import List
def os_system(s: str):
    ret = os.system(s)
    if ret != 0:
        raise Exception(s)


def make_dir_if_not_exist(paths: List[str]):
    root_path = ""
    # print(paths)
    for p in paths:
        root_path += p
        if root_path and not os.path.isdir(root_path):
            os.mkdir(root_path)
        root_path += "/"


def write_file(path: str, data: str, encoding='utf-8'):
    write_dir = path.split("/")[:-1]
    make_dir_if_not_exist(write_dir)
    if isinstance(data, bytes):
        with open(path, 'wb') as f:
            f.write(data)
    else:
        with open(path, 'w', encoding=encoding) as f:
            f.write(data)