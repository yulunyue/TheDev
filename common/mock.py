import json
import sys
import functools
import heapq
from typing import List, Dict
import math

try:
    from sortedcontainers import SortedDict, SortedList, SortedSet
except Exception as e:
    pass
from collections import defaultdict


def get_log(*args, **kw):
    pass


class logger:
    info = get_log
    map = get_log
    debug = get_log


class Constant:
    MOD = (10**9) + 7
    inf = float("inf")


class CgMock:
    msgs = []

    def input(self):
        r = input()
        self.msgs.append(r)
        return r

    def replay(self):
        pass

    def debug(self, **kw):
        debug_map = dict(inputs=self.msgs)
        debug_map.update(kw)
        print(json.dumps(debug_map), file=sys.stderr, flush=True)
        self.msgs.clear()


C = Constant()
