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


TheDevLoger = logger


class CT:
    MOD = (10**9) + 7
    inf = float("inf")
    MX = (10**5) + 1
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


class MockCf:
    dev = False

    logger = logger
    type = ""
    execute = None

    def __init__(self, f=None, cases=None, src=None):
        if self.execute is None:
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
        return ""

    def run(self, case_name=""):
        oj_run(self, case_name)

    def execute(self, inps: str):
        return self.set_inputs(inps).main()


def oj_run(ins: "MockCf", case_name=None):
    from common.tool.export import PyFile

    cases: dict = ins.get_cases()
    if case_name:
        cases = [[case_name, cases[case_name]]]
    else:
        cases = cases.items()
    for case_name, c in cases:
        exp = c.pop("result")
        ins.logger = get_dev_log(case_name)
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
    from common.util.export import ThreadRecord

    result = case.pop("result")

    class T(ThreadRecord):
        def exec_main(self):
            return i.execute(**case)

    return T().execute().get_records()


MockCg = MockCf
