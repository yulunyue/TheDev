from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
from common.algo.graph import Graph
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/minimum-height-trees/description/'
    def get_cases(self):
        return [
            dict(n =6,edges =[[3,0],[3,1],[3,2],[3,4],[5,4]],result=[3,4]),
            dict(n = 4, edges = [[1,0],[1,2],[1,3]],result=[1]),
            
        ]
    
    def findMinHeightTrees(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)

    def execute(self, n: int, edges: List[List[int]]) -> List[int]:
        self.g=Graph().reset()
        for f,t in edges:
            self.g.add_edge(f,t)
            self.g.add_edge(t,f)
        return [v.key for v in self.g.tupu(indeg_aim=1)]
if __name__=='__main__':
    Solution().run()