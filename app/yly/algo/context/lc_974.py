from common.util.export import List, MockCf, defaultdict


class Solution(MockCf):
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        ct = defaultdict(int)
        s = ans = 0
        for v in nums:
            ct[s] += 1
            s = (s + v) % k
            ans += ct[s]

        return ans

    execute = subarraysDivByK
