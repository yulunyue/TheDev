from common.util.export import List, MockCf


class Solution(MockCf):
    """
    给定一个长度为n的数组nums
    一个querys么（l，r，k）数组，
    对于每一个q=nums[l，r+1]
    我们需要找到第大的偶数，这个偶数不在q中
    """

    def get_cases(self):
        return dict(
            case0=dict(
                nums=[1, 4, 7],
                queries=[[0, 2, 1], [1, 1, 2], [0, 0, 3]],
                expected=[2, 6, 6],
            )
        )

    def kthRemainingInteger(
        self, nums: list[int], queries: list[list[int]]
    ) -> list[int]:
        ct = []
        for i, v in enumerate(nums):
            if v % 2 == 0:
                lv = v // 2
                ct.append(lv)
            nums[i] = len(ct)-1
        ans = []
        for l, r, k in queries:
            li,ri = nums[l],nums[r]
            if k < ct[li]:
                d = k
            elif k > ct[ri]:
                d = k + ri -li+1
            else:
                d=0
                for i in range(li, ri + 1):
                    c = ct[i]-ct[li]-(ri-li)
                    if c+nums[li]>=k:
                        break
            ans.append(d*2)
        return ans

    execute = kthRemainingInteger
