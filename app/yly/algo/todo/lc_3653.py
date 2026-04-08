from common.util.export import MockCf, List, math, CT, functools, operator


class Solution(MockCf):
    """
    给定一个数组nums和一个长度为m的操作序列q
    q[i]=l,r,k,v
    for l,r,k,v in q:
      for j in range(l,r,k):
        nums[j]*=v
    求nums的异或和
    """

    def get_cases(self):
        return dict(
            case0=dict(
                nums=[2, 3, 1, 5, 4], queries=[[1, 4, 2, 3], [0, 2, 1, 2]], result=31
            ),
        )

    def xorAfterQueries(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        B = math.isqrt(n)
        diff = [None] * B
        for l, r, k, v in queries:
            if k < B:
                if diff[k] is None:
                    diff[k] = [1] * (n + k)
                diff[k][l] = diff[k][l] * v % CT.MOD
                r = r + k - (r - l) % k
                diff[k][r] = diff[k][r] * pow(v, -1, CT.MOD) % CT.MOD
            else:
                for i in range(l, r + 1, k):
                    nums[i] = nums[i] * v % CT.MOD

        for k, d in enumerate(diff):
            if d is None:
                continue
            for start in range(k):
                mul_d = 1
                for i in range(start, n, k):
                    mul_d = mul_d * d[i] % CT.MOD
                    nums[i] = nums[i] * mul_d % CT.MOD

        return functools.reduce(operator.xor, nums)

    execute = xorAfterQueries
