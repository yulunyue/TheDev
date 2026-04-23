from common.util.export import MockCf


class Solution(MockCf):
    """
    给定一个长度为n的整数数组m，对于n的每个因数s
    我们可以将m分成s个子数组t，可以在t内做任意次循环移动使得m非递减
    要使 t 递增，t中有且只能有一个下降，且最小值在最大值右边
    如果 2*t 是满足的
    1<=n<=10**5
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[3, 1, 2], expected=3),
        )

    def sortableIntegers(self, nums: list[int]) -> int:
        n = len(nums)
        self.ans = 0
        next_up = [n] * n
        last_up_idx = n
        for i in range(n - 1, 0, -1):
            if nums[i - 1] > nums[i]:
                last_up_idx = i
            next_up[i - 1] = last_up_idx

        def solve(k):
            lmx = float("-inf")
            for l in range(0, n, k):
                r = l + k - 1
                nup = next_up[l]
                if nup > r:
                    if nums[l] < lmx:
                        return False
                    lmx = nums[r]
                    continue
                if nums[nup] < lmx:
                    return False
                if next_up[nup] <= r:
                    return False
                if nums[r] > nums[l]:
                    return False

                lmx = nums[nup - 1]
            self.ans += k
            return True

        for i in range(1, n):
            if n % i:
                continue
            j = n // i
            if i > j:
                break
            solve(i)
            if i != j:
                solve(j)
        return self.ans

    execute = sortableIntegers
