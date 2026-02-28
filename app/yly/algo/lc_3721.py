from common.util.export import MockCf, List, TheDevLoger
from common.algo.base.block import Block


class Bk(Block):
    def __init__(self, size, logger):
        super().__init__(size)
        self.pos = [dict() for _ in range(self.n)]
        self.logger: TheDevLoger = logger

    def update(self, l, r, v):
        super().update(l, r, v)
        # self.logger.map(
        #     l=l,
        #     r=r,
        #     v=v,
        #     d=self.get_data(),
        #     p=self.get_pos(),
        #     data=self.data,
        #     todo=self.todo,
        #     pos=self.pos,
        # )

    def set_datas(self, i, l, r, v):
        super().set_datas(i, l, r, v)
        m = self.n * i
        for j in range(self.n - 1, -1, -1):
            self.pos[i][self.data[i][j]] = m + j

    def get_pos(self):
        ans = dict()
        for i in range(self.size):
            v = self.get(i)
            if v not in ans:
                ans[v] = i
        return ans

    def find(self, r, t):
        i = j = 0
        while j + self.n < r:
            if (t - self.todo[i]) in self.pos[i]:
                return self.pos[i][t]
            i += 1
            j += self.n
        while j < r:
            if self.get(j) == t:
                return j
            j += 1
        return


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case3=dict(nums=[1, 2], result=2),
            case0=dict(nums=[2, 5, 4, 3], result=4),
            case1=dict(nums=[3, 2, 2, 5, 4], result=5),
            case2=dict(nums=[0, 2, 1], result=2),
        )

    def longestBalanced(self, nums: List[int]) -> int:
        n = len(nums)
        bs, ans = Bk(n + 1, self.logger), 0
        last_idx = dict()
        # self.logger.info(nums)
        for i, v in enumerate(nums, 1):
            u = 1 if v % 2 else -1
            if v in last_idx:
                bs.update(last_idx[v], i - 1, -u)
            else:
                bs.update(i, n, u)
            t = bs.get(i)
            j = bs.find(i - ans, t)
            if j is not None:
                ans = max(i - j, ans)
            last_idx[v] = i
            # self.logger.map(i=i, j=j, t=t, ans=ans)
        return ans

    execute = longestBalanced
