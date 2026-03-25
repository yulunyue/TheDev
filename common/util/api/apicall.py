from ..fp import File
from ..log import logger, get_log, get_dev_log
from ..module import get_function_info, Module
from ..tool import uid, json_dumps
from ..node import Node
from typing import List, Dict
import json
import os
from .apibase import ApiBase


class ApiCall:
    def __init__(self) -> None:
        self.fun_map = dict()
        self.mock_call = []

    def add_hock(self, call):
        self.mock_call.append(call)

    def call_app(self, path, params, env):
        if path not in self.fun_map:
            return dict(code=404, title=f"{path} not in {list(self.fun_map.keys())}")
        try:
            ret = self.fun_map[path](**params)
        except Exception as e:

            get_log("api").exception(e)
            import traceback

            traceback.print_exc()
            ret = dict(code=500, title=str(e))
        return json_dumps(ret)

    def call(self, path, param, env):
        ret = self.call_app(path, param, env)
        for mock_fun in self.mock_call:
            mock_fun(path, param, ret)
        return ret

    def register(self, key: str, fun):
        if key in self.fun_map:
            raise Exception(key, self.fun_map[key])
        self.fun_map[key] = fun
        logger.info(f"register {key} {fun.__name__}")

    def load_module(self, moudule_name_key, cls: ApiBase):
        m = cls()
        if hasattr(cls, "front_apis"):
            apis = cls.front_apis
        else:
            apis = [v for v in dir(m) if not v.startswith("_")]
        for fun_name in apis:
            f = getattr(m, fun_name)
            fun_key = f"{moudule_name_key}/{fun_name}"
            if callable(f):
                self.register(fun_key, f)

    def load_modules(self, mds: List[Dict]):
        for md in mds:
            for k, path in md["modules"].items():
                if k[0] == "#":
                    continue
                cl = Module().load_module_object(path, md["path"])
                self.load_module(k, cl)
