from common.tool.thread_util import run_watch_fun
from common.service.http import Node, http_test
from typing import List, Dict, Optional
import bisect
from common.util.module import Module
from common.util.log import get_log
from common.util.tool import uid

logger = get_log("algo")
from common.util.fp import File
from collections import defaultdict
import functools
from common.third_util.cg_util import CodingGame
import heapq
import os
import time
import math
import sys
import json
import numpy as np

sys.setrecursionlimit(10**5 + 1)
import bisect

inf, MOD, null, true, false = float("inf"), (10**9) + 7, None, True, False
WRITE_PATH = "data/algo/run.py"


def gen_file():
    Module().megre_to_one(
        sys.argv[0],
        WRITE_PATH,
        mock_map={"common/algo/manage.py": "app/yly/algo/base.py"},
        prefix=["common", "app"],
    )


CHANGE_STORE = dict()


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left: TreeNode = None
        self.right: TreeNode = None

    @staticmethod
    def load_from_lc_array(array):
        ret = [None] + [TreeNode(v) for v in array]
        for v in range(2, len(ret)):
            if ret[v].val is None:
                continue
            if v % 2 == 0:
                ret[v // 2].left = ret[v]
            else:
                ret[v // 2].right = ret[v]
        return ret[1]


def bp(title, value, key=""):
    return wc(title, key, value, "blue")


def wc(title, key, v, sp="p"):
    v = str(v)
    k = f"{title}_{key}"
    # font-size:28px
    return dict(key=k, title=title, value=v, type="p")


class ViewEnum:
    graph = "graph"
    string = "string"


class View(ViewEnum):
    def __init__(self, *args, key="", type=ViewEnum.string, size=1, **kwargs) -> None:
        self.key = key or uid("view")
        self.size = size
        self.set_type(type)
        self.childs: List[View] = list(args)
        self.var = None

    def set_type(self, tp):
        if not hasattr(ViewEnum, tp):
            raise Exception(tp)
        self.type = tp
        return self

    def hex_str(self):
        node = getattr(self.ins, self.key, None)
        return str(node)

    def set_ins(self, ins):
        self.ins = ins
        self.var = getattr(self.ins, self.key, None)
        if hasattr(self.var, "VIEW_TYPE"):
            self.set_type(getattr(self.var, "VIEW_TYPE"))
        return self

    def view(self):
        node = getattr(self.ins, self.key)
        return dict(data=bp(self.key, str(node), "self"), type=self.type)

    def dump_layout(self):
        ret = dict(
            size=self.size,
            key=self.key,
            type=self.type,
            childs=[v.dump_layout() for v in self.childs],
        )
        return ret


def fmax(a, b, *args):
    return a if a > b else b


def fmin(a, b, *args):
    return a if a < b else b


class SolutionBase:
    uri = ""
    log_mode = "test"
    _logs = []
    _has_view = False
    name = "solution"
    _DEV = True
    _tags = []
    _watch_var: List[View] = None
    log_str = "log"
    game_id = ""
    results = []

    def get_cases(self):
        return []

    def execute(self, *args, **kw):
        self.exec()
        return "\n".join(self.results)

    def str_util(self, v):
        return str(v)

    def log(self, *args, vars=None):
        if vars is not None:
            fs = s.split(",")
            s = "; ".join(
                [
                    f"{k}:{vars.get(k) if isinstance(vars,dict) else getattr(vars,k)}"
                    for k in fs
                ]
            )
        else:
            s = " ".join([self.str_util(a) for a in args])
        self.log_str = s
        if self.log_mode == "debug":
            logger.info(s)
        else:
            self._logs.append(self.log_str)

    def pre(self, input="", result=None, record_name=None, **kwargs):
        if "codingame" in self.uri:
            record_name = record_name or self.name
            data: dict = File(f"data/log/cg/{record_name}.json").read_file()
            kwargs["stderr"] = []
            kwargs["stdout"] = []
            for v in data["frames"]:
                if "stderr" in v:
                    kwargs["stderr"].append(json.loads(v["stderr"]))
                if "stdout" in v:
                    kwargs["stdout"].append(v["stdout"].split("\n")[0])
            kwargs.update(data.get("config", {}))
        self.lines = [v for v in input.split("\n") if v]
        return kwargs

    def exec(self):
        pass

    def run(self):
        exec_names = sys.argv[1:]
        gen_file()
        if exec_names and exec_names[0] == "view_web":
            return self.view_web()
        if exec_names and exec_names[0] == "submit":
            return self.submit()
        self.test([getattr(self, v) for v in exec_names[0].split(",")])
        self.flush_log()
        self.finish()

    def finish(self):
        pass

    agentsIds = None

    def submit(self):
        if "codingame" in self.uri:
            ret = CodingGame(self.name).pk(WRITE_PATH, self.game_id, self.agentsIds)
            File(f"data/log/cg/{self.name}.json").write_file(ret)
        else:
            raise Exception(self.uri)

    def test(self, func):
        if self.uri.startswith("lc_cls"):
            return self.run_cls()
        cases = self.get_cases()
        self.load()
        for fn in func:
            results = []
            for i, case in enumerate(cases):
                self.ep = case.get("result")
                self.results = []
                a = time.time()
                self.log(f"begin {self.name}-{fn.__name__}")
                self.log(f"case: {case}; except: {self.ep}")
                case = self.pre(**case)
                self.init(**case)
                if fn.__name__ == "execute":
                    try:
                        r = fn(**case)
                    except:
                        import traceback

                        traceback.print_exc()
                        r = None
                else:
                    r = fn(**case)
                results.append(r)
                if r is None:
                    r = "\n".join(self.results)
                self.log(
                    f"finish {self.name}-{fn.__name__}; result:\n{r}\nuse_time: {time.time()-a}"
                )
                if self.ep is not None and not self.diff(r, self.ep):
                    self.flush_log()
                    break
                if self.ep is not None:
                    self._logs = []
            self.run_finish(results)
        self.flush_log()
        logger.info(f"TEST_FINISH:{len(cases)}")

    def run_finish(self, results):
        pass

    def load(self):
        pass

    def error(self, *args):
        pass

    def output(self, s):
        self.results.append(str(s))

    def input(self) -> str:
        while self.lines and not self.lines[0]:
            self.lines.pop(0)
        if self.lines:
            return self.lines.pop(0)

    def i1(self):
        s = self.input()
        if s is None:
            return
        return int(s)

    def il(self):
        return [int(v) for v in self.input().split(" ") if v]

    def flush_log(self):
        if self._logs:
            logger.info("\n" + "\n".join(self._logs))
            self._logs.clear()

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return str(a) == str(b)

    def init(self, *args, **kwargs):
        pass

    def record(self):
        childs = {}
        flag = False

        for var in self._watch_var:
            key2, s2 = var.key + "_algo", var.hex_str() if var.hex_str else ""
            if CHANGE_STORE.get(key2) != s2:
                flag = True
                # logger.info(f'{key2}:{CHANGE_STORE.get(key2)},{s2}')
                CHANGE_STORE[key2] = s2
            childs[var.key] = var.view()
        if flag:
            return childs

    def get_view(self) -> View:
        return None

    _main_view: View = None

    def main_view(self) -> View:
        if self._main_view is None:
            self._main_view = self.get_view()
            self._watch_var = []

            def dfs(p: View):
                if not p.childs:
                    self._watch_var.append(p.set_ins(self))
                for c in p.childs:
                    dfs(c)

            dfs(self._main_view)
        return self._main_view

    def view_web(self):
        ret = self.view()
        path = f"data/algo/{self.name}/record.json"
        File(path).write_file(ret)
        logger.info(path)

    def view(self, case=None):
        if case is None:
            case = self.get_cases()[0]
        CHANGE_STORE.clear()
        self.pre(**case)
        self.init(**case)
        view = self.main_view()
        record, msg = run_watch_fun(self.execute, self.record)
        if msg:
            raise Exception(msg)
        return dict(
            layout=view.dump_layout(),
            record=record,
            msg=msg,
        )

    @classmethod
    def run_cls(cls):
        gen_file()
        for case in cls.get_cases(cls):
            c = cls(*case["params"][0])
            method, param, result = case["methods"], case["params"], case["result"]
            c.init()
            c._logs.clear()
            flag = False
            c.log(f"{method} {param} {result}")
            for i in range(1, len(method)):
                e = getattr(c, method[i])(*param[i])
                c.log(f"{method[i]} {param[i]} {e}")
                if e != result[i]:
                    c.log(f"ans:{result[i]}")
                    flag = True
                    break
            if flag:
                break
            c._logs.clear()
        cls.flush_log(cls)


PATH = "app/yly/algo"
TMP_PATH = "data/algo/main.py"


def get_md(moudle_name):
    try:
        return Module().load_module(moudle_name, fun_name="Solution")()
    except Exception as e:
        logger.error(e)


Solution = SolutionBase


class Route:
    def query(self, **kwargs):
        ret = Node(value=PATH)
        for fp in File(PATH).dp_dir():
            if not fp.path.endswith(".py"):
                continue
            module_name = fp.py_module_path()
            title = module_name.split(".")[-1]
            fc: SolutionBase = get_md(module_name)
            if fc is None or not getattr(fc, "_has_view", None):
                continue
            ret.add_child(
                key=module_name,
                title=title,
                value=fp.read_file(),
                data=dict(cases=fc.get_cases()),
            )
        return ret.to_json()

    def execute(self, content, case):
        if isinstance(case, str):
            case = json.loads(case)
        fp = File(TMP_PATH).write_file(content)
        module_name = fp.py_module_path()
        f: SolutionBase = get_md(module_name)
        _, ret, msg = f.view(case)
        # if msg:
        #     raise Exception(msg)
        return ret
