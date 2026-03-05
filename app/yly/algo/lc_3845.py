from common.util.export import MockCf, List, deque
from sortedcontainers import SortedList
from common.algo.base.tree.tietree import TieNode
from common.algo.base.bin_util import to_2


class T(TieNode):
    j = 0

    def load(self):
        self.childs = [None, None]
        return self

    def to_str(self):
        return f"{self.size}"

    def q(self, s: List[int]):
        root = self
        u = 0
        for v in s:
            v1: T = root.get(1 - v)
            root: T = root.get(v)
            k = 0
            if v1.size:
                root, k = v1, 1
            u = u * 2 + k
        return u


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case1=dict(nums=[5, 4, 5, 6], k=2, result=7),
            case0=dict(nums=[5, 4, 5, 6], k=1, result=6),
        )

    def maxXor(self, nums: list[int], k: int) -> int:
        mnt, mxt = deque(), deque()
        u = 0
        mx = max(nums)
        T.j = 0
        n = mx.bit_length()
        x = [[0] * n]
        for v in nums:
            u ^= v
            x.append(to_2(u, n)[0])
        s = T()
        # self.logger.map(x=x, k=k)
        for i, v in enumerate(nums):
            while mnt and nums[mnt[-1]] < v:
                mnt.pop()
            mnt.append(i)
            s.add(x[i])
            while T.j < i and t[-1] - t[0] > k:
                t.remove(nums[T.j])
                s.remove(x[T.j])
                T.j += 1
            y = s.q(x[i + 1])
            if y > mx:
                mx = y
            # self.logger.map(x=x[i + 1], y=y, j=T.j, s=s.show())
        return mx

    execute = maxXor
