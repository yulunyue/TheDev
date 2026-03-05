from common.util.export import MockCf, List
from sortedcontainers import SortedList
from common.algo.base.tree.tietree import TieNode
from common.algo.base.bin_util import to_2


class T(TieNode):
    idx = 0
    j = 0

    def update_pos(self, idx):
        if idx > self.idx:
            self.idx = idx

    def to_str(self):
        return f"{self.idx}"

    def q(self, s: List[int]):
        root = self
        u = 0
        for v in s:
            v1: T = root.get(1 - v)
            v2: T = root.get(v)
            if v1.idx >= T.j and v1.size:
                root = v1
                u = u * 2 + 1
            else:
                u = u * 2 + v
                root = v2
        return u


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[5, 4, 5, 6], k=2, result=7),
            case1=dict(nums=[5, 4, 5, 6], k=1, result=6),
        )

    def maxXor(self, nums: list[int], k: int) -> int:
        t = SortedList()
        T.j = x = 0
        mx = max(nums)
        n = mx.bit_length()
        s = T()
        s.add([0] * n)
        self.logger.info(s.show())
        for i, v in enumerate(nums):
            t.add(v)
            x ^= v
            y = s.q(to_2(x, n)[0])
            if y > mx:
                mx = y
            s.add(to_2(v, n)[0], i)
            while T.j < i and t[-1] - t[0] > k:
                t.remove(nums[T.j])
                x ^= nums[T.j]
                T.j += 1
            self.logger.map(x=bin(x), j=T.j, s=s.show())
        return mx

    execute = maxXor
