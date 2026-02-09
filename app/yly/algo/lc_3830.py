from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[2, 1, 3, 2], result=4),
            case1=dict(nums=[3, 2, 1, 2, 3, 2, 1], result=4),
            case2=dict(nums=[1, 1], result=1),
        )

    def calc_p(self, nums):
        p = [[1, 0]]
        for i in range(1, len(nums)):
            u, v = nums[i - 1], nums[i]
            c = v - u
            if c == 0:
                p.append([1, 0])
            elif c * p[-1][-1] > 0:
                p.append([2, c])
            else:
                p.append([p[-1][0] + 1, c])
        return p

    def longestAlternating(self, nums: List[int]) -> int:
        n = len(nums)
        pres = self.calc_p(nums)
        sufs = self.calc_p(nums[::-1])[::-1]
        ans = max(pres)[0]
        self.logger.info(pres)
        self.logger.info(sufs)
        for i in range(1, n - 1):
            c = nums[i + 1] - nums[i - 1]
            if c == 0:
                continue
            self.logger.map(i=i, c=c, p=pres[i - 1], s=sufs[i + 1])
            if pres[i - 1][1] * c < 0 and c * sufs[i + 1][1] > 0:
                ans = max(pres[i - 1][0] + sufs[i + 1][0], ans)
        return ans

    execute = longestAlternating
