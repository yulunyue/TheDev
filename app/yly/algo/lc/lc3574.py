from common.util.export import List, math, C, defaultdict, logger


class Solution:
    def get_cases(self):
        return [
            dict(nums=[3, 5, 7], k=2, result=14),
            dict(nums=[5, 5, 5], k=1, result=15),
        ]

    def maxGCDScore(self, nums: List[int], k: int) -> int:
        lowbit_pos = defaultdict(list)
        ans = 0
        intervals = []
        for i, x in enumerate(nums):
            lowbit_pos[x & -x].append(i)
            for p in intervals:
                p[0] = math.gcd(p[0], x)
            intervals.append([x, i - 1, i])
            idx = 1
            for j in range(1, len(intervals)):
                if intervals[j][0] != intervals[j - 1][0]:
                    intervals[idx] = intervals[j]
                    idx += 1
                else:
                    intervals[idx - 1][2] = intervals[j][2]
            del intervals[idx:]
            for g, l, r in intervals:
                ans = max(ans, g * (i - l))
                pos = lowbit_pos[g & -g]
                min_l = l
                if len(pos) > k:
                    min_l = max(l, pos[-k - 1])
                if min_l < r:
                    ans = max(ans, g * 2 * (i - min_l))

        return ans
