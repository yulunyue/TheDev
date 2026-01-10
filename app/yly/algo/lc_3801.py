class Solution:
    def get_cases(self):
        return dict(case0=dict(lists=[[1, 3, 5], [2, 4], [6, 7, 8]], result=18))

    def minMergeCost(self, lists: List[List[int]]) -> int:
        n=len(lists)
        u=(1<<n)-1
        sl=[[] for _ in range(u)]
        for i in range(n):
            m=1<<i
            s[m]=lists[i]
            while m:
        def dfs(s):
            

