from common.mock import MockCf
from common.util.export import List, CT, logger

I1 = """1 1
2 3
7 4
4 6"""


def ii(s: str):
    return [list(map(int, v.split(" "))) for v in s.split("\n")]


class Solution(MockCf):
    def get_cases(self):
        return [dict(s=ii(I1), result=2)]

    def execute(self, s: List[List[int]]):
        pre, _ = s.pop(0)
        s.sort(key=lambda a: a[0] * a[1])
        ans = 0
        for i, (u, v) in enumerate(s):
            c = pre // v
            if c > ans:
                ans = c
            pre *= u
        return ans

    def run(self):
        n, *args = self.input()
        s = [self.ii() for _ in range(n)]
        print(self.execute(s))


if __name__ == "__main__":
    Solution().run()
