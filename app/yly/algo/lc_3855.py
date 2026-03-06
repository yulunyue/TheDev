from common.util.export import MockCf, CT,math


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(l=1, r=2, k=2, result=66),
        )

    def sumOfNumbers(self, l: int, r: int, k: int) -> int:
        n = r - l + 1
        s = (l + r) * n // 2
        a = pow(10,k,CT.MOD)-1
        d = pow(n, (k - 1), CT.MOD)
        b = pow(9,-1,CT.MOD)
        return round(a *s* d*b) % CT.MOD

    execute = sumOfNumbers
