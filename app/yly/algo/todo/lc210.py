from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq
from common.algo.graph import Graph
class G(Graph):
    def __init__(self, key=None):
        self.ans=[]
        super().__init__(key)
        
    def tupu_end(self, q):
        self.ans.append(q[0].key)
        return super().tupu_end(q)
    
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/course-schedule-ii/submissions/600740407/'
    def get_cases(self):
        '''
        numCourses =
3
prerequisites =
[[1,0],[1,2],[0,1]]
        '''
        return [
            dict(numCourses = 3, prerequisites = [[1,0]],result=[2,0,1]),
            dict(numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]],result=[0,2,1,3]),
        ]
    def execute(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        if not prerequisites:
            return list(range(numCourses))
        g=G().reset()
        for v in range(numCourses):
            g.add_node(v)
        for a1,a0 in prerequisites:
            g.add_edge(a0,a1)
        g.tupu()
        return g.ans

    def findOrder(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        




if __name__=='__main__':
    Solution().run()