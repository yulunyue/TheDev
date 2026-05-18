from common.util.export import List, Dict, functools, CT, LOG, bisect


class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)
        st = sorted(set(nums))
        ret = 0
        l = r = nums[0]
        while st:
            l -= target
            r += target
            li = bisect.bisect_left(st, l)
            ri = bisect.bisect_right(st, r)
            if li == ri:
                return -1
            if nums[-1] <= st[ri]:
                return ret
            st = st[:li] + st[ri:]
            ret += 1
        return -1
