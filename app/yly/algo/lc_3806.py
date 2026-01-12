from common.util.export import List, MockCf, defaultdict


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[3, 1, 2], k=8, m=2, result=6),
        )

    def maximumAND(self, nums: List[int], k: int, m: int) -> int:
        n = len(nums)
        mx = max(nums) + (k // m)
        j = mx.bit_length() - 1
        ret = 0
        nums1 = nums
        while j >= 0:
            mask = 1 << j
            q, nums1, nums2 = nums1, [], []
            for v in q:
                r = v & (mask - 1)
                if v & mask:
                    nums1.append(r)
                    m -= 1
                else:
                    nums2.append(r)
            m1 = m - len(nums1)
            if m1:
                nums2.sort(reverse=True)
                k1 = m1 * mask - sum(nums2[:m1])
                if k1 <= k:
                    k -= k1
                    ret += mask
            self.logger.map(j=j, ret=ret, nums1=nums1)
            j -= 1

        return ret

    execute = maximumAND


if __name__ == "__main__":
    Solution().run()
