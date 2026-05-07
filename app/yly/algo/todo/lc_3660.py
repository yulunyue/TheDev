from common.util.export import List, MockCf, bisect, CT


class Solution(MockCf):
    """
    向右更小
    向左更大
    """

    def get_cases(self):
        return dict(
            case0=dict(
                nums=[2, 1, 3],
                expected=[2, 2, 3],
            )
        )

    def maxValue(self, nums: List[int]) -> List[int]:
        n = len(nums)
        r_min = [nums[-1]] * n
        for i in range(n - 2, -1, -1):
            r_min[i] = nums[i] if nums[i] < r_min[i + 1] else r_min[i + 1]
        t = [[r_min[0], nums[0]]]
        for i in range(1, n):
            if nums[i] > t[-1][-1]:
                t.append([r_min[i], nums[i]])
        ans = [-1] * n
        self.log(t=t)
        for i, v in enumerate(nums):
            j = bisect.bisect_right(t, [v, CT.inf]) - 1
            ans[i] = t[j][1]
        return ans

    execute = maxValue
