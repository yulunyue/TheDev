from common.util.export import List, MockCf, CT, bisect


class Solution(MockCf):
    """
    给定一个长度为n的数组nums
    一个querys么（l，r，k）数组，
    对于每一个q=nums[l，r+1]
    我们需要找到第大的偶数，这个偶数不在q中

    """

    def get_cases(self):
        return dict(
            case2=dict(
                nums=[4, 6, 22, 24], queries=[[0, 2, 10], [0, 3, 13]], expected=[26, 34]
            ),
            case1=dict(nums=[2, 8], queries=[[0, 1, 1], [0, 1, 2]], expected=[4, 6]),
            case0=dict(
                nums=[1, 4, 7],
                queries=[[0, 2, 1], [1, 1, 2], [0, 0, 3]],
                expected=[2, 6, 6],
            ),
        )

    def kthRemainingInteger(
        self, nums: list[int], queries: list[list[int]]
    ) -> list[int]:
        n = len(nums)
        idx = [[None, None] for _ in range(n)]
        lv, rv = 0, CT.inf
        ct = [0]
        for i in range(n):
            j = n - 1 - i
            iv, jv = nums[i], nums[j]
            if iv % 2 == 0:
                lv = iv // 2
            if jv % 2 == 0:
                rv = jv // 2
            idx[i][0], idx[j][1] = lv, rv
            ct.append(ct[-1] + (iv % 2 == 0))

        ans = [0] * len(queries)
        # self.log(nums=[0 if v % 2 else v // 2 for v in nums], idx=idx, ct=ct)
        for i, (l, r, k) in enumerate(queries):
            _, lr = idx[l]
            d = lr - 1
            # self.log(l=l, r=r, k=k, ll=ll, lr=lr)
            if d >= k:
                ans[i] = k * 2
                continue

            def util(j):
                cm = ct[j + 1] - ct[l]
                c = idx[j][0] - lr + 1 - cm
                # self.log(j=j, d=d, c=c)
                if c + d >= k or j == r:
                    return k + cm - (c + d >= k)
                return None

            lc = l + bisect.bisect_left(
                range(l, r + 1), True, key=lambda v: util(v) is not None
            )

            ans[i] = util(lc) * 2
        return ans

    execute = kthRemainingInteger
