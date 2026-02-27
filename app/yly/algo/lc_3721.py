from common.util.export import MockCf, List, TheDevLoger
from common.algo.base.block import Block


class Bk(Block):
    def __init__(self, size, logger):
        super().__init__(size)
        self.pos = [dict() for _ in range(self.n)]
        self.logger: TheDevLoger = logger

    def update(self, l, r, v):
        self.logger.map(l=l, r=r, v=v)
        return super().update(l, r, v)

    def set_datas(self, i, l, r, v):
        self.pos[i] = dict()
        return super().set_datas(i, l, r, v)

    def set_data(self, i, v):
        self.pos[v] = i
        return super().set_data(i, v)

    def find(self, r, t):
        if t == 0:
            return -1
        i = j = 0
        while j + self.n < r:
            i += 1
            if t in self.pos[i]:
                return self.pos[i][t]
            j += self.n
        while j < r:
            if self.get(j) == t:
                return j
            j += 1
        return


class Solution(MockCf):
    def get_cases(self):
        return dict(
            # case0=dict(nums=[2, 5, 4, 3], result=4),
            case1=dict(nums=[3, 2, 2, 5, 4], result=5),
        )

    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        bs, ans = Bk(n, self.logger), 0
        last_idx = dict()
        self.logger.info(nums)
        for i, v in enumerate(nums):
            u = 1 if v % 2 else -1
            bs.update(i, n - 1, u)
            if v in last_idx:
                bs.update(last_idx[v], i, -u)
            t = bs.get(i)
            j = bs.find(i - ans, t)
            if j is not None:
                ans = max(i - j, ans)
            last_idx[v] = i
            self.logger.map(i=i, j=j, v=v, ans=ans, todo=bs.todo, data=bs.data)
        return ans

    execute = longestBalanced
