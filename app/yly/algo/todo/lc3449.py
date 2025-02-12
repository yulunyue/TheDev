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
        n=len(points)
        mn=min(points)
        def check(v):
            l=[]
            lc=0
            s2=0
            for i in range(n):
                c=math.ceil(v/points[i])
                if i>=1:
                    ca=c-l[i-1]-lc
                    if ca<=0:
                        
                        ca=0
                l.append(c)
                s2+=c
                if s2>m:
                    return 1
            # l.append(0)
            # self.log('l',v,l,1)
            # # zero=1
            # for i in range(n,0,-1):
            #     if l[i]<l[i+1]+l[i-1]:
            #         s2+=l[i+1]+l[i-1]-l[i]
            #         if s2>m:
            #             return 1
            #         l[i]=l[i+1]+l[i-1]
            self.log('r',v,l,0)
            return 0
        return bisect.bisect_left(range(0,mn*m),1,key=check)-1


    def maxScore(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        


if __name__=='__main__':
    Solution().run()