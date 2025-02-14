from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,\
    Dict,List,MOD,inf,heapq
from common.algo.math_util import prime_flags
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n=10,result=4),
            dict(n=12,result=5),
        ]
    
    def countPrimes(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self, n: int) -> int:    
        return sum(prime_flags(n))



if __name__=='__main__':
    Solution().run()