import os
import json
from typing import List


class File:
    def __init__(self, path: str) -> None:
        self.path = path
        self.dirs = path.split('/')
        self.name = self.dirs.pop()
        self.m_time = 0
        self.data = b''

    def get_m_time(self):
        return os.path.getmtime(self.path)

    def make_dir_if_not_exist(self):
        root_path = ""
        for p in self.dirs:
            root_path += p
            if root_path and not os.path.isdir(root_path):
                os.mkdir(root_path)
            root_path += "/"

    def write_file(self, data: str, encoding='utf-8'):
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data, indent=4, ensure_ascii=False)
        self.make_dir_if_not_exist()
        if isinstance(data, bytes):
            with open(self.path, 'wb') as f:
                f.write(data)
        else:
            with open(self.path, 'w', encoding=encoding) as f:
                f.write(data)

    def is_json_file(self):
        return self.path.endswith('.json')

    def read_data(self):
        with open(self.path, 'rb') as f:
            return f.read()

    def read_file(self, encoding='utf-8'):
        data = self.read_data()
        if self.is_json_file():
            return json.loads(data.decode(encoding))
        return data.decode(encoding)

    def read_fast_file(self):
        m_time = self.get_m_time()
        if self.m_time != m_time:
            self.data = self.read_file()
            self.m_time = self.m_time
        return self.data

    def exists(self):
        return os.path.exists(self.path)
    
    def list_dir(self):
        return [File(self.path+'/'+f) for f in os.listdir(self.path)]
    
    def dp_dir(self):
        ret:List[File]=[]
        for f in self.list_dir():
            if f.is_dir():
                ret.extend(f.dp_dir())
            else:
                ret.append(f)
        return ret
    
    def is_dir(self):
        return os.path.isdir(self.path)