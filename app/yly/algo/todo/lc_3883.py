from common.util.export import List, MockCf, functools, CT


class Solution(MockCf):
    """
    求满足要求数组s的数量
    len(s)=len(digitSum)=n

    s是非递减的
    对于每一个digstSum的元素的digstSum[i]
    digstSum[i]=sum([int(for v in str(s[i]))])
     0<=s[i]<=5000
     1<=n<=1000
     0<=digstSum[i]<=50
    """

    def get_cases(self):
        return dict(
            case0=dict(digitSum=[25, 1], result=6),
            case1=dict(digitSum=[1], result=4),
        )

    def countArrays(self, digitSum: list[int]) -> int:
        mx = 5001
        ct = [set() for _ in range(mx)]
        n = len(digitSum)
        for s in range(mx):
            v = sum([int(v) for v in str(s)])
            ct[v].add(s)

        dt = [1] * mx
        for i in range(n - 1, -1, -1):
            ds = [0] * mx
            num = 0
            se = ct[digitSum[i]]
            for j in range(mx):
                if j in se:
                    num += 1
                ds[j] = (num * dt[j]) % CT.MOD
            self.log(ds=ds)
            dt = ds
        return dt[-1]

    execute = countArrays
