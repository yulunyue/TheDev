import json
import sys
import functools
import heapq
from typing import List, Dict, Tuple, Optional
import math
from collections import defaultdict, deque
import os
import random
from itertools import permutations
import bisect

null = None
true = True
false = False


def get_log(*args, **kw):
    pass


class logger:
    info = get_log
    map = get_log
    debug = get_log
    log_tree = get_log
    log_grid = get_log


class CT:
    MOD = (10**9) + 7
    inf = float("inf")
    MX = (10**5) + 1
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


class MockCf:
    dev = False

    type = ""
    execute = None

    def __init__(self, f=None, cases=None, src=None):
        if f is not None:
            self.execute = f
        self.cases = cases
        self.src_file = src
        self.inputs = []

    def get_cases(self) -> Dict:
        return self.cases

    def set_logger(self, log):
        self.logger: logger = log

    def set_inputs(self, inputs: str):
        self.inputs = [v for v in inputs.split("\n") if v]
        return self

    def input(self):
        if self.inputs:
            return self.inputs.pop(0)
        return input()

    def ii(self):
        return [int(v) for v in self.input().split(" ") if v]

    _o = None

    def output(self, s):
        if self._o is None:
            self._o = open("output.txt", "w")
        self._o.write(f"{s}\n")

    def exec(self):
        raise NotImplementedError

    def run(self, case_name=""):
        oj_run(self, case_name)

    cls_agent = None

    def main(self):
        raise NotImplemented

    def execute(self, inps: str):
        return self.set_inputs(inps).main()

    def init(self, **kw):
        raise NotImplementedError

    def set_layout(self, keys):
        self.layout_keys = keys
        return self

    def get_layout(self):
        from common.tool.export import get_dom_type, Row, Column

        n = len(self.layout_keys)
        m = math.ceil(math.sqrt(n))
        r = Row()

        for i, k in enumerate(self.layout_keys):
            if i % m == 0:
                c = Column()
                r.add(c)
            c.add(get_dom_type(k, getattr(self, k)))
        return r

    def log(self, **kw):
        self.logger.map(**kw)

    def get_agent(self, **kw):
        return


def oj_run(ins: "MockCf", case_name=None):
    from common.tool.export import PyFile
    from common.util.export import get_dev_log, logger, get_file_path_by_cls

    cases: dict = ins.get_cases()
    if case_name:
        cases = [[case_name, cases[case_name]]]
    else:
        cases = cases.items()
    for case_name, c in cases:
        exp = c.pop("result")
        ins.logger = get_dev_log(case_name)
        agent = ins.get_agent(**c)
        if agent is not None:
            methods, args, res = c["methods"][1:], c["args"][1:], [None]
            for i, method in enumerate(methods):
                u = getattr(agent, method)(*args[i])
                ins.log(f"{method} {args[i]}")
                res.append(u)
        else:
            res = ins.execute(**c)
        if res != exp:
            logger.info(f"FAILED {case_name} {exp}!={res}")
        else:
            logger.info(f"PASS {case_name} {exp}=={res}")
    src_file = ins.src_file
    if src_file is None:
        src_file = get_file_path_by_cls(ins.__class__)
    PyFile(src_file).compile_to_one_file()


def execute_by_thread(i: MockCf, case: dict):
    from common.util.export import ThreadRecord, hash_any_str

    result = case.pop("result")
    keys_pre = set(dir(i))
    i.init(**case)
    i.set_layout(set(dir(i)) - keys_pre)

    class T(ThreadRecord):
        def exec_main(self):
            return i.exec()

        def uk(self):
            return "".join(hash_any_str(getattr(i, key)) for key in i.layout_keys)

        def to_josn(self):
            ret = dict()
            for key in i.layout_keys:
                v = getattr(i, key)
                if hasattr(v, "to_json"):
                    ret[key] = v.to_json()
                else:
                    ret[key] = v
            return ret

    return dict(
        layout=i.get_layout(),
        records=T().execute().get_records(),
    )


MockCg = MockCf
