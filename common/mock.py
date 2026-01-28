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


TheDevLoger = logger


class CT:
    MOD = (10**9) + 7
    inf = float("inf")
    MX = (10**5) + 1
    min = lambda a, b: a if a < b else b
    max = lambda a, b: a if a > b else b


class MockCf:
    dev = False
    inputs = None
    logger = logger
    type = ""
    execute = None

    def __init__(self, f=None, cases=None, src=None):
        if self.execute is None:
            self.execute = f
        self.cases = cases
        self.src_file = src

    def get_cases(self):
        return self.cases

    def set_logger(self, log):
        self.logger: logger = log

    def set_inputs(self, inputs: str):
        self.inputs = [v for v in inputs.split("\n") if v]
        return self

    def input(self):
        if self.inputs:
            return self.inputs.pop(0)
        self.inputs.append(input())
        return self.inputs[-1]

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
        if os.path.exists("common/third_service/oj.py"):
            from common.third_service.oj import oj_run

            oj_run(self, case_name)
        else:
            self.exec()

    def execute(self, inps: str):
        return self.set_inputs(inps).main()


MockCg = MockCf
