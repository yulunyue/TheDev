from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n=2,k=3,result=[]),
            dict(n = 4, k = 6,result=[3,4,1,2]),
            dict(n = 3, k = 2,result=[3,2,1]),
        ]

    

    def execute(self, n: int, k: int) -> List[int]:
        s=[1]
        for i in range(1,n):
            s.append(s[-1]*(i//2+1))
        ret=[]
        for i in range(n-1,-1,-1):
            v,k=k//s[i],k%s[i]
            if n%2==1:
                ret.append(v*2+(1 if i%2==0 else 2))
            else:
                ret.append(v*2+(2 if i%2==0 else 1))
            # self.log(v,k)
        return ret if k<=0 else []
    def permute(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()