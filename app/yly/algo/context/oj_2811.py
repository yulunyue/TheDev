from common.util.export import logger
from common.mock import MockCf

I1 = """0 1 1 0 1 0
1 0 0 1 1 1
0 0 1 0 0 1
1 0 0 1 0 1
0 1 1 1 0 0"""

R1 = """1 0 1 0 0 1
1 1 0 1 0 1
0 0 1 0 1 1
1 0 0 1 0 0
0 1 0 0 0 0"""
DR = [[0, 1], [1, 0], [0, -1], [-1, 0]]
STORE = dict()


def u(s: str):
    return [[int(u) for u in v.split(" ")] for v in s.split("\n")]


class Solution(MockCf):
    uri = "http://bailian.openjudge.cn/practice/2811/"

    def get_cases(self):
        return [dict(inputs=I1, result=R1)]

    def execute(self, inputs: str):
        self.test()

    def get_nexts(self, y, x):
        if (y, x) in STORE:
            return STORE[y, x]
        STORE[y, x] = [[y, x]]
        for dy, dx in DR:
            pass
        return STORE[y, x]

    def test(self):
        i, o = u(I1), u(R1)
        for i, row in enumerate(o):
            for j, v in enumerate(row):
                pass

    def main(self):
        s = [input() for _ in range(5)]
        print(self.execute("\n".join(s)))


if __name__ == "__main__":
    Solution().main()
