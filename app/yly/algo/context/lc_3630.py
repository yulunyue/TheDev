from common.util.export import List


class Solution:
    def get_cases(self):
        return [dict(nums=[2, 3, 6, 7], result=15)]

    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)

        def u(nums):
            a = [0]
            c = 0
            for v in nums:
                c ^= v
                a.append(c)
            return a

        a = u(nums)
        c = u(nums[::-1])[::-1]
        mx = a[-1]
        for i in range(n):
            mx = max(mx, a[i] + c[i])
            b = 0
            for j in range(i, n):
                b &= nums[j]
                mx = max(mx, a[i] + b + c[j + 1])
        return mx

    def execute(self, *args, **kw):
        return self.maximizeXorAndXor(*args, **kw)
