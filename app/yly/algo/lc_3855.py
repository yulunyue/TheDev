from common.util.export import MockCf, CT


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(l=1, r=2, k=2, result=66),
        )

    def sumOfNumbers(self, l: int, r: int, k: int) -> int:
        n = r - l + 1
        s = (l + r) * n // 2
        a = 0
        d = n ** (k - 1)
        for i in range(k):
            m = k - 1 - i
            a += s * (10**m)
        return (a * d) % CT.MOD

    execute = sumOfNumbers
