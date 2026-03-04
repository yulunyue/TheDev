from common.util.export import MockCf, List
from sortedcontainers import SortedList


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(nums=[5, 4, 5, 6], k=2, result=7))

    def maxXor(self, nums: list[int], k: int) -> int:
        t = SortedList()
        j = 0
        x = mx = 0
        self.logger.info(nums)
        for i, v in enumerate(nums):
            t.add(v)
            x ^= v
            while j < i and t[-1] - t[0] > k:
                t.remove(nums[j])
                x ^= nums[j]
                j += 1
            y = x
            for k in range(j, i + 1):
                if y > mx:
                    mx = y
                y ^= nums[j]
            self.logger.map(v=v, j=j, i=i, x=x, y=y, mx=mx)
        return mx

    execute = maxXor
