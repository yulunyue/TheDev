from common.util.export import MockCf, CT, List
from common.algo.base.geo.andrew import Andrew, Vec


class Solution(MockCf):
    """
    将一个长度为为n的正整数数组A，恰好分成连续的k个子数组，如何求k个子数组和的平方的和的最小值
    a[i][j]=min(a[t][j-1]+(p[i]-p[t])**2,j-1<=t<=i)
        =p[i]**2+min(a[t][j-1]+p[t]**2 -2*p[i] *p[t])
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        p = [0] * (n + 1)
        for i, v in enumerate(nums):
            p[i + 1] = p[i] + v
        f = [0] + [CT.inf] * n
        for j in range(k):
            x = p[j]
            a = Andrew().append_down_det(x, f[j] + x * x)
            for i in range(j, n - k + j + 1):
                x = p[i + 1]
                kx = Vec(-2 * x, 1)
                while len(a.q) > 1 and kx.dot(a.q[0]) >= kx.dot(a.q[1]):
                    a.q.popleft()
                a.append_down_det(x, f[i + 1] + x * x)
                f[i + 1] = x * x + kx.dot(a.q[0])

        return (f[-1] + p[-1]) // 2

    execute = minPartitionScore
