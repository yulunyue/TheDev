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
        ct = [[] for _ in range(51)]
        for s in range(5000, -1, -1):
            ct[sum([int(v) for v in str(s)])].append(s)

        @functools.lru_cache(None)
        def dfs(i, last_v):
            if i == len(digitSum):
                return 1
            ans = 0
            for u in ct[digitSum[i]]:
                if u < last_v:
                    break
                ans = (ans + dfs(i + 1, u)) % CT.MOD
            return ans

        return dfs(0, 0)

    execute = countArrays
