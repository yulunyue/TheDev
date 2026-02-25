from common.util.export import List, defaultdict, MockCf, functools
from common.algo.base.comb import Comb

MX = 20
C = Comb().load(MX)
F = defaultdict(int)
G = []


def u(a, b, c):
    return C.comb(a, b) * C.comb(a - b, c)


for k in range(MX):
    G.append([])
    for m in range(k + 1):
        for n in range(k + 1 - m):
            G[-1].append([m, n, n - m])
    for j in range(MX):
        for i in range(k + j * 2, MX):
            F[i, k] += u(i, j + k, j)


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[2, 3, 2], k=6, result=2),
            case1=dict(nums=[4, 6, 3], k=2, result=2),
            case2=dict(nums=[5], k=4, result=0),
            case3=dict(nums=[2, 2], k=4, result=1),
            case4=dict(nums=[2] * 19, k=524288, result=1),
        )

    def countSequences(self, nums: List[int], k: int) -> int:
        ct, kt = [0] * 7, [0] * 7
        a1 = 1
        for v in [2, 3, 5]:
            while k % v == 0:
                k = k // v
                kt[v] += 1
        for v in nums:
            ct[v] += 1
        if k != 1:
            return 0
        a2346 = 0
        for l6, r6, c6 in G[ct[6]]:
            k3, k2, a = kt[3] - c6, kt[2] - c6, u(ct[6], l6, r6)
            for l3, r3, c3 in G[ct[3]]:
                k31 = k3 - c3
                if k31 != 0:
                    continue
                b = u(ct[3], l3, r3)
                for l4, r4, c4 in G[ct[4]]:
                    k21 = abs(k2 - c4 * 2)
                    c = u(ct[4], l4, r4)
                    if k21 <= ct[2]:
                        a2346 += a * b * c * F[ct[2], k21]
                    # self.logger.map(
                    #     l6=l6, r6=r6, l3=l3, r3=r3, l4=l4, r4=r4, k2=k21, a=a2346
                    # )
        a1, a5 = 3 ** ct[1], F[ct[5], kt[5]]
        return a1 * a5 * a2346

    execute = countSequences
