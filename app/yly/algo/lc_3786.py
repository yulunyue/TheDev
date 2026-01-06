from common.util.export import MockCf,List

class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(n = 4, edges = [[0,1],[0,2],[0,3]], group = [1,1,4,4],result=3))
    def interactionCosts(self, n: int, edges: List[List[int]], group: List[int]) -> int:
        g=[[] for _ in range(n)]
        for f,t in edges:
            g[f].append(t)
            g[t].append(f)
        self.ans=0
        sm=[defaultdict(lambda :[0,0]) for _ in range(n)]
        def dfs(v,p,d=0):
            for u in g[v]:
                if u==p:continue
                dfs(u,v,d+1)
                for i,c in enumerate(sm[u]):
                    sm[v][i]+=c
            sm[v][group[v]][1]+=d
        dfs(0,-1)
        ans=[0]*20
        def dfs(v,p,d=0):
            for u in g[v]:
                if u==p:continue
                dfs(u,v,d+1)
        dfs(0,-1)

if __name__=="__main__":
    Solution().run()
