from common.util.export import logger, List
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
        self.inputs = u(inputs)
        self.h, self.w = len(self.inputs), len(self.inputs[0])
        self.mask_all = (2**self.w) - 1
        self.init()
        self.result = [[0] * self.w for _ in range(self.h)]
        self.change_dfs(0)
        return "\n".join([" ".join(str(v) for v in row) for row in self.result])

    def change_dfs(self, j):
        if j == self.w:
            return self.change_row()
        else:
            if self.change_dfs(j + 1):
                return True
            self.change(0, j)
            if self.change_dfs(j + 1):
                return True
            self.change(0, j)
        return False

    def change_row(self):
        for i in range(1, self.h):
            for j in range(self.w):
                if self.inputs[i - 1][j]:
                    self.change(i, j)
        if sum(self.inputs[-1]) == 0:
            # logger.info(self.inputs)
            return True
        return False

    def change(self, i, j):
        self.result[i][j] = 1 - self.result[i][j]
        for y, x in self.relative_pos[i][j]:
            self.inputs[y][x] = 1 - self.inputs[y][x]

    def init(self):
        self.relative_pos = []
        for i, row in enumerate(self.inputs):
            self.relative_pos.append([])
            for j, v in enumerate(row):
                tmp = [[i, j]]
                if i > 0:
                    tmp.append([i - 1, j])
                if j > 0:
                    tmp.append([i, j - 1])
                if i + 1 < len(self.inputs):
                    tmp.append([i + 1, j])
                if j + 1 < len(row):
                    tmp.append([i, j + 1])
                self.relative_pos[-1].append(tmp)

    def check(self):
        pass

    def main(self):
        s = [input() for _ in range(5)]
        print(self.execute("\n".join(s)))


if __name__ == "__main__":
    Solution().main()
