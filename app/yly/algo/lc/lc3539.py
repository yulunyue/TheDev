from common.util.export import List, C, functools
from common.algo.base.math_util import Comb

CB = Comb().load((10**5) + 1, C.MOD)


class Solution:
    def get_cases(self):
        return [dict(M=5, K=5, nums=[1, 10, 100, 10000, 1000000], result=991600007)]

    def magicalSum(self, M: int, K: int, nums: List[int]) -> int:
        n = len(nums)
        pow_v = [[1] * (M + 1) for _ in range(n)]
        for i, v in enumerate(nums):
            for j in range(1, M + 1):
                pow_v[i][j] = pow_v[i][j - 1] * v % C.MOD

        @functools.cache
        def dfs(i: int, left_m: int, x: int, left_k: int) -> int:
            c1 = x.bit_count()
            if c1 + left_m < left_k:  # 可行性剪枝
                return 0
            if i == n or left_m == 0 or left_k == 0:  # 无法继续选数字
                return 1 if left_m == 0 and c1 == left_k else 0
            res = 0
            for j in range(left_m + 1):  # 枚举 I 中有 j 个下标 i
                # 这 j 个下标 i 对 S 的贡献是 j * pow(2, i)
                # 由于 x = S >> i，转化成对 x 的贡献是 j
                bit = (x + j) & 1  # 取最低位，提前从 left_k 中减去，其余进位到 x 中
                r = dfs(i + 1, left_m - j, (x + j) >> 1, left_k - bit)
                res += r * pow_v[i][j] * CB.inv_fac[j]
            return res % C.MOD

        return dfs(0, M, 0, K) * CB.fac[M] % C.MOD
