from common.util.export import MockCf, List
from common.algo.base.block import Block


class Bk(Block):
    def __init__(self, size):
        super().__init__(size)
        self.pos = [dict() for _ in range(self.n)]

    def update_area(self, l, r, v):
        self.pos[i]
        return super().update_area(l, r, v)

    def set_data(self, i, v):
        self.pos[v] = i
        return super().set_data(i, v)

    def find(self, r, target):
        for j in range(r):
            i = j // self.n
        return


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[2, 5, 4, 3], result=4),
            case1=dict(nums=[3, 2, 2, 5, 4], result=5),
        )

    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        bs = Block(n)
        last_idx = dict()
        for i, v in enumerate(nums):
            u = 1 if v % 2 else -1
            bs.update(i, n - 1, u)
            if v in last_idx:
                for j in range(last_idx[v], i):
                    bs.update(j, i, -u)

            last_idx[v] = i

    execute = longestBalanced
