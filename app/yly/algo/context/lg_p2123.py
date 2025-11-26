from common.util.export import List, Dict, MockCf


class Solution(MockCf):
    uri = "https://www.luogu.com.cn/problem/P2123"
    """  A,B 为正整数
    MA[i] = SUM(A[:i+1])
    C[i] = A[i] + B[i] i==1
         = max(C[i-1], MA[i]) + B[i] i>=2
    考虑 位置 i, j=i+1, k=i-1
    不交换
    C[j] = max(max(), MA[k]+A[i]+A[j])+B[j]
    """

    def calc(self, a, b):
        ans = 0
        n = len(a)
        for i in range(n):
            if i == 0:
                pass
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
