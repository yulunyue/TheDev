from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n =6,edges =[[3,0],[3,1],[3,2],[3,4],[5,4]],result=[3,4]),
            dict(n = 4, edges = [[1,0],[1,2],[1,3]],result=[1]),
            
        ]
    
    def findMinHeightTrees(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)

    def execute(self, n: int, edges: List[List[int]]) -> List[int]:
        ret=[inf,[]]
        g=[[] for _ in range(n)]
        for f,t in edges:
            g[f].append(t)
            g[t].append(f)
        def st(v,idx,l=None):

            if v<ret[0]:
                ret[1]=[idx]
                ret[0]=v
            elif v==ret[0]:
                ret[1].append(idx)
        l=[]
        def dfs(u,f=-1,a=0):
            l=[]
            for v in g[u]:
                if v==f:
                    continue
                l.append(dfs(v,u,a+1))
            return a
        st(dfs(0),0,-1)
        return ret[1]
if __name__=='__main__':
    Solution().run()