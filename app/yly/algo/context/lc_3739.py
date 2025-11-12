from common.util.export import List, MockCf
from sortedcontainers import SortedList


class Solution(MockCf):
    def countMajoritySubarrays(self, nums: List[int], target: int) -> int:
        te = SortedList()
        s = 0
        for v in nums:
            u = 1 if v == target else -1
            s += u
            te.add(s)
        s = 0
        ans = 0
        for v in nums:
            u = 1 if v == target else -1
            ans += len(te) - te.bisect_right(s)
            s += u
            te.remove(s)
        return ans

    def countMajoritySubarrays(self, nums: List[int], target: int) -> int:
        s = n = len(nums)
        cnt = [0] * (n * 2 + 1)
        ans = f = 0
        cnt[s] = 1
        for x in nums:
            if x == target:
                f += cnt[s]
                s += 1
            else:
                s -= 1
                f -= cnt[s]
            ans += f
            cnt[s] += 1
        return ans

    execute = countMajoritySubarrays
