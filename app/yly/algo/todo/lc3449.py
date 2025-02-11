from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,math
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(points = [5,3], m = 8,result=12),
            dict(points = [1,8],m=10,result=5),
            dict(points = [2,4], m = 3,result=4),
            
            
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
            l2=[]
            s2=0
            for i in range(n):
                c=math.ceil(v/points[i])
                l2.append(c)
                s2+=c
            if s2>m:
                return 1
            self.log(v,l2)
            return 0
        return bisect.bisect_left(range(l,r+1),1,key=check)-1


    def maxScore(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        


if __name__=='__main__':
    Solution().run()