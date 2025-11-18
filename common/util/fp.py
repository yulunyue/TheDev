import os
import json
from typing import List, Dict
import zipfile
import shutil
import io


def dump_default(v):
    return str(v)


def json_dump(oj):
    return json.dumps(oj, indent=4, ensure_ascii=False, default=dump_default)


class File:
    def __init__(self, path: str) -> None:
        self.path = path
        self.dirs = path.split("/")
        self.file_name = self.dirs.pop()
        names = self.file_name.split(".")
        self.name = names[0]
        self.type = names[-1]
        self.m_time = 0
        self.data = b""

    def parent(self):
        return File("/".join(self.dirs))

    def get_m_time(self):
        return os.path.getmtime(self.path)

    def child(self, name):
        return File(self.path + "/" + name)

    def make_dir_if_not_exist(self, is_dir=False):
        if self.exists():
            return self
        root_path = ""
        dirs = self.dirs[:]
        if is_dir:
            dirs.append(self.file_name)
        for p in dirs:
            root_path += p
            if root_path and not os.path.isdir(root_path):
                os.mkdir(root_path)
            root_path += "/"
        return self

    def write_file(self, data: str, encoding="utf-8"):
        if isinstance(data, dict) or isinstance(data, list):
            data = json_dump(data)
        self.make_dir_if_not_exist()
        if isinstance(data, bytes):
            with open(self.path, "wb") as f:
                f.write(data)
        else:
            if not isinstance(data, str):
                data = str(data)
            with open(self.path, "w", encoding=encoding) as f:
                f.write(data)
        return self

    def write_if_not_exists(self, data=""):
        if not self.exists():
            self.write_file(data)
        return self

    def is_json_file(self):
        return self.path.endswith(".json")

    def read_data(self):
        with open(self.path, "rb") as f:
            return f.read()

    def read_line(self):
        return self.read_data().decode("utf-8").replace("\r", "").split("\n")

    def read_file(self, encoding="utf-8"):
        data = self.read_data()
        if self.is_json_file():
            return json.loads(data.decode(encoding))
        elif self.file_name.endswith(".cfg") or self.file_name.endswith(".ini"):
            from configparser import ConfigParser

            config = ConfigParser()
            config.read(self.path)
            data = {}
            for section in config.sections():
                data[section] = {}
                for key, val in config.items(section):
                    data[section][key] = val
            return data
        return data.decode(encoding)

    _config = None

    def get(self, *keys, default_value=None):
        if self._config is None:
            self._config = self.read_file()
        tmp = self._config
        for k in keys:
            if k not in tmp:
                return default_value
            tmp = tmp[k]
        return tmp

    def read_fast_file(self):
        m_time = self.get_m_time()
        if self.m_time != m_time:
            self.data = self.read_file()
            self.m_time = self.m_time
        return self.data

    def exists(self):
        return os.path.exists(self.path)

    def list_dir(self, depth=1, with_dir=False, filter=None) -> List["File"]:
        if depth == 0:
            return []
        ret = []

        def append(f):
            if filter and not filter(f):
                return
            ret.append(f)

        for name in os.listdir(self.path):
            f = File(self.path + "/" + name)
            if f.is_dir():
                if with_dir:
                    append(f)
                ret.extend(f.list_dir(depth - 1))
            else:
                append(f)
        return ret

    def list_tree_file(self):
        return self.list_dir(-1)

    def is_dir(self):
        return os.path.isdir(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

    def py_module_path(self):
        return self.path.replace("/", ".").replace(".py", "")

    def dump_excel(self):
        import pandas

        ret = pandas.read_excel(self.path, sheet_name=None)
        sheets = ret.keys()
        ret = dict()
        for name in sheets:
            ret[name] = pandas.read_excel(self.path, sheet_name=name).to_dict()
        return ret

    def get_relative_path(self, path: str):
        if path.startswith("/"):
            return path
        path_prefix = self.path.split("/")
        p_idx = 0
        while p_idx < len(path) and path[p_idx] == ".":
            path_prefix.pop()
            p_idx += 1
        if p_idx == 0:
            return self.path + "/" + path
        return "/".join(path_prefix + path[p_idx:].split("/"))

    def dump(self):
        if self.type.startswith("xls"):
            return self.dump_excel()

    WITHE_FILE_HANDER = dict()

    def get_writer(self) -> io.TextIOWrapper:
        if self.path in self.WITHE_FILE_HANDER:
            return self.WITHE_FILE_HANDER[self.path]
        self.make_dir_if_not_exist()
        self.WITHE_FILE_HANDER[self.path] = open(self.path, "w", encoding="utf-8")
        return self.WITHE_FILE_HANDER[self.path]

    def zip(self):
        with zipfile.ZipFile(self.path + ".zip", "w", zipfile.ZIP_DEFLATED) as f:
            for c in self.list_tree_file():
                arc_name = os.path.relpath(c.path, self.path)
                f.write(c.path, arcname=arc_name)
        f.close()
        return self

    def unzip(self):
        output_dir = self.path.replace(".zip", "")
        with zipfile.ZipFile(self.path) as zf:
            for member in zf.namelist():
                zf.extract(member, path=output_dir)

    def replace(self, info: dict):
        data = self.read_file()
        for k, v in info.items():
            data = data.replace(k, v)
        self.write_file(data)
        return self

    def remove(self):
        if self.is_dir():
            shutil.rmtree(self.path)
        elif self.is_file():
            os.remove(self.path)
        return self

    def rename(self, src, dst):
        return File(self.path.replace(src, dst))


class Cache:
    def __init__(self, name):
        self.fp = File(f"data/cache/{name}.json")
        self.store = dict()
        if self.fp.exists():
            self.store.update(self.fp.read_file())

    def set(self, key, value):
        self.store[key] = value
        return self

    def get(self, key):
        return self.store[key]

    def exists(self, key):
        return key in self.store

    def save(self):
        self.fp.write_file(self.store)
        return self


CACHE: Dict[str, Cache] = dict()


def get_cache(name):
    if name not in CACHE:
        CACHE[name] = Cache(name)
    return CACHE[name]
