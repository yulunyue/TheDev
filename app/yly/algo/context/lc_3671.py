from common.util.export import List, logger, CT, defaultdict, math
from common.algo.base.fen_wick_node import FenWickTree

mx = (10**5) + 1
div = [[] for _ in range(mx)]
for i in range(1, mx):
    for j in range(i, mx, i):
        div[j].append(i)


class Solution:
    def get_cases(self):
        return [dict(nums=[1, 2, 3], result=10)]

    def query(self, data):
        mx = max(data)
        f = FenWickTree().set_range(mx)
        ans = 0
        for v in data:
            a = f.query(v - 1)
            f.update(v, a + 1)
            ans += a + 1
        return ans

    def totalBeauty(self, nums: List[int]) -> int:
        mx = len(nums)
        p = [[] for _ in range(mx + 1)]
        for x in nums:
            for d in div[x]:
                p[d].append(x // d)
        res = 0
        f = [0] * (mx + 1)
        for x in range(mx, 0, -1):
            if not p[x]:
                continue
            f[x] = self.query(p[x])
            for y in range(x * 2, mx + 1, x):
                f[x] -= f[y]
            res = (res + f[x] * x) % CT.MOD
            # logger.map(res=res, px=p[x])
        return res

    execute = totalBeauty
