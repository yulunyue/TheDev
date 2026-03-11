from common.util.export import MockCf, CT, List, functools, itertools, deque
from common.algo.base.geo.andrew import Andrew, Vec


class Solution(MockCf):
    """
    将一个长度为为n的正整数数组A，恰好分成连续的k个子数组，如何求k个子数组和的平方的和的最小值
    a[i][j]=min(a[t][j-1]+(p[i]-p[t])**2,j-1<=t<=i)
        =p[i]**2+min(a[t][j-1]+p[t]**2 -2*p[i] *p[t])
    """

    def get_cases(self):
        return dict(
            case2=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=4),
            case0=dict(nums=[5, 39, 4, 32], k=2, result=1656),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        pre = list(itertools.accumulate(nums, initial=0))
        f = [0] + [CT.inf] * n

        for K in range(1, k + 1):
            s = pre[K - 1]
            q = deque([Vec(s, f[K - 1] + s * s - s)])
            for i in range(K, n - (k - K) + 1):  # 其他子数组的长度至少是 1
                s = pre[i]
                p = Vec(-2 * s, 1)
                while len(q) > 1 and p.dot(q[0]) >= p.dot(q[1]):
                    q.popleft()

                v = Vec(s, f[i] + s * s - s)
                f[i] = p.dot(q[0]) + s * s + s

                while len(q) > 1 and (q[-1] - q[-2]).det(v - q[-1]) <= 0:
                    q.pop()
                q.append(v)
                self.logger.map(j=K - 1, i=i, fi=f[i], q=list(q))

        return f[n] // 2

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        p = [0] * (n + 1)
        for i, v in enumerate(nums):
            p[i + 1] = p[i] + v
        f = [0] + [CT.inf] * n
        for j in range(k):
            x = p[j]
            a = Andrew().append_down_det(x, f[j] + x * x - x)
            for i in range(j, n - k + j + 1):
                x = p[i + 1]
                kx = Vec(-2 * x, 1)
                while len(a.q) > 1 and kx.dot(a.q[0]) >= kx.dot(a.q[1]):
                    a.q.popleft()
                v = Vec(x, f[i + 1] + x * x - x)
                f[i + 1] = x * x + kx.dot(a.q[0]) + x
                a.append_down_det(v)
                self.logger.map(j=j, i=i, fi=f[i + 1], q=list(a.q))

        return f[-1] // 2

    execute = minPartitionScore
