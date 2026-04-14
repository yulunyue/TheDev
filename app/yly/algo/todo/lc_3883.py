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
        ct = [[] for _ in range(mx)]
        n = len(digitSum)
        for s in range(mx):
            v = sum([int(v) for v in str(s)])
            ct[v].append(s)
        lt = ct[digitSum[-1]]
        dt = {v: len(lt) - i for i, v in enumerate(lt)}
        for i in range(n - 2, -1, -1):
            cur, nxt = ct[digitSum[i]], ct[digitSum[i + 1]]
            cur_i, nxt_i = len(cur) - 1, len(nxt) - 1
            st = dict()
            num = 0
            ns = 0
            while cur_i >= 0:
                while cur[cur_i] <= nxt[nxt_i] and nxt_i >= 0:
                    num = (num + dt[nxt[nxt_i]]) % CT.MOD
                    nxt_i -= 1
                ns = (ns + num) % CT.MOD
                st[cur[cur_i]] = ns
                cur_i -= 1
            # self.log(dt=dt, st=st, cur=cur, nxt=nxt)
            dt = st

        return dt[ct[digitSum[0]][0]]

    execute = countArrays
