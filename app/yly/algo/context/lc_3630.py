from common.util.export import List, Dict, logger


class Solution:
    def get_cases(self):
        return [
            dict(nums=[2, 3, 6, 7], result=15),
            dict(nums=[625, 165, 454, 598], result=1834.1),
        ]

    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)
        ct = {(n, n): 0}
        on = [0]
        for i, v in enumerate(nums):
            on.append(on[-1] ^ v)
            ct[i, i], ct[i, i + 1] = 0, v
            for j in range(i + 2, n + 1):
                ct[i, j] = ct[i, j - 1] & nums[j - 1]
        mx = 0
        for i in range(n + 1):
            for j in range(i, n + 1):
                o0i = on[0] ^ on[i]
                ojn = on[j] ^ on[n]
                oij = on[i] ^ on[j]
                a = o0i + oij + ct[j, n]
                b = o0i + ct[i, j] + ojn
                c = ct[0, i] + oij + ojn
                logger.map(
                    o0i=o0i, oij=oij, ojn=ojn, c0i=ct[0, i], cij=ct[i, j], cjn=ct[j, n]
                )
                mx = max(mx, a, b, c)
        return mx

    def test(self, nums):
        def and_fun(l, r, tp=0):
            if l == r:
                return 0
            a = nums[l]
            for v in range(l + 1, r):
                if tp == 0:
                    a &= nums[v]
                else:
                    a ^= nums[v]
            return a

        def xor_fun(l, r):
            return and_fun(l, r, 1)

        mx = 0
        n = len(nums)
        for i in range(n + 1):
            for j in range(i, n + 1):
                a1 = and_fun(0, i) + xor_fun(i, j) + xor_fun(j, n)
                a2 = xor_fun(0, i) + and_fun(i, j) + xor_fun(j, n)
                a3 = xor_fun(0, i) + xor_fun(i, j) + and_fun(j, n)
                mx = max(mx, a1, a2, a3)
        return mx

    def execute(self, *args, **kw):
        return self.maximizeXorAndXor(*args, **kw)
