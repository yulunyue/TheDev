from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
import math
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/maximize-the-distance-between-points-on-a-square/description/'
    def get_cases(self):
        return [

        ]
    def execute(self, side: int, points: List[List[int]], k: int) -> int:
        mx=math.sqrt(side*2)
        pts=[]
        for x,y in points:
            pass
        def check():
            pass
    def maxDistance(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        



if __name__=='__main__':
    Solution().run()