from common.util.export import List
from common.algo.base.comb import Comb

MX = 20
C = Comb().load(MX)
for i in range(2, MX):
    for j in range(1, i // 2):
        pass


class Solution:
    def get_cases(self):
        return dict(dict(nums=[2, 3, 2], k=6, result=2))

    def countSequences(self, nums: List[int], k: int) -> int:
        ct = [0] * 6
        a = 1
        for v in nums:
            if v == 1:
                a *= 3
            elif k % v == 0:
                k = k // v
            else:
                ct[v] += 1

        if k != 1:
            return 0
        return a

    execute = countSequences
