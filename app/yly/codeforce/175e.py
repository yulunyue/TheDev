

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq


def case_load(sl):
    return dict(
        n=int(sl[0]),
        vids=[list(map(int, v.split(' '))) for v in sl[1:-1]],
        result=int(sl[-1])
    )


try:
    from app.yly.manage import SolutionBase
    SolutionBase.case_load = case_load
except:
    class SolutionBase:

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            sl = [input()]
            for _ in range(int(sl[0])):
                sl.append(input())
            sl.append("")
            print(self.execute(**case_load(sl)))

inf = float("inf")


class Solution(SolutionBase):
    uri = ""
    gameid = ''

    def get_cases(self):
        return [
            '''
6
0
0
1 2 1
2 1 5 2 2
1 1 2
1 3 4
30
''',
        ]

    def execute(self, n, vids):
        ans = 0
        p = [None for _ in range(n)]

        for cid, ids in enumerate(vids):
            for i in range(1, len(ids), 2):
                p[ids[i]] = [cid, ids[i+1]]
        self.log(p)


if __name__ == '__main__':
    Solution().run()
