from common.util.export import List, Dict, MockCf


class Solution(MockCf):
    uri = "https://www.luogu.com.cn/problem/P2123"

    def calc(self, a, b):
        ans = 0
        return ans

    def execute(self):
        ans = []
        for _ in range(int(self.input())):
            numsa, numsb = [], []
            for _ in range(int(self.input())):
                a, b = self.ii()
                numsa.append(a)
                numsb.append(b)
            ans.append(self.calc(numsa, numsb))
        return "\n".join([str(v) for v in ans])


if __name__ == "__main__":
    print(Solution().execute())
