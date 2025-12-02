from common.util.export import List, Dict, MockCf, CT


class Solution(MockCf):
    uri = "https://www.luogu.com.cn/problem/P2123"
    """  A,B 为正整数
    MA[i] = SUM(A[:i+1])
    C[i] = A[i] + B[i] i==1
         = max(C[i-1], MA[i]) + B[i] i>=2
    考虑 位置 i, i+1,i-1
    不交换
    C[i+1] = max(
        C[i-1] + B[i] + B[i+1], 
        MA[i-1] + A[i] + B[i] + B[i+1],
        MA[i-1]+ A[i]+ A[i+1]+ B[i+1]
    )
    交换 i,i+1
    C[i+1] = max(
        C[i-1]+B[i+1]+B[i],
        MA[i-1]+A[i+1]+B[i+1]+B[i],
        MA[i-1]+A[i]+A[i+1]+B[i],
    )
    则不交换不会变差
    min(A[i],B[i+1])<=min(A[i+1],B[i])


    """

    def calc(self, a, b):
        c = c1 = 0
        n = len(a)
        ai, bi = a[0], b[0]
        for i in range(1, n):
            aj, bj = a[i], b[i]
            bs += bj
            c1 = c
            if CT.min(ai, bj) > CT.min(aj, bi):
                pass
            else:
                c1 = max()
            ai, bi, c1 = aj, bj, c

        return c1

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
