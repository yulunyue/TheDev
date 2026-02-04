from common.util.export import List, MockCf, functools, heapq, bisect
from sortedcontainers.sortedlist import SortedList


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(nums=[1, 3, 2, 6, 4, 2], k=3, dist=3, result=5))

    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        n = len(nums)
        k -= 1
        dist += 1
        sl = sorted(nums[1 : dist + 1])
        tmp = mx = sum(sl[:k])
        self.logger.info(sl)
        for i in range(dist + 1, n):
            lv, rv = nums[i - dist], nums[i]
            li = bisect.bisect_left(sl, lv)

            if li < k:
                tmp -= lv - sl[k]
            sl.pop(li)
            ri = bisect.bisect_left(sl, rv)
            sl.insert(ri, rv)
            if ri < k:
                tmp += rv - sl[k]
            if tmp < mx:
                mx = tmp
            self.logger.map(i=i, lv=lv, li=li, ri=ri, rv=rv, sl=sl)
        return nums[0] + mx

    execute = minimumCost
