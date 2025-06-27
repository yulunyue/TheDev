from common.util.export import List, defaultdict, bisect, logger
from common.algo.base.math_util import prime_flags
from common.algo.base.segtree import SegTreeNode

P = prime_flags((10**5) + 1)


class T(SegTreeNode):
    def do(self, v):
        # self.todo += v
        self.value = v

    def merge(self, l, r):
        # return max(l, r)
        return l + r


class Solution:
    def get_cases(self):
        return [
            dict(nums=[2, 1, 4], queries=[[0, 1]]),
            dict(nums=[2, 1, 3, 1, 2], queries=[[1, 2], [3, 3]], result=[3, 4]),
        ]

    def maximumCount(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        root = T().set_range(0, n - 1)
        st = defaultdict(list)
        self.sum_all = 0
        ans = []

        def add(idx, f, flag=0):
            if not P[f]:
                return
            j = bisect.bisect_left(st[f], f)
            logger.map(f=f, j=j, stf=st[f])
            if len(st[f]) >= 2:
                root.update(st[f][0], st[f][-1], -1)
            if len(st[f]) == flag:
                self.sum_all += -1 if flag == 1 else 1
            if flag == 1:
                st[f].pop(j)
            else:
                st[f].insert(j, idx)
            if len(st[f]) >= 2:
                root.update(st[f][0], st[f][-1], 1)

        for i, v in enumerate(nums):
            add(i, v)

        for idx, v in queries:
            add(idx, nums[idx], 1)
            add(idx, v)
            nums[idx] = v
            ans.append(self.sum_all + root.query(0, n - 1))
     
        return ans
