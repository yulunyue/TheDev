from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true
import heapq
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict( n = 12, primes = [2,7,13,19],result=32 ),
        ]
    def execute(self, n: int, primes: List[int]) -> int:
        h=[1]
        for _ in range(n-1):
            a=heapq.heappop(h)
            while h and a==h[0]:
                a=heapq.heappop(h)
            for p in primes:
                heapq.heappush(h,a*p)
        return h[0]
    def nthSuperUglyNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)



if __name__=='__main__':
    Solution().run()