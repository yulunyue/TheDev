from common.util.export import List, defaultdict, MockCf, functools
from common.algo.base.comb import Comb

MX = 20
C = Comb().load(MX)
F = defaultdict(int)
G = []
for k in range(MX):
    G.append([])
    for m in range(k + 1):
        for n in range(k + 1 - m):
            G[-1].append([m, n, n - m])
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

        def u(a, b, c):
            return C.comb(a, b) * C.comb(a - b, c)

        if k != 1:
            return 0
        a2346 = 0
        for l6, r6, c6 in G[ct[6]]:
            k3, k2, a = kt[3] - c6, kt[2] - c6, u(ct[6], l6, r6)
            for l3, r3, c3 in G[ct[3]]:
                k3 -= c3
                if k3 < 0:
                    break
                if k3 > 0:
                    continue
                a *= u(ct[3], l3, r3)
                for l4, r4, c4 in G[ct[4]]:
                    k2 -= c4 * 2
                    a *= u(ct[4], l4, r4)
                    if k2 < 0:
                        k2 = -k2
                    if k2 <= ct[2]:
                        a *= F[ct[2], k2]
            a2346 += a

        a1, a5 = 3 ** ct[1], F[ct[5], kt[5]]
        if a2346 == 0:
            a2346 = 1
        return a1 * a5 * a2346

    execute = countSequences
