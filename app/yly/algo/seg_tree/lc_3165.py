from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.algo.manage import SolutionBase, rs, bs, gs, ah
except Exception as e:
    print(f'{e}', file=sys.stderr)

    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def watch(self, *args, **kwags):
            pass


inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class SegTreeNode:
    '''
                          1[0-6]
            2[0-3]                      3[4-6]
     4[0-1]        5[2-3]         6[4-5]         7[6-6]
8[0-0]  9[1-1] 10[2-2] 11[3-3] 12[4-4] 13[5-5]
    '''

    def __init__(self, l, r, idx=1, default_value=0) -> None:
        self.idx = idx
        self.l = l
        self.r = r
        self.m = (l+r)//2
        self.default_value = default_value
        self.todo = 0
        self.f00 = self.f01 = self.f10 = self.fmx = 0
        self._left: SegTreeNode = None
        self._right: SegTreeNode = None

    @property
    def left(self):
        if not self._left:
            self._left = SegTreeNode(
                self.l, self.m, self.idx*2, self.default_value)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = SegTreeNode(
                self.m+1, self.r, self.idx*2+1, self.default_value)
        return self._right

    def query(self, l, r):
        if l <= self.l and self.r <= r:
            return self.fmx
        self.down()
        res = 0
        if self.m < r:
            res += self.right.query(l, r)
        if self.m >= l:
            res += self.left.query(l, r)
        return res

    def update(self, l, r, value):
        if l <= self.l and self.r <= r:
            self.do(value)
            return
        self.down()
        if self.m < r:
            self.right.update(l, r, value)
        if self.m >= l:
            self.left.update(l, r, value)
        self.up()

    def do(self, v):
        self.fmx = max(v, 0)

    def down(self):
        if self.todo:
            self.left.do(self.todo)
            self.right.do(self.todo)
            self.todo = 0

    def up(self):
        self.f00 = max(self.left.f00+self.right.f10,
                       self.left.f01+self.right.f00)
        self.f01 = max(self.left.f00+self.right.fmx,
                       self.left.f01+self.right.f01)
        self.f10 = max(self.left.f10+self.right.f10,
                       self.left.fmx+self.right.f00)
        self.fmx = max(self.left.f10+self.right.fmx,
                       self.left.fmx+self.right.f01)

    def get_title(self):
        sr = rs(f"{self.l}:{self.r}", Solution.arr[self.l:self.r])
        return '</br>'.join([
            f"{sr}",
            f"{rs('f00',self.f00)}, {rs('f10',self.f10)}",
            f"{rs('f01',self.f01)},  {rs('fmx',self.fmx)}"
        ])

    def algo_view(self):
        ret = dict(
            title=self.get_title(),
            childs=[],
        )
        if self._left:
            ret['childs'].append(self._left.algo_view())
        if self._right:
            ret['childs'].append(self._right.algo_view())
        return ret

    def hex_str(self):
        ret = [f'{self.f00}{self.f01}{self.f10}{self.fmx}']
        if self._left:
            ret.append(self._left.hex_str())
        if self._right:
            ret.append(self._right.hex_str())
        return "".join(ret)


class Solution(SolutionBase):
    uri = 'https://leetcode.cn/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/description/'
    arr = []
    has_view = True

    def get_cases(self):
        return [
            dict(nums=[4, 5, 10, 12, 15, 6], queries=[
                 [1, 3], [2, 7]], result=21),
            dict(nums=[3, 5, 9], queries=[[1, -2], [0, -3]], result=21)
        ]

    def init(self, nums: List[int], queries: List[List[int]], result=0) -> int:
        self.result = result
        Solution.arr = nums
        self.queries = queries
        self.n = len(Solution.arr)
        self.t = SegTreeNode(0, self.n-1)
        self.ans = 0
        for i, v in enumerate(Solution.arr):
            self.t.update(i, i, v)

    def hex_str(self):
        return ''

    def algo_view(self):
        ret = '<br>'.join([
            f'lc3165_不包含相邻元素的子序列的最大和',
            f'{ah("链接",self.uri)}; 解法: 线段树',
            f"",
            f'每个节点存储4个信息',
            f'1. f00: 区间最左边和最右边的数都不选的情况下的最大值',
            f'2. f01: 最左边的数不选的最大值',
            f'3. f10: 最右边的数不选的最大值',
            f'4. fmx: 区间最大值',
            "",
            f'所以有: ',
            f'f00 = max(left.f00+right.f10, left.f01+right.f00)',
            f'f01 = max(left.f00+right.fmx, left.f01+right.f01)',
            f'f10 = max(left.f10+right.f10, left.fmx+right.f00)',
            f'fmx = max(left.f10+right.fmx, left.fmx+right.f01)',

        ])
        return dict(title=ret)

    def get_watch(self):
        return [
            self.watch('text', self.hex_str, self.algo_view),
            [

                [
                    self.watch(
                        'text',
                        lambda: f'{Solution.arr+self.queries}',
                        lambda: dict(title=bs("输入序列", Solution.arr)+" "+bs("查询列表", self.queries))),
                    self.watch(
                        'text',
                        lambda: f'{self.result}{self.ans}',
                        lambda:  dict(
                            title=f'{bs("期望结果",self.result)} {bs("当前结果",self.ans)}')
                    ),
                ],
                self.watch("tree", self.t.hex_str, self.t.algo_view, 1),
            ],

        ]

    def execute(self):
        while self.queries:
            idx, value = self.queries.pop(0)
            Solution.arr[idx] = value
            self.t.update(idx, idx, value)
            self.ans = self.ans+self.t.query(0, self.n-1)
        return self.ans % M

    def maximumSumSubsequence(self, *args, **kg):
        self.init(*args, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
