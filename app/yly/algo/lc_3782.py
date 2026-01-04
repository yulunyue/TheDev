from common.util.export import MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(n=1, result=1),
            case1=dict(n=2, result=1),
            case2=dict(n=3, result=3),
            case3=dict(n=4, result=3),
            case4=dict(n=9, result=9),
        )

    def lastInteger(self, n: int) -> int:
        """ """
        l, r = 1, n
        c = 1
        k = 0
        while n > 1:
            if n % 2 == 0:
                if k == 0:
                    r = r - c
                else:
                    l = l + c
            c = c * 2
            k = 1 - k
            n = (n + 1) >> 1
        return l if k == 0 else r

    execute = lastInteger


if __name__ == "__main__":
    Solution().run()
