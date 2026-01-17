from common.util.export import (
    File,
    get_log,
    uid,
    Module,
    get_function_info,
    get_dev_log,
    logger,
)
from .node import Node
from typing import List
import json
import os


class ApiCall:
    def __init__(self) -> None:
        self.fun_map = dict()
        self.mock_call = []

    def add_hock(self, call):
        self.mock_call.append(call)

    def call_app(self, path, params):
        if path not in self.fun_map:
            return dict(code=404, title=f"{path} not in {list(self.fun_map.keys())}")
        try:
            ret = self.fun_map[path](**params)
        except Exception as e:

            get_log("api").exception(e)
            import traceback

            traceback.print_exc()
            ret = dict(code=500, title=str(e))
        if isinstance(ret, Node):
            return json.dumps(ret.to_json(), ensure_ascii=False)
        return ret

    def call(self, path, param):
        ret = self.call_app(path, param)
        for mock_fun in self.mock_call:
            mock_fun(path, param, ret)
        return ret

    def load_module_str(self, path: str, modules: List[str], enable=True):
        if not enable:
            return
        if not os.path.isdir(path):
            raise Exception(path)
        return [
            Module().load_module_object(moudule_name, path) for moudule_name in modules
        ]

    def register(self, key: str, fun):
        keys = key.split("/")[-4:]
        if keys[0]:
            keys[0] = ""
        key = "/".join(keys)
        if key in self.fun_map:
            raise Exception(key, self.fun_map[key])
        self.fun_map[key] = fun
        logger.info(f"register {key} {fun.__name__}")

    def load_module(self, cls):
        m = cls()

        moudule_name_key = cls.API_ROUTE
        for fun_name in dir(m):
            if fun_name.startswith("_"):
                continue
            f = getattr(m, fun_name)
            fun_key = f"/{moudule_name_key}/{fun_name}"
            if callable(f):
                self.register(fun_key, f)

    def load_modules(self, mds):
        for md in mds:
            if isinstance(md, dict):
                self.load_modules(self.load_module_str(**md))
            else:
                self.load_module(md)

    def to_json(self):
        childs = []
        for k in sorted(self.fun_map.keys()):
            childs.append(dict(key=k))
        return dict(childs=childs)
