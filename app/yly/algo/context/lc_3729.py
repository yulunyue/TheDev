from common.util.export import MockCf, List, defaultdict


class Solution(MockCf):
    def numGoodSubarrays(self, nums: List[int], k: int) -> int:
        ans = 0
        ct = defaultdict(int)
        s = 0
        ct_same = 0
        same_ct = 0
        for i, v in enumerate(nums):
            ct[s] += 1
            s = (s + v) % k

            if i > 0 and v == nums[i - 1]:
                ct_same += 1
                same_ct += (ct_same * v) % k == 0
            else:
                same_ct = 0
                ct_same = 0
            ans += ct[s] - same_ct
            self.logger.map(i=i, ans=ans, ct=ct[s], ct_same=ct_same, same_ct=same_ct)
        return ans

    execute = numGoodSubarrays
