from common.util.export import List, defaultdict, MockCf
from common.algo.base.comb import Comb

MX = 20
C = Comb().load(MX)
F = defaultdict(int)
for k in range(MX):
    for j in range(MX - k * 2):
        for i in range(k + j * 2, MX):
            F[i, k] += C.comb(i, j + k) * C.comb(i - j - k, j)


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[2, 3, 2], k=6, result=2),
        )

    def countSequences(self, nums: List[int], k: int) -> int:
        ct = [0] * 6
        a1 = 1
        kt = [0] * 6
        for v in nums:
            if v == 1:
                a1 *= 3
                continue
            elif k % v == 0:
                k = k // v
                kt[v] += 1
            ct[v] += 1
        kt[2] += 2 * kt[4]
        kt[4] = 0
        if k != 1:
            return 0
        a24 = 0
        for i in range(ct[4] + 1):
            for j in range(ct[2] + 1):
                if i * 2 + j == kt[2]:
                    a24 += F[ct[4], i] * F[ct[2], j]
        a35 = F[ct[3], kt[3]] * F[ct[5], kt[5]]
        if a24 == 0:
            a24 = 1
        return a1 * a35 * a24

    execute = countSequences
