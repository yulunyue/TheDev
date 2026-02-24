from common.util.export import List, defaultdict, MockCf, functools
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
        ct, kt = [0] * 7, [0] * 7
        a1 = 1
        for v in nums:
            if k % v == 0:
                k = k // v
                if v == 4:
                    kt[2] += 2
                elif v == 5:
                    kt[2] += 1
                    kt[3] += 1
                else:
                    kt[v] += 1
            ct[v] += 1

        if k != 1:
            return 0
        a2346 = 0
        for a6 in range(ct[6] + 1):
            for a4 in range(ct[4] + 1):
                for
            c6, r6, r2, r3 = a6, ct[6] - c6, ct[2], ct[3]
            while c6 - r6 <= min(r2 - kt[2], r3 - kt[3]):
                c6 += 1
                for k6 in range(r6 + 1):
                    k2, k3 = kt[2] - k6, kt[3] - k6
                    if k2 < 0 or k3 < 0:
                        break
                r6 -= 1

        a1, a5 = 3 ** ct[1], F[ct[5], kt[5]]
        if a2346 == 0:
            a2346 = 1
        return a1 * a5 * a2346

    execute = countSequences
