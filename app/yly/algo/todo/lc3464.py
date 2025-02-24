from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
import math
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/maximize-the-distance-between-points-on-a-square/description/'
    def get_cases(self):
        return [
            dict(side=2, points = [[0,0],[1,2],[2,0],[2,2],[2,1]], k = 4,result=1)
        ]
    def execute(self, side: int, points: List[List[int]], k: int) -> int:
        p=[]
        for x,y in points:
            if x==0:
                p.append(y)
            elif y==side:
                p.append(x+side)
            elif x==side:
                p.append(3*side-y)
            else:
                p.append(4*side-x)
        p.sort()
        # self.log(p)
        def check(low):
            for start in p:
                cur,end=start,start+4*side-low
                for _ in range(k-1):
                    i=bisect.bisect_left(p,cur+side)
                    if i==len(p) or p[i]>end:
                        break
                else:
                    return True
            return False

        return bisect.bisect_left(range(1,side+1),True,key=check)+1

    def maxDistance(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        



if __name__=='__main__':
    Solution().run()