from common.util.export import MockCf, functools, CT, List


class Solution(MockCf):
    """
    给定长度为n的数组nums，和k
    我们需要从nums选择一个子序列 s
    满足
        s[i+1]-s[i]>=k
        nums[s[i]],nums[s[i+1]] 交替增减
    求nums[s]的最大值

    对于 s[i]属于 [n-k,n) 最大值dadd[i],dsub[i]为 s[i]
    对于 s[i]属于 [n-k*2,n-k) 最大值为
        减,dadd[i] = s[i]+max(nums[i+k:] if v>s[i])
        加,dsub[i] = s[i]+max(nums[i+k:] if v<s[i])
    对于 s[i]属于 [n-k*3,n-2*k)
        减,s[i]+max(nums[i+k:] if v>s[i],dsub[i])
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[5, 4, 2], k=2, expected=7),
        )

    def maxAlternatingSum1(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        # 1. 值域离散化
        vals = sorted(set(nums))
        m = len(vals)
        val_to_idx = {v: i for i, v in enumerate(vals)}  # 值 -> 离散化下标

        INF_NEG = -(10**18)  # 负无穷

        # 2. 线段树（支持单点更新，区间查询最大值）
        class SegTree:
            def __init__(self, size):
                self.N = 1
                while self.N < size:
                    self.N <<= 1
                self.tree = [INF_NEG] * (2 * self.N)

            def update(self, pos, val):
                i = pos + self.N
                if val > self.tree[i]:
                    self.tree[i] = val
                    i >>= 1
                    while i:
                        self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])
                        i >>= 1

            def query(self, l, r):  # 区间 [l, r] 最大值，若 l>r 返回负无穷
                if l > r:
                    return INF_NEG
                l += self.N
                r += self.N
                res = INF_NEG
                while l <= r:
                    if l & 1:
                        res = max(res, self.tree[l])
                        l += 1
                    if not (r & 1):
                        res = max(res, self.tree[r])
                        r -= 1
                    l >>= 1
                    r >>= 1
                return res

        tree_up = SegTree(m)  # 存储 dp_up[j] (最后一步为上升)
        tree_down = SegTree(m)  # 存储 dp_down[j] (最后一步为下降)

        dp_up = [0] * n
        dp_down = [0] * n

        ans = INF_NEG

        for i in range(n):
            # 将距离当前 i 刚好为 k 的索引加入线段树
            if i - k >= 0:
                idx = val_to_idx[nums[i - k]]
                tree_up.update(idx, dp_up[i - k])
                tree_down.update(idx, dp_down[i - k])

            cur = nums[i]
            pos = val_to_idx[cur]

            # 查询所有小于 cur 的 dp_down 最大值（用于上升转移）
            best_down = tree_down.query(0, pos - 1)
            # 查询所有大于 cur 的 dp_up 最大值（用于下降转移）
            best_up = tree_up.query(pos + 1, m - 1)

            # 转移：可以单独作为子序列，也可以接在前面尾巴后面
            dp_up[i] = max(cur, cur + best_down) if best_down != INF_NEG else cur
            dp_down[i] = max(cur, cur + best_up) if best_up != INF_NEG else cur

            ans = max(ans, dp_up[i], dp_down[i])

        return ans

    def maxAlternatingSum2(self, nums: list[int], k: int) -> int:
        n = len(nums)

        @functools.lru_cache(None)
        def dfs(i, lc):
            mn = -CT.inf
            for j in range(i + k, n):
                c = nums[j] - nums[i]
                if c == 0 or c * lc > 0:
                    continue
                v = dfs(j, 1 if c > 0 else -1)
                if v > mn:
                    mn = v
            if mn == -CT.inf:
                mn = 0
            mn += nums[i]
            self.log(i=i, lc=lc, mn=mn)
            return mn

        ans = max(dfs(i, 0) for i in range(n))
        dfs.cache_clear()
        return ans

    execute = maxAlternatingSum
