from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
from common.algo.math_util import china_rest_mod
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-ii/description/'
    def get_cases(self):
        return [
            dict(s = "3902",result=True),
            dict(s='34789',result=False)
        ]
    def execute(self, s: str) -> bool:
        n=len(s)
        s=[int(v) for v in s]
        a=b=0
        for i in range(n-1):
            c=china_rest_mod(n-2,i,[2,5])
            a=(a+c*s[i])%10
            b=(b+c*s[i+1])%10
        return a==b
    def hasSameDigits(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        




if __name__=='__main__':
    Solution().run()