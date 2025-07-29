from common.util.export import List, Dict, logger, functools
from common.algo.base.xor_basis import XorBais


class Solution:
    def get_cases(self):
        return [
            dict(nums=[2885, 2072, 3875, 64, 3024], result=9011),
            dict(nums=[2, 3, 6, 7], result=15),
            dict(nums=[625, 165, 454, 598], result=1834),
        ]

    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)
        sz = max(nums).bit_length()
        u = 1 << n
        sub_and = [0] * u
        sub_xor = [0] * u
        sub_or = [0] * u
        sub_and[0] = -1
        for i, x in enumerate(nums):
            hight_bit = 1 << i
            for mask in range(hight_bit):
                hi = hight_bit | mask
                sub_and[hi] = sub_and[mask] & x
                sub_or[hi] = sub_or[mask] | x
                sub_xor[hi] = sub_xor[mask] ^ x
        sub_and[0] = 0

        def max_xor2(sub: int):
            b = XorBais(sz)
            xor = sub_xor[sub]
            for i, x in enumerate(nums):
                if sub >> i & 1:
                    b.insert(x & ~xor)
            return xor + b.max_xor() * 2

        ans = 0
        for i in range(u):
            j = (u - 1) ^ i
            if sub_and[i] + sub_or[j] * 2 - sub_xor[j] > ans:  # 有机会让 ans 变得更大
                ans = max(ans, sub_and[i] + max_xor2(j))
        return ans

    def execute(self, *args, **kw):
        return self.maximizeXorAndXor(*args, **kw)
