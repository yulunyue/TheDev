from common.util.export import File, get_log, uid, Module, get_function_info
from common.service.node import Node
from typing import List
import json
import os

logger = get_log("http")


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
            logger.exception(e)
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

    def load_module_str(self, key: str, modules: List[str]):
        if key and not os.path.isdir(key):
            raise Exception(key)
        if modules == "*":
            modules = os.listdir(key)
        path_key = key if key.startswith("/") else "/" + key
        for moudule_name in modules:
            m = Module().load_module(moudule_name, key, "Route")()
            moudule_name_key = moudule_name.replace(".", "/")
            for fun_name in dir(m):
                if fun_name.startswith("_"):
                    continue
                f = getattr(m, fun_name)
                fun_key = f"{path_key}/{moudule_name_key}/{fun_name}"
                if callable(f):
                    self.fun_map[fun_key] = f

    def load_module(self, cls):
        m = cls.Route()
        moudule_name_key = cls.__name__.replace(".", "/")
        for fun_name in dir(m):
            if fun_name.startswith("_"):
                continue
            f = getattr(m, fun_name)
            fun_key = f"/{moudule_name_key}/{fun_name}"
            if callable(f):
                self.fun_map[fun_key] = f
                logger.info(f"register {fun_key}")

    def load_modules(self, mds):
        for md in mds:
            if isinstance(md, str):
                self.load_module_str(md)
            else:
                self.load_module(md)

    def to_json(self):
        childs = []
        for k in self.fun_map:
            c = get_function_info(self.fun_map[k])
            childs.append(c.set_key(k).set_title(k))
        return dict(childs=childs)
