from common.util.export import List, MockCf, defaultdict
from common.algo.base.bin_util import low_bits


class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(nums=[1, 2, 3], result=3))

    def countEffective(self, nums: List[int]) -> int:
        xor_all = 0
        f = defaultdict(int)
        for v in nums:
            xor_all |= v
            f[v] += 1
        n = xor_all.bit_length()
        for i in range(n):
            u = 1 << i
            v = 0
            while v <= xor_all:
                v = v | u
                v += 1

    execute = countEffective


if __name__ == "__main__":
    Solution().run()
