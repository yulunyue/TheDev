from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,math
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(points = [2,4], m = 3,result=4),
            dict(points = [10,1]+[100000]*200+[20,2,22], m = 1213,result=338),
            
        ]
    
    def execute(self, points: List[int], m: int) -> int:
        if m<len(points):
            return 0
        '''
        n[i]=n[i-1]+n[i+1]
        '''
        n=len(points)
        mn=min(points)
        l,r=0,mn*m
        def check(v):
            m1=0
            l2=[]
            for i in range(n):
                c=math.ceil(v/points[i])
                if len(l2)>=2 and l2[-1]-l2[-2]>c:
                    c=l2[-1]-l2[-2]
                l2.append(c)
                m1+=c
                if m1>m:
                    return 1
            return 0
        return bisect.bisect_left(range(l,r+1),1,key=check)-1


    def maxScore(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        


if __name__=='__main__':
    Solution().run()