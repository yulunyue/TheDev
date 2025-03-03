from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n = 3, k = 2,result=[3,2,1]),
        ]
    def e_num(self,v,k):
        n=[v//2,(v+1)//2]
        c=[1,1]
        for i in range(1,v+1):
            if i!=n:
                c[0]=c[0]*i
            c[1]=c[1]*i
        if k>c[0]*c[1]:
            return []
        self.log(c,n)
        ret=[]
        for i in range(v+1,1,1):
            c[i%2]=c[i%2]//((v+1)//2)
            j=k//c[i%2]
            ret.append(j*2+v%2)
        return ret
    
    def o_num(self):
        pass

    def execute(self, n: int, k: int) -> List[int]:
        return self.e_num(n,k) if n%2==1 else self.o_num(n,k)
    
    def permute(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()