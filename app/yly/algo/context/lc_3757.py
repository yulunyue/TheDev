from common.util.export import List, MockCf, functools, CT

P2 = [1] * ((10**5) + 1)
for i in range(1, len(P2)):
    P2[i] = (P2[i - 1] * 2) % CT.MOD


class Solution(MockCf):
    def countEffective(self, nums: List[int]) -> int:
        """
        or_all = xor(nums)
        求解有多少个子集=or_all
        """
        x = 0

        for v in nums:
            x |= v
        n = len(nums)

        @functools.lru_cache(None)
        def dfs(i, s):
            if i == n:
                return 1 if s == 0 else 0
            if s == 0:
                return P2[n - i]
            v = s & nums[i]
            a = dfs(i + 1, s)
            if v:
                a += dfs(i + 1, s ^ v)
            else:
                a *= 2
            # self.logger.map(i=i, s=s, a=a)
            return a % CT.MOD

        ret = (P2[n] - dfs(0, x)) % CT.MOD
        dfs.cache_clear()
        return ret

    def countEffective(self, nums: List[int]):
        if all(x == nums[0] for x in nums):
            return 1
        n = len(nums)
        or_all = functools.reduce(lambda a, b: a | b, nums)
        w = or_all.bit_length()
        u = 1 << w
        f = [0] * u
        for x in nums:
            f[x] += 1
        for i in range(w):
            bit = 1 << i
            if or_all & bit == 0:
                continue
            s = 0
            while s < u:
                s |= bit
                f[s] += f[s ^ bit]
                s += 1
        ans = P2[n]
        sub = or_all
        while True:
            p2 = P2[f[sub]]
            flag = (or_all ^ sub).bit_count() % 2
            ans -= -p2 if flag else p2
            if sub == 0:
                break
            sub = (sub - 1) & or_all
        return ans % CT.MOD

    execute = countEffective
