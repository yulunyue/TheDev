import json
from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from functools import lru_cache

import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


local_debug = sys.argv[-1] == 'test'
logs = ""


def log(*s):
    global logs
    if not local_debug or len(logs) >= 2048:
        return
    logs += " ".join([str(v) for v in s])+"\n"


class Solution(Encrypter):
    @classmethod
    def get_cases(cls):
        return [[
            ["Encrypter", "encrypt", "decrypt"],
            [[['a', 'b', 'c', 'd'], ["ei", "zf", "ei", "am"],
              ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]],
             ["abcd"], ["eizfeiam"]],
            [null, "eizfeiam", 2]
        ]]

    @classmethod
    def run(cls):
        global logs
        if not local_debug:
            return
        logs = ""
        for case in cls.get_cases():
            m, inp, es = case
            r = cls(*inp[0])
            log(m[0], *inp[0])
            flag = True
            for i in range(1, len(inp)):
                log(m[i], inp[i], es[i])
                e = getattr(r, m[i])(*inp[i])
                if not r.diff(e, es[i]):
                    print(logs, e, es[i])
                    flag = False
                    break
            if not flag:
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution.run()
