import os
import json
from typing import List, Dict
import zipfile
import shutil
import io
from .tool import time_format, json_dumps
from .str_util import StrUtil


class File:
    def __init__(self, path: str) -> None:
        if not isinstance(path, str):
            raise Exception(path)
        self.path = path.replace("\\", "/")
        self.dirs = self.path.split("/")
        self.name = self.file_name = self.dirs.pop()
        self.type = ""
        names = self.file_name.split(".")
        if len(names) > 1:
            self.type = names.pop()
            self.name = ".".join(names)
        self.m_time = 0
        self.data = b""

    FILES: Dict[str, "File"] = dict()

    @classmethod
    def new(cls, path):
        if path not in File.FILES:
            File.FILES[path] = File(path)
            from .log import logger

            # logger.info(File.FILES[path])
        return File.FILES[path]

    def get_size(self):
        return os.path.getsize(self.path)

    def parent(self):
        dirs = self.get_abs_path().split("/")
        dirs.pop()
        return File("/".join(dirs))

    def get_m_time(self):
        return os.path.getmtime(self.path)

    def get_m_time_str(self):
        return time_format(self.get_m_time())

    def child(self, *args):
        args = [self.path] + list(args)
        return File("/".join(args))

    def get_abs_path(self):
        if ":" in self.path:
            return self.path
        cwd = os.getcwd().replace("\\", "/")
        if self.path.startswith("/"):
            if os.name == "nt":
                return cwd[:2] + self.path
            return self.path
        return cwd + "/" + self.path

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
            data = json_dumps(data, indent=2)
        self.make_dir_if_not_exist()
        if isinstance(data, bytes):
            with open(self.path, "wb") as f:
                f.write(data)
        else:
            if not isinstance(data, str):
                data = str(data)
            with open(
                self.path, "w", newline="\n", encoding=encoding
            ) as f:  # newline="" 可以写LF 而不是CRLF \n 而不是 \r\n
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
        return self.read_data().decode("utf-8").replace("\r\n", "\n").split("\n")

    def copy_to(self, dst: "File", over_write=False):
        if isinstance(dst, str):
            dst = File(dst)
        if dst.exists() and not over_write:
            return dst
        if self.is_file():
            dst.write_file(self.read_data())
        elif self.is_dir():
            shutil.copy(self.path, dst.path)
        else:
            raise Exception(self)
        return dst

    def move_to(self, dst):
        self.copy_to(dst)
        self.remove()
        return dst

    def read_file(self, encoding="utf-8"):
        data = self.read_data().replace(b"\r", b"")
        if self.is_json_file():
            try:
                return json.loads(data.decode(encoding))
            except Exception as e:
                raise Exception(self, e)
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
        elif self.file_name.endswith(".toml"):
            try:
                import tomllib

                return tomllib.loads(data.decode(encoding))
            except:
                import toml

                return toml.load(self.path)
        return data.decode(encoding, errors="replace")

    _config = None

    def get_config(self):
        if self._config is None:
            self._config = dict()
            if self.exists():
                data = self.read_file()
                self._config.update(data)
        return self._config

    def get(self, *keys, default_value=None):
        tmp = self.get_config()
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
        if os.path.islink(self.path):
            return True
        return os.path.exists(self.path)

    def list_dir(
        self, depth=1, with_dir=False, mathchs=None, ignores=None
    ) -> List["File"]:
        if depth == 0:
            return []
        ret = []

        def check(path: str):

            return StrUtil().set_ignores(ignores).set_matchs(mathchs).match(path)

        for name in os.listdir(self.path):
            f = File(self.path + "/" + name)
            if f.is_dir():
                if with_dir:
                    ret.append(f)
                ret.extend(
                    f.list_dir(
                        depth - 1, with_dir=with_dir, mathchs=mathchs, ignores=ignores
                    )
                )
            elif check(f.path):
                ret.append(f)
        return ret

    def list_tree_file(self, with_dir=False):
        return self.list_dir(-1, with_dir=with_dir)

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

    def get_writer(self, mode="wb") -> io.TextIOWrapper:
        if self.path in self.WITHE_FILE_HANDER:
            return self.WITHE_FILE_HANDER[self.path]
        self.make_dir_if_not_exist()
        self.WITHE_FILE_HANDER[self.path] = open(self.path, mode)
        return self.WITHE_FILE_HANDER[self.path]

    def get_bin_writer(self) -> io.TextIOWrapper:
        self.make_dir_if_not_exist()
        return open(self.path, "wb")

    def zip(self, dst=None, targets=None, ignores=None):
        if dst is None:
            dst = self.path + ".zip"
        dst_file = File(dst).remove()
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as f:
            if targets is None:
                targets = self.list_tree_file()
            for c in targets:
                if isinstance(c, str):
                    local_path, arc_name, c = self.path + "/" + c, c, self.child(c)
                if c.is_file():
                    local_path, arc_name = c.path, os.path.relpath(c.path, self.path)
                    f.write(local_path, arcname=arc_name)
                else:
                    for d in c.list_dir(ignores=ignores):
                        local_path, arc_name = d.path, os.path.relpath(
                            d.path, self.path
                        )
                        f.write(local_path, arcname=arc_name)

        return dst_file

    def unzip(self, dst=None):
        if dst is None:
            dst = self.path.replace(".zip", "")
        if isinstance(dst, str):
            dst = File(dst)
        with zipfile.ZipFile(self.path) as zf:
            for member in zf.namelist():
                zf.extract(member, path=dst.path)
        return dst

    def replace(self, info: dict):
        data = self.read_file()
        for k, v in info.items():
            data = data.replace(k, v)
        self.write_file(data)
        return self

    def remove(self):
        if not self.exists():
            return self
        if self.is_dir():
            shutil.rmtree(self.path)
        elif self.is_file():
            os.remove(self.path)
        return self

    def rename(self, src, dst):
        return File(self.path.replace(src, dst))

    def __repr__(self):
        return f"[File: {self.get_abs_path()} ; EXIST:{self.exists()}]"
